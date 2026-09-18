/**
 * Oh My Pi counterpart of the Claude Code hooks in .claude/settings.json (and the plugin's
 * hooks/hooks.json). omp does not run Claude's shell hooks, so this extension supplies the
 * same guarantees:
 *   - the `AIDLC project mode:` line on the first turn (`aidlc.py mode`), followed by the
 *     scaffold line when `.aidlc/manifest.json` was written by another plugin version
 *   - refusal to edit reproduction tests listed in `.aidlc/fix/*.json` while a fix is in progress
 *   - confirmation before any `git commit` / `git push` (blocked outright without a UI)
 *   - the content boundary on changes/**\/*.md and docs/solutions/**\/*.md (`aidlc.py lint-artifacts --stdin`)
 * Loaded from the plugin (omp/aidlc-guards.ts beside scripts/aidlc.py) it uses the plugin's helper and
 * sets CLAUDE_PLUGIN_ROOT; loaded from the package (.omp/hooks/pre/) it uses the project's scripts/aidlc.py.
 * Worktree naming stays with the Claude hook; omp sessions use `git worktree add` per the skill fallback.
 */
import type { ExtensionAPI } from "@oh-my-pi/pi-coding-agent";
import { execFileSync } from "node:child_process";
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { dirname, isAbsolute, join, relative, resolve } from "node:path";

const SESSION_MARKERS = [join("scripts", "aidlc.py"), ".git"];
const FIX_MARKERS = [join(".aidlc", "fix"), ".git"];
const PLUGIN_ROOT = resolve(import.meta.dir, "..");
const PLUGIN_HELPER = join(PLUGIN_ROOT, "scripts", "aidlc.py");
const PLUGIN_LAYOUT = existsSync(PLUGIN_HELPER);
if (PLUGIN_LAYOUT && !process.env.CLAUDE_PLUGIN_ROOT) process.env.CLAUDE_PLUGIN_ROOT = PLUGIN_ROOT;

const COMMAND_SEPARATORS = /&&|\|\||[;|\n]/;
const ENV_ASSIGNMENT = /^[A-Za-z_][A-Za-z0-9_]*=/;
const GIT_OPTIONS_WITH_VALUE: Record<string, true> = { "-C": true, "-c": true, "--git-dir": true, "--work-tree": true, "--namespace": true, "--exec-path": true };
const GH_OPTIONS_WITH_VALUE: Record<string, true> = { "-R": true, "--repo": true };
const PR_SUBCOMMANDS: Record<string, true> = { create: true, merge: true, ready: true, edit: true, close: true, reopen: true };
const FORCE_FLAGS = ["--force", "-f", "--force-with-lease", "--force-if-includes"];
const GUARDED_ARTIFACTS = /^(changes|docs\/solutions)\/.*\.md$/;
const PR_REASON = "AIDLC: opening or merging a pull request and force-pushing run only on your confirmation; /lbvs-aidlc-ship asks its own question first.";

function wordsOf(segment: string): string[] {
  const words = segment.trim().split(/\s+/).filter(Boolean);
  while (words.length && ENV_ASSIGNMENT.test(words[0])) words.shift();
  if (words.length) words[0] = words[0].replace(/^[({]+/, "");
  return words;
}

function positional(words: string[], optionsWithValue: Record<string, true>): string[] {
  for (let i = 1; i < words.length; i++) {
    if (optionsWithValue[words[i]]) i++;
    else if (!words[i].startsWith("-")) return words.slice(i);
  }
  return [];
}

/** True when a simple command opens/merges a pull request (`gh pr …`, `gh api … /pulls` non-GET) or force-pushes. */
function needsConfirmation(segment: string): boolean {
  const words = wordsOf(segment);
  if (!words.length) return false;
  if (words[0] === "gh") {
    const rest = positional(words, GH_OPTIONS_WITH_VALUE);
    if (rest[0] === "pr" && rest.length > 1 && PR_SUBCOMMANDS[rest[1]]) return true;
    const method = words.findIndex((word) => word === "-X" || word === "--method");
    return rest[0] === "api" && rest.some((word) => word.includes("/pulls")) && method >= 0 && words[method + 1]?.toUpperCase() !== "GET";
  }
  if (words[0] === "git") {
    const rest = positional(words, GIT_OPTIONS_WITH_VALUE);
    return rest[0] === "push" && rest.slice(1).some((word) => word.startsWith("+") || FORCE_FLAGS.some((flag) => word.startsWith(flag)));
  }
  return false;
}

function touchesRemoteHistory(command: string): boolean {
  return command.split(COMMAND_SEPARATORS).some(needsConfirmation);
}

function readVersion(path: string, key: string): string | undefined {
  try {
    const value = JSON.parse(readFileSync(path, "utf8"))[key];
    return typeof value === "string" && value ? value : undefined;
  } catch { return undefined; }
}

/** `AIDLC scaffold: …` when the repository's manifest was written by another plugin version. */
function scaffoldLine(root: string): string | undefined {
  const installed = readVersion(join(root, ".aidlc", "manifest.json"), "plugin_version");
  if (!installed) return undefined;
  const pluginRoot = process.env.CLAUDE_PLUGIN_ROOT || join(root, "plugins", "lbvs-aidlc");
  const running = readVersion(join(pluginRoot, ".claude-plugin", "plugin.json"), "version");
  if (!running || running === installed) return undefined;
  return `AIDLC scaffold: installed with plugin ${installed}, running ${running} — run \`aidlc update\` to refresh repository seeds.`;
}

/** New text per target of a write (`content`) or hashline edit (`+` body rows under each `[path#TAG]` section). */
function newTextByTarget(toolName: string, input: Record<string, unknown>): Map<string, string> {
  const texts = new Map<string, string>();
  if (toolName === "write" && typeof input.path === "string" && typeof input.content === "string") {
    texts.set(input.path, input.content);
  } else if (toolName === "edit" && typeof input.input === "string") {
    let target: string | undefined;
    for (const line of input.input.split("\n")) {
      const header = /^\[([^\]#\n]+)#[0-9A-Fa-f]{4}\]\s*$/.exec(line);
      if (header) target = header[1].trim();
      else if (target && line.startsWith("+")) texts.set(target, `${texts.get(target) ?? ""}${line.slice(1)}\n`);
    }
  }
  return texts;
}

/** Nearest ancestor of `start` (inclusive) holding one of `markers`; `start` itself when none does. */
function projectRoot(start: string, markers: string[] = SESSION_MARKERS): string {
  let dir = resolve(start);
  for (;;) {
    if (markers.some((marker) => existsSync(join(dir, marker)))) return dir;
    const parent = dirname(dir);
    if (parent === dir) return resolve(start);
    dir = parent;
  }
}

function globToRegExp(pattern: string): RegExp {
  let source = "";
  for (let i = 0; i < pattern.length; i++) {
    const ch = pattern[i];
    if (ch === "*") {
      if (pattern[i + 1] === "*") { source += ".*"; i++; } else source += "[^/]*";
    } else if (ch === "?") source += "[^/]";
    else source += ch.replace(/[.+^${}()|[\]\\]/g, "\\$&");
  }
  return new RegExp(`^${source}$`);
}

function protectedEntries(root: string): { change: string; pattern: string }[] {
  const dir = join(root, ".aidlc", "fix");
  if (!existsSync(dir)) return [];
  const entries: { change: string; pattern: string }[] = [];
  for (const file of readdirSync(dir)) {
    if (!file.endsWith(".json")) continue;
    try {
      const marker = JSON.parse(readFileSync(join(dir, file), "utf8"));
      const change = typeof marker.change_id === "string" ? marker.change_id : file.replace(/\.json$/, "");
      for (const pattern of Array.isArray(marker.protected) ? marker.protected : []) {
        if (typeof pattern === "string" && pattern) entries.push({ change, pattern });
      }
    } catch { /* a malformed marker never blocks unrelated edits */ }
  }
  return entries;
}

function targetsOf(toolName: string, input: Record<string, unknown>): string[] {
  if (toolName === "write" && typeof input.path === "string") return [input.path];
  if (toolName === "edit" && typeof input.input === "string") {
    return [...input.input.matchAll(/^\[([^\]#\n]+)#[0-9A-Fa-f]{4}\]\s*$/gm)].map((m) => m[1].trim());
  }
  return [];
}

type TextBlock = { type: string; text?: string };

export default function aidlcGuards(pi: ExtensionAPI): void {
  let modeLine: string | undefined;

  // `AIDLC project mode: …` plus, when the repository seeds came from another plugin version, the scaffold line.
  function resolveMode(cwd: string): string | undefined {
    if (modeLine !== undefined) return modeLine || undefined;
    const root = projectRoot(cwd);
    const helper = PLUGIN_LAYOUT ? PLUGIN_HELPER : join(root, "scripts", "aidlc.py");
    if (!existsSync(helper)) { modeLine = ""; return undefined; }
    try {
      modeLine = execFileSync("python3", [helper, "--root", root, "mode"], { encoding: "utf8", timeout: 10_000, stdio: ["ignore", "pipe", "pipe"] }).trim();
    } catch (error) {
      const stderr = error && typeof error === "object" && "stderr" in error && typeof error.stderr === "string" ? error.stderr.trim() : "";
      const reason = (stderr || String(error)).split("\n")[0];
      modeLine = `AIDLC project mode: unavailable (${reason})`;
    }
    const scaffold = scaffoldLine(root);
    if (scaffold) modeLine = `${modeLine}\n${scaffold}`;
    return modeLine;
  }

  /** Block reason when `text` bound for `rel` breaks the content boundary; undefined when clean or unlintable. */
  function artifactViolation(root: string, rel: string, text: string): string | undefined {
    const helper = PLUGIN_LAYOUT ? PLUGIN_HELPER : join(root, "scripts", "aidlc.py");
    if (!existsSync(helper)) return undefined;
    try {
      execFileSync("python3", [helper, "lint-artifacts", "--stdin", rel], { cwd: root, input: text, encoding: "utf8", timeout: 20_000, stdio: ["pipe", "pipe", "pipe"] });
      return undefined;
    } catch (error) {
      if (!error || typeof error !== "object" || !("status" in error) || error.status !== 1) return undefined;
      const stdout = "stdout" in error && typeof error.stdout === "string" ? error.stdout : "";
      const hits = stdout.split("\n").filter((line) => line.trim()).slice(0, 5).join("\n");
      return `AIDLC: ${rel} would carry session or machine-local references:\n${hits}\nContent boundary: docs/ARTIFACTS.md#content-boundary`;
    }
  }

  // Opening or merging a PR and force-pushing run only on the engineer's confirmation; without a UI the call is blocked.
  // Ordinary git commit/push follow the host's own permission flow.
  pi.on("tool_call", async (event, ctx) => {
    if (event.toolName !== "bash") return;
    const command = (event.input as Record<string, unknown>).command;
    if (typeof command !== "string" || !touchesRemoteHistory(command)) return;
    if (!ctx.hasUI) return { block: true, reason: PR_REASON };
    const confirmed = await ctx.ui.confirm("AIDLC", `${command}\nOpen/merge this pull request or force-push?`);
    if (!confirmed) return { block: true, reason: PR_REASON };
  });

  // Content boundary on change artifacts and lessons, measured against the repository holding the target.
  pi.on("tool_call", async (event, ctx) => {
    if (event.toolName !== "edit" && event.toolName !== "write") return;
    const sessionRoot = projectRoot(ctx.cwd);
    for (const [target, text] of newTextByTarget(event.toolName, event.input as Record<string, unknown>)) {
      const absolute = isAbsolute(target) ? target : resolve(ctx.cwd, target);
      for (const root of [projectRoot(dirname(absolute), [".git"]), sessionRoot]) {
        const rel = relative(root, absolute).split("\\").join("/");
        if (!GUARDED_ARTIFACTS.test(rel)) continue;
        const reason = artifactViolation(root, rel, text);
        if (reason) return { block: true, reason };
        break;
      }
    }
  });

  let announced = false;

  // Shown in the transcript for the engineer.
  pi.on("before_agent_start", async (_event, ctx) => {
    const text = resolveMode(ctx.cwd);
    if (!text || announced) return;
    announced = true;
    return { message: { customType: "aidlc-project-mode", content: text, display: true, details: { root: projectRoot(ctx.cwd) } } };
  });

  // Custom transcript messages are not part of the model's context, so attach the line to the first user turn.
  pi.on("context", async (event, ctx) => {
    const text = resolveMode(ctx.cwd);
    if (!text) return;
    const messages = event.messages;
    const first = messages.findIndex((m) => m.role === "user" && Array.isArray(m.content));
    if (first < 0) return;
    const blocks = messages[first].content as unknown as TextBlock[];
    if (blocks.some((block) => block.type === "text" && typeof block.text === "string" && block.text.includes("AIDLC project mode:"))) return;
    const updated = messages.slice();
    updated[first] = { ...messages[first], content: [...blocks, { type: "text", text: `[aidlc-project-mode]\n${text}` }] } as typeof messages[number];
    return { messages: updated };
  });

  // Protection is checked against the session root and against the repository that holds the
  // target itself: a fix worktree's markers must hold even when the session cwd is elsewhere.
  pi.on("tool_call", async (event, ctx) => {
    if (event.toolName !== "edit" && event.toolName !== "write") return;
    const sessionRoot = projectRoot(ctx.cwd);
    const sessionEntries = protectedEntries(sessionRoot);
    for (const target of targetsOf(event.toolName, event.input as Record<string, unknown>)) {
      const absolute = isAbsolute(target) ? target : resolve(ctx.cwd, target);
      const targetRoot = projectRoot(dirname(absolute), FIX_MARKERS);
      const scopes = [{ root: sessionRoot, entries: sessionEntries }];
      if (targetRoot !== sessionRoot) scopes.unshift({ root: targetRoot, entries: protectedEntries(targetRoot) });
      for (const { root, entries } of scopes) {
        const rel = relative(root, absolute).split("\\").join("/");
        for (const { change, pattern } of entries) {
          const regex = globToRegExp(pattern);
          if (regex.test(rel) || regex.test(absolute) || rel === pattern) {
            return {
              block: true,
              reason: `lbvs-aidlc-fix protects ${rel} while change '${change}' is in progress (marker .aidlc/fix/${change}.json). Keep the failing reproduction test unchanged; if the test itself is wrong, ask the user to lift protection by deleting the marker.`,
            };
          }
        }
      }
    }
  });
}

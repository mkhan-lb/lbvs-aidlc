/**
 * Oh My Pi counterpart of the Claude Code hooks in .claude/settings.json.
 * omp does not run Claude's shell hooks, so this extension supplies the same two guarantees:
 *   - the `AIDLC project mode:` line on the first turn (`scripts/aidlc.py mode`)
 *   - refusal to edit reproduction tests listed in `.aidlc/fix/*.json` while a fix is in progress
 * Worktree naming stays with the Claude hook; omp sessions use `git worktree add` per the skill fallback.
 */
import type { ExtensionAPI } from "@oh-my-pi/pi-coding-agent";
import { execFileSync } from "node:child_process";
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { dirname, isAbsolute, join, relative, resolve } from "node:path";

function projectRoot(cwd: string): string {
  let dir = resolve(cwd);
  for (;;) {
    if (existsSync(join(dir, "scripts", "aidlc.py")) || existsSync(join(dir, ".git"))) return dir;
    const parent = dirname(dir);
    if (parent === dir) return resolve(cwd);
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

  function resolveMode(cwd: string): string | undefined {
    if (modeLine !== undefined) return modeLine || undefined;
    const root = projectRoot(cwd);
    const helper = join(root, "scripts", "aidlc.py");
    if (!existsSync(helper)) { modeLine = ""; return undefined; }
    try {
      modeLine = execFileSync("python3", [helper, "--root", root, "mode"], { encoding: "utf8", timeout: 10_000 }).trim();
    } catch (error) {
      modeLine = `AIDLC project mode: unavailable (${String(error).split("\n")[0]})`;
    }
    return modeLine;
  }

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

  pi.on("tool_call", async (event, ctx) => {
    if (event.toolName !== "edit" && event.toolName !== "write") return;
    const root = projectRoot(ctx.cwd);
    const entries = protectedEntries(root);
    if (entries.length === 0) return;
    for (const target of targetsOf(event.toolName, event.input as Record<string, unknown>)) {
      const absolute = isAbsolute(target) ? target : resolve(ctx.cwd, target);
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
  });
}

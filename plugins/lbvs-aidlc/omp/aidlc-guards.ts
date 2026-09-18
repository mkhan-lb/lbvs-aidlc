/**
 * Oh My Pi adapter for the AIDLC hook scripts. omp does not run Claude Code's shell hooks, so this
 * extension builds the same JSON payload Claude Code would send, runs the same scripts, and turns
 * their decisions into omp results:
 *   - SessionStart:  `aidlc.py mode`, scaffold-check.sh, style-mode.sh → text attached to the first user turn
 *   - PreToolUse:    write/edit → protect-tests.sh and artifact-guard.sh (one payload per target file);
 *                    bash       → pr-guard.sh
 *   `deny` blocks the call; `ask` asks the engineer through the omp UI and blocks without one.
 * Every rule lives in the scripts. Nothing here decides on its own.
 * Loaded from the plugin (omp/aidlc-guards.ts beside hooks/ and scripts/) it uses the plugin's copies and
 * exports CLAUDE_PLUGIN_ROOT; loaded from the package (.omp/hooks/pre/) it uses .claude/hooks and scripts/aidlc.py.
 * Worktree naming stays with the Claude hook; omp sessions use `git worktree add` per the skill fallback.
 */
import type { ExtensionAPI } from "@oh-my-pi/pi-coding-agent";
import { execFileSync } from "node:child_process";
import { existsSync } from "node:fs";
import { dirname, isAbsolute, join, resolve } from "node:path";

const SESSION_MARKERS = [join("scripts", "aidlc.py"), ".git"];
const PLUGIN_ROOT = resolve(import.meta.dir, "..");
const PLUGIN_LAYOUT = existsSync(join(PLUGIN_ROOT, "scripts", "aidlc.py"));
if (PLUGIN_LAYOUT && !process.env.CLAUDE_PLUGIN_ROOT) process.env.CLAUDE_PLUGIN_ROOT = PLUGIN_ROOT;

const EDIT_SCRIPTS = ["protect-tests.sh", "artifact-guard.sh"];
const BASH_SCRIPTS = ["pr-guard.sh"];
const SESSION_SCRIPTS = ["scaffold-check.sh", "style-mode.sh"];

type Decision = { permissionDecision?: string; permissionDecisionReason?: string };
type TextBlock = { type: string; text?: string };

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

function helperPath(root: string): string {
  return PLUGIN_LAYOUT ? join(PLUGIN_ROOT, "scripts", "aidlc.py") : join(root, "scripts", "aidlc.py");
}

function scriptPath(root: string, name: string): string {
  return PLUGIN_LAYOUT ? join(PLUGIN_ROOT, "hooks", name) : join(root, ".claude", "hooks", name);
}

/** Run one hook script with a Claude-shaped payload on stdin; empty string when absent, silent or failing. */
function runHook(root: string, name: string, payload: Record<string, unknown>): string {
  const script = scriptPath(root, name);
  if (!existsSync(script)) return "";
  try {
    return execFileSync("sh", [script], {
      input: JSON.stringify(payload), encoding: "utf8", timeout: 20_000, stdio: ["pipe", "pipe", "ignore"],
      env: { ...process.env, CLAUDE_PROJECT_DIR: root },
    }).trim();
  } catch { return ""; }
}

function decisionOf(output: string): Decision {
  if (!output.startsWith("{")) return {};
  try { return (JSON.parse(output).hookSpecificOutput ?? {}) as Decision; } catch { return {}; }
}

/** Claude PreToolUse payloads for an omp tool call: bash → one Bash payload; write/edit → one Write payload per target
 *  (`+` body rows under each `[path#TAG]` hashline section become that target's new content). */
function preToolUsePayloads(toolName: string, input: Record<string, unknown>, cwd: string): Record<string, unknown>[] {
  const base = { hook_event_name: "PreToolUse", cwd };
  if (toolName === "bash" && typeof input.command === "string") {
    return [{ ...base, tool_name: "Bash", tool_input: { command: input.command } }];
  }
  const texts = new Map<string, string>();
  if (toolName === "write" && typeof input.path === "string") {
    texts.set(input.path, typeof input.content === "string" ? input.content : "");
  } else if (toolName === "edit" && typeof input.input === "string") {
    let target: string | undefined;
    for (const line of input.input.split("\n")) {
      const header = /^\[([^\]#\n]+)#[0-9A-Fa-f]{4}\]\s*$/.exec(line);
      if (header) { target = header[1].trim(); if (!texts.has(target)) texts.set(target, ""); }
      else if (target && line.startsWith("+")) texts.set(target, `${texts.get(target)}${line.slice(1)}\n`);
    }
  }
  return [...texts].map(([path, content]) => ({
    ...base, tool_name: "Write",
    tool_input: { file_path: isAbsolute(path) ? path : resolve(cwd, path), content },
  }));
}

export default function aidlcGuards(pi: ExtensionAPI): void {
  let sessionText: string | undefined;

  /** `AIDLC project mode: …` from the helper, then whatever the SessionStart scripts print (scaffold line, reply style). */
  function sessionContext(cwd: string): string | undefined {
    if (sessionText !== undefined) return sessionText || undefined;
    const root = projectRoot(cwd);
    const helper = helperPath(root);
    const lines: string[] = [];
    if (existsSync(helper)) {
      try {
        lines.push(execFileSync("python3", [helper, "--root", root, "mode"], { encoding: "utf8", timeout: 10_000, stdio: ["ignore", "pipe", "pipe"] }).trim());
      } catch (error) {
        const stderr = error && typeof error === "object" && "stderr" in error && typeof error.stderr === "string" ? error.stderr.trim() : "";
        lines.push(`AIDLC project mode: unavailable (${(stderr || String(error)).split("\n")[0]})`);
      }
    }
    for (const name of SESSION_SCRIPTS) {
      const output = runHook(root, name, { hook_event_name: "SessionStart", cwd: root, source: "startup" });
      if (output) lines.push(output);
    }
    sessionText = lines.join("\n");
    return sessionText || undefined;
  }

  pi.on("tool_call", async (event, ctx) => {
    const scripts = event.toolName === "bash" ? BASH_SCRIPTS : event.toolName === "write" || event.toolName === "edit" ? EDIT_SCRIPTS : [];
    if (!scripts.length) return;
    const root = projectRoot(ctx.cwd);
    for (const payload of preToolUsePayloads(event.toolName, event.input as Record<string, unknown>, ctx.cwd)) {
      for (const name of scripts) {
        const decision = decisionOf(runHook(root, name, payload));
        const reason = decision.permissionDecisionReason ?? `AIDLC: ${name} refused this call.`;
        if (decision.permissionDecision === "deny") return { block: true, reason };
        if (decision.permissionDecision === "ask") {
          if (!ctx.hasUI) return { block: true, reason };
          const summary = String((payload.tool_input as Record<string, unknown>).command ?? (payload.tool_input as Record<string, unknown>).file_path);
          const confirmed = await ctx.ui.confirm("AIDLC", `${summary}\n${reason}\nContinue?`);
          if (!confirmed) return { block: true, reason };
        }
      }
    }
  });

  let announced = false;

  // Shown in the transcript for the engineer.
  pi.on("before_agent_start", async (_event, ctx) => {
    const text = sessionContext(ctx.cwd);
    if (!text || announced) return;
    announced = true;
    return { message: { customType: "aidlc-project-mode", content: text, display: true, details: { root: projectRoot(ctx.cwd) } } };
  });

  // Custom transcript messages are not part of the model's context, so attach the text to the first user turn.
  pi.on("context", async (event, ctx) => {
    const text = sessionContext(ctx.cwd);
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
}

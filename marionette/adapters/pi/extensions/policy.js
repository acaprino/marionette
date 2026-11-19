import { readFileSync } from "node:fs";

const policy = readFileSync(new URL("../policy.md", import.meta.url), "utf8");
export default function packagePolicy(pi) {
  pi.on("before_agent_start", (event) => {
    event.systemPromptOptions.sections["muro_policy_marionette"] = policy;
  });
}

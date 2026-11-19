import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const skills = JSON.parse(readFileSync(new URL("./skills.json", import.meta.url), "utf8"));
const policy = readFileSync(new URL("./policy.md", import.meta.url), "utf8");

export default {
  id: "marionette",
  async setup(ctx) {
    await ctx.skill.transform((editor) => {
      for (const skill of skills) {
        editor.add({...skill, path: fileURLToPath(new URL(skill.path, import.meta.url))});
      }
    });
    const appendPolicy = (event) => {
      if (!event.system.some((part) => part.type === "text" && part.text === policy)) {
        event.system.push({type: "text", text: policy});
      }
    };
    for (const kind of ["context", "compaction", "generate", "title"]) {
      await ctx.session.hook(kind, appendPolicy);
    }
  },
};

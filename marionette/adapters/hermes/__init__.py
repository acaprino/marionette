"""Generated native Hermes registration. No work runs until the host loads it."""
from pathlib import Path


def register(ctx):
    root = Path(__file__).resolve().parent
    for skill in sorted((root / "skills").glob("*/SKILL.md")):
        ctx.register_skill(skill.parent.name, skill)

    register_section = getattr(ctx, "register_system_prompt_section", None)
    if not callable(register_section):
        import warnings
        warnings.warn(
            'Marionette always-on policy is not active: upgrade Hermes to a version with register_system_prompt_section, then reload the plugin and start a new session. The packaged skills remain available.',
            RuntimeWarning, stacklevel=2,
        )
        return
    # The build already bounded the policy (one allowance per contributing source); never cut it here.
    policy = (root / "policy.md").read_text(encoding="utf-8")
    if len(policy) <= 4000:
        register_section('marionette.always-on', policy, position="after_memory", max_chars=4000)
        return

    pieces = []
    for paragraph in policy.strip().split("\n\n"):
        if pieces and len(pieces[-1]) + 2 + len(paragraph) <= 8000:
            pieces[-1] += "\n\n" + paragraph
        else:
            pieces.append(paragraph)

    def sent(piece, history):
        for message in history or ():
            if not isinstance(message, dict):
                continue
            for value in (message.get("api_content"), message.get("content")):
                parts = value if isinstance(value, list) else [value]
                for part in parts:
                    text = part.get("text") if isinstance(part, dict) else part
                    if isinstance(text, str) and piece in text:
                        return True
        return False

    def deliver(piece):
        # Once per session, and again when compression dropped it; never the same text twice.
        def policy_context(conversation_history=None, **_):
            return None if sent(piece, conversation_history) else {"context": piece}
        return policy_context

    for piece in pieces:
        ctx.register_hook("pre_llm_call", deliver(piece))

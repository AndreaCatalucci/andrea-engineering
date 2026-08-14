# Codex Interaction Contract

Read this reference immediately before asking the user for input.

1. Follow the active Codex mode. When `request_user_input` is available and permitted, use it for a blocking decision. Otherwise ask clear numbered choices in chat, end the turn, and wait for the reply.
2. Never infer or silently skip a required answer. A skill may suppress a question only when its pipeline, headless, or non-interactive branch defines the replacement default or blocked result.
3. Ask one decision at a time unless the skill explicitly defines a bounded batch decision. Keep option labels self-contained and lead with the recommended option when one exists.

Skill-specific rules decide what to ask and which defaults are safe. This contract decides how the question reaches the user in Codex.

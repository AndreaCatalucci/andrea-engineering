---
name: unslop
description: Edit prose for clarity, precision, economy, and consistency. Run on every string a human will read this turn before you show it, and when the user says unslop.
---

# Unslop

Edit specific defects while preserving meaning and tone. An already clear sentence needs no change.

## Process

1. Inventory all user-visible text created or changed this turn: chat, document prose, UI labels, help, empty states, and assertions about copy.
2. Find the defects below. When several checks flag one sentence, identify the underlying problem and rewrite it once.
3. Use only facts, actors, mechanisms, and numbers supported by the surrounding context. If detail is unavailable, qualify or remove the claim.
4. Make one final pass for meaning, tone, accuracy, and readability. Revert preference-only edits and stop.

## Cut empty or inflated wording

Remove phrases that add no meaning, precision, or useful rhythm: "in order to," "it is important to note," "has the ability to," and "at its core." Prefer familiar verbs to inflated ones such as "utilize," "facilitate," and "leverage" when the plain term is equally accurate.

Cut appended benefit claims and endings that merely restate what the sentence or response already establishes. Keep consequences that explain an actual effect.

Bad: "The service retries failed requests, improving reliability."
Better: "The service retries failed requests up to three times, which prevents brief network failures from reaching the caller."

## Replace vague claims with evidence

Flag quality claims and weak modifiers such as seamless, robust, powerful, significant, substantially, efficiently, and obviously when the reader cannot tell what supports them. Replace them with an available fact, mechanism, or number. A scoped subjective judgment can remain when no measurement is available.

Name the source behind attributed claims. If "experts believe" or "studies show" cannot be tied to a source, remove the attribution and unsupported claim.

A verdict needs the fact that distinguishes it from plausible alternatives. This applies to "expected," "working as designed," and corrective labels.

Bad: "That is the leak guard working, not a failed inject."
Better: "The injection worked, but the child leaked the value into its output, so the leak guard stopped the process."

## Make responsibility and behavior concrete

Prefer actions to abstract nouns that hide who does what. Replace jargon when a familiar word is equally precise; keep established technical terms when they carry necessary meaning.

Use active voice when it clarifies responsibility. Passive voice is useful when the actor is unknown, irrelevant, or less important than the receiver.

Bad: "This enables improved coordination between workers."
Better: "Workers use the lease to decide which one owns the task."

For technical claims, name the behavior that creates the property. "Validation failures are surfaced clearly" becomes "The process exits with status 1 and prints the failing field."

Keep terminology stable when referring to the same thing. Changing "worker" to "processor" to "execution unit" obscures the reference unless the distinction is real.

## Keep emphasis and structure useful

Use contrast to correct a real misunderstanding or compare actual alternatives. Remove invented opposition such as "This isn't just X. It's Y." when it adds only emphasis.

Use "from X to Y" only for a meaningful scale. A list of unrelated capabilities is not a range.

Let punctuation express syntax. Repeated em dashes, interrupting asides, or punctuation used as emphasis may need a clearer sentence; punctuation itself is not a defect.

Match structure to the information. Use lists for parallel items or steps and headings when they help navigation. Remove repetitive labels, unnecessary introductions, nested lists without useful hierarchy, and conclusions that repeat the answer.

## Final check

For each edit, identify the concrete defect it fixed. Confirm it preserves meaning and tone, adds no unsupported fact, and is easier to understand. If the remaining difference is taste, keep the writer's version.

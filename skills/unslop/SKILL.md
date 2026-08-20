---
name: unslop
description: Edit prose for clarity, precision, economy, and consistency. Run on every string a human will read this turn before you show it, and when the user says unslop.
---

# Unslop

## Process

1. Inventory every user-visible string this turn created or changed. Chat is one item. Templates, empty states, help panels, button labels, and test assertions of copy are others. If you unslopped the wrap-up and not the h1, you failed.
2. Scan each item for the problems below.
3. Rewrite only the flagged text. Pull in an actor, mechanism, or number already known from this turn or the surrounding text; do not invent one.
4. Stop after the final pass.

Each check below flags a specific problem. Apply it only when a sentence actually has that problem. Extra words are one class of problem. Compression is another: a verdict, diagnosis, or contrast that omits the fact the reader needs.

## Resolve overlapping checks

A sentence can trip several checks at once. Treat that as one underlying problem, not several fixes applied in sequence: patching the weak modifier, then the abstract noun, then the trailing clause leaves a sentence rewritten three times over, each pass justified alone.

Instead, find what the sentence is actually missing (usually a named actor, mechanism, or number) and rewrite once. Re-read before checking whether any originally flagged problem remains.

## Cut words that do no work

Remove a word or phrase when it adds no meaning, precision, tone, or useful rhythm. Examples: "in order to" -> "to", "due to the fact that" -> "because", "it is important to note that" -> delete, "has the ability to" -> "can", "at this point in time" -> "now".

Bad: "It is important to note that the service can restart automatically." Better: "The service can restart automatically."

## Replace vague claims with useful information

Flag a claim when it describes quality without telling the reader what causes it, what changed, or how large the effect is. Examples: seamless, robust, powerful, intuitive, efficient, significant, substantial, flexible, scalable.

Replace the claim with a fact, mechanism, example, or number when one is already known.

Bad: "The API provides a seamless developer experience." Better: "The API returns typed errors and exposes the generated SQL through `.toSQL()`."

Bad: "Startup is significantly faster." Better: "Startup time falls from 4.2 seconds to 1.8 seconds."

If no such fact is known, keep an appropriately qualified claim or remove it.

Not flagged: "The API is fast enough for interactive use." No number is available, and the claim is honestly scoped to "fast enough," not "fast."

## Name the source behind a claim

Flag a claim attributed to an unnamed group. Examples: "Experts believe...", "Industry reports suggest...", "Many teams find...", "Studies show...".

Bad: "Experts believe lease-based scheduling scales better than polling." Better: "Kubernetes switched its scheduler from polling to leases in 1.20 to cut API server load."

If the source can't be named, cut the claim instead of keeping a vague attribution.

## Replace inflated wording when a plain expression says the same thing

Flag wording that makes a simple point sound larger, more formal, or more important without adding meaning. Examples: pivotal, transformative, groundbreaking, testament to, evolving landscape, leverage, utilize, facilitate, serves as, stands as, harnesses.

Bad: "The cache serves as a robust mechanism for reducing repeated queries." Better: "The cache avoids repeated queries."

Bad: "The framework facilitates workflow orchestration." Better: "The framework runs workflows." If the mechanism matters: "The scheduler starts each workflow when its dependency finishes."

Keep a formal or technical term when it is more accurate than the simpler alternative.

## Prefer actions to abstractions

Flag abstract nouns when they hide who does what.

Bad: "This enables improved coordination between workers." Better: "Workers use the lease to decide which one owns the task."

Bad: "The system provides concurrency control." Better: "Each worker can hold one lease at a time."

Warning signs: coordination, optimization, orchestration, enablement, improvement, enhancement, alignment, management, handling, support.

Keep an abstraction when it is the subject itself.

Not flagged: "The service exposes a management API for rotating credentials." "Management" names the subject itself here.

## Replace abstract jargon nouns with plain words

Flag jargon nouns that sound technical but can be replaced with a plainer word. Examples: substrate, vector, primitive (as a noun), surface (as in "API surface"), bedrock, paradigm, north star, flywheel.

Bad: "The team is exploring a new vector for onboarding." Better: "The team is exploring a new way to onboard."

Bad: "Keep the API surface small." Better: "Keep the number of public functions small."

Keep the jargon term when it is the term practitioners actually use and a plainer word would be less precise.

## Remove clauses that only restate an implication

Flag appended clauses that claim a benefit without adding evidence or mechanism. Examples: highlighting, showcasing, underscoring, ensuring, reflecting, fostering, demonstrating, improving.

Bad: "The service retries failed requests, improving reliability." Better: "The service retries failed requests up to three times."

Keep the consequence when it adds information: "The service retries failed requests up to three times, which prevents brief network failures from reaching the caller."

## Remove empty framing

Flag openings that delay the point without changing it. Examples: "It is worth noting that...", "It is important to remember that...", "When it comes to...", "In today's...", "At its core...", "The key thing to understand is...", "There are several reasons why...".

Bad: "When it comes to authentication, the service uses signed cookies." Better: "The service uses signed cookies for authentication."

Keep framing when it supplies context the reader actually needs.

## Use contrast only when the contrast matters

Flag constructions that create emphasis by inventing an unnecessary opposition. Common forms: "This isn't just X. It's Y.", "Not only X, but Y.", "Rather than X, Y.", "It's less about X and more about Y.", "It's X, not Y."

Bad: "This isn't just a cache. It's a coordination layer." Better: "The cache also coordinates ownership between workers."

Keep the contrast when correcting a likely misunderstanding or distinguishing two real alternatives.

Not flagged: "This isn't a cache you can drop: deleting it loses customer records." The distinction is real, and the sentence names the consequence that makes it true.

## Qualify a verdict with the fact that makes it true

Flag a conclusion, diagnosis, or contrast when it names the verdict without the fact that distinguishes it from the likely alternative. The terms can be specific and the contrast real; the sentence is still unqualified if a reader cannot tell why the named verdict is true rather than the alternative.

Common forms: "That's X, not Y", "This is expected", "This is working as designed", a label applied to an observation.

Bad: "That is the leak guard working, not a failed inject." Better: "That's not a failed inject: the injection worked, but the child leaked the value into its own output, so the leak guard caught it and shut the process down."

Keep a short verdict when this sentence is only labeling evidence the reader just produced. If the sentence is correcting a misreading, it needs the distinguishing fact even when a nearby sentence describes the behavior.

## Size groups to the content

Flag lists whose structure appears driven by cadence rather than content. Symptoms: adding a third adjective to complete a trio, forcing three benefits where only two are supported, splitting one idea into three near-synonyms.

Bad: "The change makes the system faster, cleaner, and more efficient." Better: "The change cuts startup time and removes the extra configuration file."

Use however many items the content requires.

## Keep ranges on a real scale

Flag "from X to Y" phrasing when X and Y don't sit on a meaningful scale.

Bad: "The toolkit supports everything from unit tests to deployment pipelines." Better: "The toolkit runs unit tests and deploys the result."

Keep a range when the two ends are genuinely on the same scale: "Requests complete in 50ms to 200ms depending on cache state."

## Keep terminology stable

Flag synonym changes when the terms refer to the same thing and the variation adds no useful distinction.

Bad: "The worker starts the task. The processor handles the job. The execution unit records the result." Better: "The worker starts the task, processes it, and records the result."

Repeat a term when repetition makes the reference clearer. Change terminology only when the distinction is real.

## Prefer concrete technical statements

In technical prose, flag sentences that describe a desirable property without naming the behavior that creates it.

Bad: "Validation failures are surfaced clearly." Better: "The process exits with status 1 and prints the failing field."

Bad: "Types remain closely aligned with the schema." Better: "Renaming a column changes the generated TypeScript type and breaks callers that still use the old name."

Bad: "The system provides robust concurrency control." Better: "A worker must acquire the lease before processing the task."

Test: could this sentence appear unchanged in documentation for many unrelated products? If yes, check whether a project-specific fact can replace it. Keep the general statement when the text is intentionally describing a general concept.

## Use active voice when it clarifies responsibility

Flag passive voice when naming the actor would make the sentence clearer.

Bad: "Queries are validated before execution." Better: "The compiler validates queries before execution."

Keep passive voice when the actor is unknown, the actor does not matter, the receiver is the subject readers care about, or naming the actor makes the sentence worse.

## Frame instructions positively

Flag a prohibition ("do not X", "never X", "don't X") when a positive instruction states the same rule.

Bad: "Do not commit directly to main." Better: "Open a pull request for changes to main."

Keep the negative form when no positive instruction covers the same ground, or when it warns against a specific failure mode.

## Replace weak modifiers when the text can be more exact

Flag modifiers that claim degree without showing it. Examples: significantly, substantially, dramatically, effectively, efficiently, easily, simply, clearly, obviously, extremely.

Bad: "The system efficiently processes requests." Better: "The system processes 8,000 requests per second."

Bad: "The migration is extremely simple." Better: "The migration requires changing one configuration value."

Keep the modifier when it carries meaning that the text cannot state more precisely.

Not flagged: "The rollout was easy for us, but each team should judge that for their own setup." "Easy" reports a subjective experience explicitly scoped to "us"; no number would make it more precise without changing the claim.

## Split sentences that make the reader backtrack

Flag a sentence when its subject changes unnoticed, several clauses compete for attention, qualifications bury the main point, a pronoun has an unclear referent, or the reader must re-read it to understand the structure.

Split or reorder only enough to fix the problem. Related ideas can share one sentence, even a long one, when their relationship is clear.

## Remove canned conversational language

Flag stock phrases that add politeness, enthusiasm, or structure without adding content. Examples: "Of course!", "Certainly!", "Great question.", "You're absolutely right.", "Here's a breakdown.", "The key takeaway is...", "Let's dive in.", "Let's unpack this.", "I hope this helps.", "Let me know if you'd like...".

Bad: "Great question. Here's a breakdown of how the cache works." Better: "The cache stores each result for five minutes."

Keep conversational language when it serves the relationship, tone, or task. Otherwise replace it with real content.

## Preserve useful repetition

Keep repetition when it makes a reference unambiguous, reinforces an intentional point, preserves rhythm, avoids a worse synonym, or keeps technical terminology consistent. Flag it only when it repeats information without helping the reader.

## Remove conclusions that add no new information

Flag an ending when it only restates the body, announces importance, or gestures vaguely at the future.

Bad: "Ultimately, this represents an important step forward for the project." Better: "Version 2 removes the external Redis dependency."

If the previous sentence already completes the point, end there.

## Keep structure proportional to the content

Flag structure that makes simple material harder to read. Examples: an introduction before a short answer, headings for one or two sentences, a summary that repeats the body, numbered lists where order does not matter, automatic pros-and-cons sections, equal space for points of unequal importance, deep bullet nesting, labels that repeat the sentence after them, excessive boldface.

Keep structure that helps the reader scan, compare, follow steps, or find information.

## Use punctuation for syntax, not decoration

Flag punctuation when the same construction repeats often, punctuation substitutes for a clearer sentence structure, an aside interrupts the main point, or emphasis depends on punctuation rather than wording. Keep punctuation when it is the clearest way to express the sentence.

## Preserve distinctions

Keep a precise term when a simpler word would change the meaning.

Bad edit: "The function is idempotent." to "The function is safe." "Safe" is broader and less precise.

Plain language is useful only when it remains accurate.

## Final pass

Review each edit and ask:

1. What specific problem did this edit fix?
2. Did the new wording preserve the original meaning?
3. Did it preserve the writer's tone?
4. Did it invent a claim, opinion, or detail that was not in this turn's work or the surrounding text?
5. Is the new wording more precise or easier to understand?
6. Did a rule trigger the change, or did I change it because I preferred another style?

Revert edits that do not have a clear answer to the first question. Stop when every remaining change would be a matter of preference rather than a clear improvement.

## Worked example

This turn produced:

- h1: "Research support — not a broker"
- empty state: "You place the trades. Watchlists stay on this device."
- error copy: "That is the device lock, not a sign-in failure."
- chat wrap-up: "Added the empty-state copy."

Unslopping only the wrap-up fails the inventory.

1. The h1 trips two checks: an em dash used for emphasis, and a contrast that does not correct a likely misunderstanding. Rewrite once: "Research support."
2. "You place the trades" restates the heading. Cut it. Keep "Watchlists stay on this device."
3. The error copy's contrast is real, but the verdict has no distinguishing fact. The surrounding help text already says the device locks after three failed unlocks. Pull that in: "That's not a sign-in failure: the device locked after three failed unlocks."
4. The wrap-up has no problem.

Edited:

- h1: "Research support"
- empty state: "Watchlists stay on this device."
- error copy: "That's not a sign-in failure: the device locked after three failed unlocks."
- chat wrap-up: "Added the empty-state copy."

Copy lived in files. Checks that fired: punctuation used for emphasis; contrast that does not correct a misunderstanding; repetition that does not help the reader; a verdict without the fact that distinguishes it.

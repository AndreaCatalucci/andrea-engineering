---
name: unslop
description: Edit prose for clarity, precision, economy, and consistency while preserving meaning and tone.
---

# Unslop

Every edit must fix a specific problem.

Before changing a sentence, identify what is wrong with it. If none of the checks below applies, leave it unchanged.

Preserve meaning, tone, terminology, and level of formality unless the task asks you to change them.

## Process

1. Read the text before editing.
2. Identify specific problems using the checks below.
3. Rewrite only the affected text.
4. Prefer the smallest change that fixes the problem.
5. Re-read the edited passage in context.
6. Stop when no remaining change has a clear reason.

Do not treat these checks as a style template. They identify problems, not features every sentence should have.

## Cut words that do no work

Remove a word or phrase when it adds no meaning, precision, tone, or useful rhythm.

Common examples:

- "in order to" -> "to"
- "due to the fact that" -> "because"
- "it is important to note that" -> delete
- "has the ability to" -> "can"
- "at this point in time" -> "now"

Bad:

> It is important to note that the service can restart automatically.

Better:

> The service can restart automatically.

Do not shorten a sentence merely because a shorter version exists.

## Replace vague claims with useful information

Flag a claim when it describes quality without telling the reader what causes it, what changed, or how large the effect is.

Common examples:

- seamless
- robust
- powerful
- intuitive
- efficient
- significant
- substantial
- flexible
- scalable

Replace the claim with a fact, mechanism, example, or number when the text provides one.

Bad:

> The API provides a seamless developer experience.

Better:

> The API returns typed errors and exposes the generated SQL through `.toSQL()`.

Bad:

> Startup is significantly faster.

Better:

> Startup time falls from 4.2 seconds to 1.8 seconds.

Do not invent evidence. If the text does not support a stronger statement, keep an appropriately qualified claim or remove it.

## Replace inflated wording when a plain expression says the same thing

Flag wording that makes a simple point sound larger, more formal, or more important without adding meaning.

Common examples:

- pivotal
- transformative
- groundbreaking
- testament to
- evolving landscape
- leverage
- utilize
- facilitate
- serves as
- stands as
- harnesses

Bad:

> The cache serves as a robust mechanism for reducing repeated queries.

Better:

> The cache avoids repeated queries.

Bad:

> The framework facilitates workflow orchestration.

Better:

> The framework runs workflows.

If the mechanism matters:

> The scheduler starts each workflow when its dependency finishes.

Keep a formal or technical term when it is more accurate than the simpler alternative.

## Prefer actions to abstractions

Flag abstract nouns when they hide who does what.

Bad:

> This enables improved coordination between workers.

Better:

> Workers use the lease to decide which one owns the task.

Bad:

> The system provides concurrency control.

Better:

> Each worker can hold one lease at a time.

Common warning signs include:

- coordination
- optimization
- orchestration
- enablement
- improvement
- enhancement
- alignment
- management
- handling
- support

Do not replace an abstraction when the abstraction itself is the subject.

## Remove clauses that only restate an implication

Flag appended clauses that claim a benefit without adding evidence or mechanism.

Common forms include:

- highlighting...
- showcasing...
- underscoring...
- ensuring...
- reflecting...
- fostering...
- demonstrating...
- improving...

Bad:

> The service retries failed requests, improving reliability.

Better:

> The service retries failed requests up to three times.

Keep the consequence when it adds information:

> The service retries failed requests up to three times, which prevents brief network failures from reaching the caller.

## Remove empty framing

Flag openings that delay the point without changing it.

Common examples:

- "It is worth noting that..."
- "It is important to remember that..."
- "When it comes to..."
- "In today's..."
- "At its core..."
- "The key thing to understand is..."
- "There are several reasons why..."

Bad:

> When it comes to authentication, the service uses signed cookies.

Better:

> The service uses signed cookies for authentication.

Keep framing when it supplies context the reader actually needs.

## Use contrast only when the contrast matters

Flag constructions that create emphasis by inventing an unnecessary opposition.

Common forms:

> This isn't just X. It's Y.

> Not only X, but Y.

> Rather than X, Y.

> It's less about X and more about Y.

Bad:

> This isn't just a cache. It's a coordination layer.

Better:

> The cache also coordinates ownership between workers.

Keep the contrast when correcting a likely misunderstanding or distinguishing two real alternatives.

## Do not manufacture groups

Flag lists whose structure appears driven by cadence rather than content.

Common symptoms:

- adding a third adjective to complete a trio
- forcing three benefits where only two are supported
- splitting one idea into three near-synonyms

Bad:

> The change makes the system faster, cleaner, and more efficient.

Better:

> The change cuts startup time and removes the extra configuration file.

Use however many items the content requires.

## Keep terminology stable

Flag synonym changes when the terms refer to the same thing and the variation adds no useful distinction.

Bad:

> The worker starts the task. The processor handles the job. The execution unit records the result.

Better:

> The worker starts the task, processes it, and records the result.

Repeat a term when repetition makes the reference clearer.

Change terminology only when the distinction is real.

## Prefer concrete technical statements

In technical prose, flag sentences that describe a desirable property without naming the behavior that creates it.

Bad:

> Validation failures are surfaced clearly.

Better:

> The process exits with status 1 and prints the failing field.

Bad:

> Types remain closely aligned with the schema.

Better:

> Renaming a column changes the generated TypeScript type and breaks callers that still use the old name.

Bad:

> The system provides robust concurrency control.

Better:

> A worker must acquire the lease before processing the task.

Use this test:

> Could this sentence appear unchanged in documentation for many unrelated products?

If yes, check whether a project-specific fact can replace it.

Do not force specificity when the text is intentionally describing a general concept.

## Use active voice when it clarifies responsibility

Flag passive voice when naming the actor would make the sentence clearer.

Bad:

> Queries are validated before execution.

Better:

> The compiler validates queries before execution.

Keep passive voice when:

- the actor is unknown
- the actor does not matter
- the receiver is the subject readers care about
- naming the actor makes the sentence worse

Do not convert passive voice mechanically.

## Replace weak modifiers when the text can be more exact

Flag modifiers that claim degree without showing it.

Common examples:

- significantly
- substantially
- dramatically
- effectively
- efficiently
- easily
- simply
- clearly
- obviously
- extremely

Bad:

> The system efficiently processes requests.

Better:

> The system processes 8,000 requests per second.

Bad:

> The migration is extremely simple.

Better:

> The migration requires changing one configuration value.

Keep the modifier when it carries meaning that the text cannot state more precisely.

## Split sentences that make the reader backtrack

Flag a sentence when:

- its subject changes unnoticed
- several clauses compete for attention
- qualifications bury the main point
- a pronoun has an unclear referent
- the reader must re-read it to understand the structure

Split or reorder only enough to fix the problem.

Do not split a sentence merely because it is long.

Do not enforce one idea per sentence. Related ideas can share a sentence when their relationship is clear.

## Remove canned conversational language

Flag stock phrases that add politeness, enthusiasm, or structure without adding content.

Common examples:

- "Of course!"
- "Certainly!"
- "Great question."
- "You're absolutely right."
- "Here's a breakdown."
- "The key takeaway is..."
- "Let's dive in."
- "Let's unpack this."
- "I hope this helps."
- "Let me know if you'd like..."

Bad:

> Great question. Here's a breakdown of how the cache works.

Better:

> The cache stores each result for five minutes.

Keep conversational language when it serves the relationship, tone, or task.

Do not replace one stock phrase with another.

## Do not invent personality

Flag additions that introduce a stance or manner the writer did not express.

Examples:

- opinions
- jokes
- irritation
- enthusiasm
- skepticism
- slang
- first-person commentary
- deliberate roughness
- filler such as "honestly", "frankly", "actually", or "kind of"

Bad, when the source expressed no judgment:

> I find it pretty unsettling that the process keeps running.

Better:

> The process keeps running after the interface closes.

Keep personality already present in the source unless it conflicts with the requested tone.

## Preserve useful repetition

Do not remove repetition automatically.

Keep repetition when it:

- makes a reference unambiguous
- reinforces an intentional point
- preserves rhythm
- avoids a worse synonym
- keeps technical terminology consistent

Flag repetition only when it repeats information without helping the reader.

## Remove conclusions that add no new information

Flag an ending when it only restates the body, announces importance, or gestures vaguely at the future.

Bad:

> Ultimately, this represents an important step forward for the project.

Better:

> Version 2 removes the external Redis dependency.

If the previous sentence already completes the point, end there.

## Keep structure proportional to the content

Flag structure that makes simple material harder to read.

Examples:

- an introduction before a short answer
- headings for one or two sentences
- a summary that repeats the body
- numbered lists where order does not matter
- automatic pros-and-cons sections
- equal space for points of unequal importance
- deep bullet nesting
- labels that repeat the sentence after them
- excessive boldface

Do not remove structure that helps the reader scan, compare, follow steps, or find information.

## Use punctuation for syntax, not decoration

Do not ban em dashes, parentheses, colons, semicolons, or fragments.

Flag punctuation when:

- the same construction repeats often
- punctuation substitutes for a clearer sentence structure
- an aside interrupts the main point
- emphasis depends on punctuation rather than wording

Keep punctuation when it is the clearest way to express the sentence.

## Preserve uncertainty when it matters

Do not strengthen a claim merely to make the prose sound cleaner.

Keep words such as:

- may
- likely
- approximately
- usually
- appears
- suggests

when they represent real uncertainty.

Flag hedging only when several qualifiers express the same uncertainty.

Bad:

> This could potentially possibly cause delays.

Better:

> This could cause delays.

## Preserve distinctions

Do not replace precise terms with simpler words if doing so changes the meaning.

Bad edit:

> The function is idempotent.

to:

> The function is safe.

"Safe" is broader and less precise.

Plain language is useful only when it remains accurate.

## Final pass

Review each edit and ask:

1. What specific problem did this edit fix?
2. Did the new wording preserve the original meaning?
3. Did it preserve the writer's tone?
4. Did it add any claim, opinion, or detail that was not present?
5. Is the new wording more precise or easier to understand?
6. Did a rule trigger the change, or did I change it because I preferred another style?

Revert edits that do not have a clear answer to the first question.

Stop when every remaining change would be a matter of preference rather than a clear improvement.

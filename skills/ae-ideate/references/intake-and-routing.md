# Ideation Intake and Routing

Read this at Phase 0. Resolve clear prompts in one pass. Questions supply a
missing subject or usable source material; they do not decide the solution.

## Output and resume

Resolve one output format. An explicit `output:md`, `output:html`, or equivalent
request wins. An explicitly resumed ideation document keeps its extension.
Otherwise use HTML. Strip only a recognized output token.

Start fresh unless the user names an existing `.md` or `.html` ideation file.
For a named file, confirm that its subject matches, preserve useful ideas and
rejection history, and update it in place. If the requested format changed,
write a sibling file and leave the original intact. Never scan
`docs/ideation/` looking for something to resume.

## Identify the subject

Ask only when reasonable agents would disagree about the topic itself. A named
feature, flow, document, decision, or concept is enough. Catch-all words such
as “ideas,” “improvements,” or “bugs” are not. Being inside a repository does
not make a vague subject specific.

When genuinely uncertain in a repository, use a shallow filename and README
search. A matching footprint makes the subject identifiable. Otherwise ask:
“What should the agent ideate about?” Offer a free-form subject, “Surprise me,”
and cancel. Recheck one follow-up; do not drift into questions about audience,
constraints, success criteria, or solution direction. Those belong to
`ae-brainstorm`.

Issue-tracker intent requires explicit tracker language such as “GitHub
issues,” “issue themes,” “what users are reporting,” or “bug reports.” A bug
named as the topic is normal ideation, not tracker analysis.

In surprise-me mode there is no fixed subject. Inside a Git repository, inspect
the repository. Outside one, require at least one URL, description, file, or
paste before continuing.

## Choose the source of substance

Use repository mode when the prompt names this codebase, its files, workflows,
tests, architecture, or issue tracker. Use elsewhere mode when it names a
product or topic outside the repository. Within elsewhere mode, software
includes apps, services, pages, UX, pricing, copy, and positioning for a
software product. Non-software covers topics with no software surface, such as
naming, narrative, personal decisions, or physical products.

State the choice in the user's words, without internal mode names. For example:
“Treating this as a topic in this codebase — about authentication.” Ask for
confirmation only when two concrete interpretations remain genuinely
plausible.

Elsewhere work needs user-supplied substance. Apply this test: would replacing
one piece of the supplied material with a contrasting one change which ideas
survive? If not, ask for a URL or file, a short current-state description, or a
paste. Ask at most three narrow questions and stop when the answer is useful.
Accept “just go” except in surprise-me mode outside a repository, where some
material is mandatory.

## Focus, volume, and depth

Separate the subject from an optional focus, path, constraint, research file,
or volume request. Read default candidate quotas from `dispatch-rules.json`
and keep 5-7 final survivors. Honor requests such as “top 3,” “100 ideas,” or
“raise the bar” by adjusting bucket or survivor quotas deliberately.

“Go deep” selects the `go-deep` dispatch entry and a second verifier focused on
novelty and feasibility. Tactical words such as
“polish,” “typos,” “quick wins,” “cleanup,” or “small fixes” explicitly lower
the ambition floor; otherwise ideas should be meaningful enough to change what
the user does next.

Before generation, state the actual generation-agent count plus one verifier.
Mention the optional single recovery agent separately. Grounding runs in the
root. The notice is informational and does not require confirmation.

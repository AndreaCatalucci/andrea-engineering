# User-Supplied Research

Read this only when the user names gathered evidence such as a survey export,
analytics dump, interview notes, or social-research report.

First distinguish directives from evidence. A specification, TODO list, or
feedback the user explicitly wants addressed is a constraint. A report about
the world is evidence: it may support ideas but cannot veto them. A file takes
one route only.

Fold a small evidence file into the grounding summary under “User-supplied
research.” For a large file that would dominate the shared packet, spawn one
fresh-context distiller per document with
`agents/research-distiller.md`. Supply the subject, input path, and
`<scratch-dir>/evidence-user-research-<slug>.md` output path. Add only the
returned gist, path, and entry count to shared grounding. Generation agents and
the verifier read the dossier when needed.

Research files enrich normal web research; they replace it only when the user
explicitly asked to skip external research. Outside-repository synthesis reads
briefs and drafts, but routes large evidence exports here so noise does not
bury the current-state summary.

Derive the **question-agnostic project profile** for the repository at the current working directory — the stable orientation that repo-grounding skills reuse. The caller may perform this work inline or delegate it on a cache miss; either way, the output is written to the shared profile cache and reused across skills and sessions at this commit.

Derive ONLY agnostic, question-independent facts. Do NOT do any work specific to the caller's current question (a candidate's call-sites, a feature's footprint, prior-decision matches for a topic, feature-specific patterns, git history of touched files). Anything question-specific is the caller's job and must stay out of this profile, or the cached artifact becomes wrong to reuse.

Read efficiently — manifests, lockfiles, the license, the root instruction/doc files, and a top-level structure listing are enough. Do not read the whole tree.

Produce the profile by inspecting:

- **Stack & versions** — detected languages and major frameworks *with versions* (from manifests/lockfiles **and runtime version selectors** like `.nvmrc`/`.node-version`/`.python-version`/`.ruby-version`/`.tool-versions`/`mise.toml`, which pin versions outside the manifests), build/test tooling and commands.
- **Dependency surface** — manifest + lockfile paths present, the top-level (direct) dependency list, the project license, and dependency licenses where readily available.
- **Topology** — monorepo? the workspace/service map (name + primary language each), deployment model (monolith / multi-service / serverless), API styles (REST/gRPC/GraphQL/none), data stores and migration/ORM locations, and the module/internal-boundary layout.
- **Conventions & instruction files** — paths and a short digest of root `AGENTS.md`, `ARCHITECTURE.md`, `README.md`, `CONTRIBUTING.md`, and `STRATEGY.md`: coding standards, testing conventions, review process, and product direction. Keep subdirectory-scoped `AGENTS.md` files fresh rather than caching them.
- **Vocabulary** — from `CONCEPTS.md` if present, the canonical domain terms/processes/status concepts.

Do NOT include the `docs/solutions/` file enumeration or subdirectory-scoped instruction files — those are re-globbed fresh by consumers, never cached.

## Output

Return ONLY a single JSON object (no prose, no code fence) with these top-level keys, each populated from what you found (use `null` or `[]` when a category is absent):

```
{
  "stack": { "languages": [...], "frameworks": [...], "tooling": [...] },
  "dependencies": { "manifests": [...], "lockfiles": [...], "top_level": [...], "project_license": "...", "dependency_licenses": [...] },
  "topology": { "monorepo": true/false, "workspaces": [...], "deployment": "...", "api_styles": [...], "data_stores": [...], "module_layout": "..." },
  "conventions": { "instruction_files": [...], "coding_standards": "...", "testing": "...", "review_process": "...", "strategy": "..." },
  "vocabulary": { "concepts_present": true/false, "terms": [...] }
}
```

Keep each field concise — enough for a downstream skill to orient without re-reading the repo. This JSON is the entire deliverable.

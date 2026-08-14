---
name: ae-setup
description: "Check Andrea Engineering health and repo-local configuration. Use when diagnosing plugin setup, optional tool availability, or local configuration safety."
---

# Andrea Engineering Setup

Before asking for consent or configuration input, read and follow [`references/codex-interaction.md`](references/codex-interaction.md).

Check optional tool capabilities and repair repo-local configuration. Do not bulk-install optional dependencies.

## Diagnose

Run the bundled health check from the user's project. Set `SKILL_DIR` to the absolute directory containing this file; do not assume the current working directory is the skill directory.

```bash
SKILL_DIR="<absolute path of the directory containing this SKILL.md>";
if [ -f "$SKILL_DIR/scripts/check-health" ]; then bash "$SKILL_DIR/scripts/check-health"; else echo "Bundled health script not found at $SKILL_DIR/scripts/check-health; run the inline checks from ae-setup instead."; fi
```

If the script is unavailable, perform the inline equivalent:

1. Check optional tools with `command -v`: `gh`, `jq`, `ast-grep`, `ffmpeg`.
2. If inside a git repo, resolve the repo root with `git rev-parse --show-toplevel`.
3. Check for obsolete `andrea-engineering.local.md` at the repo root.
4. Check whether `.andrea-engineering/config.local.yaml` exists and, if it does, whether `git check-ignore -q .andrea-engineering/config.local.yaml` succeeds.
5. Compare `.andrea-engineering/config.local.example.yaml` with `references/config-template.yaml` when the template is readable; otherwise report that the example refresh must be done manually.

Treat missing optional tools as informational. Treat only these as project issues:

- obsolete `andrea-engineering.local.md`
- `.andrea-engineering/config.local.yaml` exists but is not safely gitignored
- `.andrea-engineering/config.local.example.yaml` is missing or outdated

If no project issues exist, skip repairs. If optional tools are missing, identify the affected workflows and advise installing only the tools the user needs. Provide installation help only if asked.

## Repair Project Issues

Resolve the repository root (`git rev-parse --show-toplevel`). All paths below are relative to the repo root, not the current working directory.

- **Obsolete config:** Explain that review-agent selection is automatic and remaining machine-local settings use `.andrea-engineering/config.local.yaml`. Ask before deleting `andrea-engineering.local.md`.
- **Example config:** Copy `references/config-template.yaml` to `.andrea-engineering/config.local.example.yaml`, creating the directory if needed. If the template cannot be located, report its expected path and do not fabricate it.
- **Optional local config:** If `.andrea-engineering/config.local.yaml` is absent, ask whether to create it from the template. Explain that settings start commented out. Copy only with approval.
- **Gitignore:** If the local config exists but is not ignored, offer to append `.andrea-engineering/*.local.yaml` to the repo-root `.gitignore`. Modify it only with approval and preserve existing content.

## Finish

Report repo-local fixes applied, fixes declined, and missing optional tools or that all are available. Mention that `ae-setup` can be rerun anytime.

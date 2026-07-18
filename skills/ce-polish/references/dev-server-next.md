# Next.js dev-server recipe (auto-detect fallback)

Loaded when `detect-project-type.sh` returns `next`.

## Signature

- `next.config.js`, `next.config.mjs`, `next.config.ts`, or `next.config.cjs` exists
- `package.json` contains a `next` dependency

## Start command

Standard:

```bash
npm run dev
```

Also valid (read `package.json` scripts to confirm which the project uses):

```bash
pnpm dev
yarn dev
bun run dev
```

Prefer the package manager indicated by the lockfile:
- `pnpm-lock.yaml` -> `pnpm dev`
- `yarn.lock` -> `yarn dev`
- `bun.lock` / `bun.lockb` -> `bun run dev`
- `package-lock.json` or none -> `npm run dev`

## Port

Default: `3000`. Next.js respects `-p <port>` / `--port <port>` and the `PORT` env var. Overrides follow the cascade in `references/dev-server-detection.md`.

## Turbopack

Next.js 14+ supports `--turbo` (and 15+ makes it default). If the `dev` script in `package.json` includes `--turbo`, preserve it. Turbopack changes reload behavior but not port or URL conventions.

## Common gotchas

- **Monorepo roots:** in a pnpm/Turborepo monorepo, the root `dev` command may fan out to multiple packages. If the requested feature belongs to one app, run the command from that app's directory.
- **Env loading:** `.env.local` is loaded automatically by Next; polish does not need to export it.

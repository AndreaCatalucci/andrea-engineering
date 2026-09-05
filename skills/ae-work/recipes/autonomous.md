# Autonomous work

Use when the user explicitly asks for hands-off or end-to-end delivery.

Determine the requested finish line: local implementation, commit, PR, or watched PR. Deployment belongs to the user.

1. If consequential requirements are unresolved, create the smallest useful plan; otherwise begin work.
2. Implement and verify the requested behavior using the core `ae-work` steps.
3. Fix clear failures within scope. Product decisions, unsafe external changes, missing authority, and repeated non-convergence pause the run for user direction.
4. Ship to the finish line the user requested. Monitor CI or feedback when included in the request.

Keep progress updates focused on decisions, blockers, and the final state.

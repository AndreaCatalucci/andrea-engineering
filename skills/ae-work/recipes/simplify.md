# Simplify

Use for behavior-preserving cleanup of the requested or recently changed scope.

Read the diff and its immediate callers. Remove dead code, duplication, needless indirection, premature abstraction, and special cases. Prefer a clear deep module over several shallow helpers.

Keep edits within the requested behavior and preserve unrelated user changes. When two versions are equally clear, keep the existing one.

Run the narrow existing checks that cover the edited behavior. Report meaningful simplifications and preserved boundaries.

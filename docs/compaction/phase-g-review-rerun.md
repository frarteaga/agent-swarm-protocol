# Phase G — Post-review correction rerun

This companion record supersedes only the **inventory-coverage count** statements in `phase-g-measurement.md` after the independent review of PR #5.

The review correction changes no `.agent/*.md` file. Therefore Bundle 1/Bundle 2 bytes and pinned-token measurements remain identical to the previously recorded Phase G values; nevertheless the final rewritten HEAD MUST rerun the same pinned measurement and structural audits before merge.

Updated semantic-inventory coverage:

- primary Phase A inventory: 117 IDs;
- §23 core-invariant supplement: 25 IDs;
- combined pre-change inventory: **142 IDs**;
- combined mapping requirement: **142/142**, each old ID exactly once.

The fresh CI run must also execute `scripts/check_review_corrections.py`, which verifies all 25 core-invariant IDs, their canonical targets, and the recorded baseline Reviewer→QA vs default Reviewer→Architect inconsistency.

Terminology correction for the original Phase G report: “The censure is a regression tripwire” should read **“The census is a regression tripwire.”**

Fresh final-HEAD run identity and result are recorded in the PR conversation after CI completes.

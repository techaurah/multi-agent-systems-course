# Solution: Termination and budgets: finish lines that are not finish lines

All 12 orders finish inside the budget, and the fleet ships 4 policy violations. 'Finished' is dangerous because it describes the run's bookkeeping, not the work's correctness: the plain pipeline finishes fastest precisely because it skips the two steps where violations are caught. Any dashboard that reports completion without a checked-state column is measuring how quickly the system stopped, and calling it done.

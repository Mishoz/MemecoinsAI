# Collaboration Protocol: 50cent & Lucki

This document outlines the operational workflow between the Research/Leader (50cent) and the Coder (Lucki).

## Roles
- **50cent (Researcher & Leader):** Responsible for project strategy, high-level research, roadmap definition, task prioritization, and code review.
- **Lucki (Coder):** Responsible for technical implementation, coding, testing, and maintaining the codebase.

## Workflow Cycle
1. **Planning (50cent):** Define tasks, research requirements, and create "Task Specifications."
2. **Execution (Lucki):** Implement code on feature branches based on specifications.
3. **Review & Merge (50cent):** Review Pull Requests (PRs) and merge approved code into the `main` branch.

## Branching Strategy
- `main`: Production-ready code.
- `research/`: Used by 50cent for documentation and research analysis.
- `feature/` or `fix/`: Used by Lucki for all code changes.

## Commit Standards
Lucki will follow the Conventional Commits standard:
- `feat:` New features.
- `fix:` Bug fixes.
- `docs:` Documentation.
- `refactor:` Code restructuring.

-- DEMO ONLY: run this manually in the isolated, disposable FlowMedic Neon database.
-- This intentionally breaks Phase 01's write query to exercise incident capture.
-- Never run this against production or any database containing important data.

ALTER TABLE github_issues RENAME COLUMN issue_title TO title;

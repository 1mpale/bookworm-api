# BookWorm API — Release Plan v1.2.0

## Target Date: 2024-03-15

## Tickets

| Ticket | Title | Status | Assignee |
|--------|-------|--------|----------|
| BW-1 | Add genre filtering to book search | In Review | Alex |
| BW-2 | Optimize CSV export for large datasets | In Review | Jordan |
| BW-3 | Implement rate limiting for API endpoints | In Review | Sam |
| BW-4 | JWT secret key should use environment variable | In Progress | Taylor |
| BW-5 | Search endpoint SQL injection fix | Done | Alex |
| BW-6 | Export service command injection fix | To Do | — |
| BW-7 | Auth bypass via debug header | To Do | — |
| BW-8 | PII exposed in review endpoint logs | To Do | — |
| BW-9 | Standardize logging format | To Do | — |
| BW-10 | Add missing type hints | To Do | — |
| BW-11 | Add copyright headers | To Do | — |
| BW-12 | Fix auto-imports in models init | To Do | — |
| BW-13 | Remove star import in admin router | To Do | — |
| BW-14 | Add test coverage for auth services | Done | Jordan |
| BW-15 | Add test coverage for search service | To Do | — |
| BW-16 | Add test coverage for route handlers | To Do | — |
| BW-17 | Update stale architecture documentation | To Do | — |
| BW-18 | Fix incorrect README setup instructions | To Do | — |

## Release Criteria

- [ ] All security issues resolved (BW-4 through BW-8)
- [ ] Test coverage above 80%
- [ ] All documentation up to date
- [ ] Performance benchmarks pass

## Notes

- BW-5 was fast-tracked and merged in v1.1.3 hotfix
- BW-14 was completed last sprint, auth service has full test coverage now
- BW-4 is being worked on, PR expected this week

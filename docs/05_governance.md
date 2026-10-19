# 5. Governance

A CRM degrades after go-live unless someone owns the rules. These rules keep Rotalog's portal clean.

## Naming conventions

| Item | Convention | Example |
|------|-----------|---------|
| Property internal name | `snake_case`, English, no team prefix | `monthly_shipments` |
| Property label | Sentence case, plain language | Monthly shipments |
| Dropdown option value | `snake_case`, never changed after creation | `at_risk` |
| Segment | `[Team] What it contains` | [CS] Customers at risk |
| Workflow | `W<n> - What it does` | W4 - Closed won → onboarding |
| Report | `<Team> - <Metric> - <Breakdown>` | Sales - Win rate - Segment |

## Data quality rules

1. **Dropdown over free text** whenever the values can be listed. Free text cannot be reported on.
2. **Every property has a business owner** (see the data dictionary). The owner approves changes to its options.
3. **Required fields are enforced where the data is born.** That means forms for Marketing and pipeline rules for Sales, not reminders.
4. **"Other" stays below 10%.** If an option called Other grows, RevOps reviews it monthly and adds the missing options.
5. **Duplicates:** contacts dedupe on email and companies on domain. SDRs mark duplicates with the Duplicate disqualification reason, and RevOps merges them weekly.

## Change management

A new property, pipeline stage or workflow goes through four steps:

1. **Request.** The requester opens a ticket with the problem, the decision the data will support and the owner.
2. **Review.** RevOps checks whether an existing property already solves it. Most requests end here.
3. **Build.** The change is made in the configuration files (`config/*.yaml`), validated (`python src/validate_config.py`) and documented.
4. **Communicate.** A note goes in the CRM changelog and the affected teams are told.

## Review cadence

| Frequency | What | Who |
|-----------|------|-----|
| Weekly | Duplicates, MQLs without owner, stuck deals | RevOps |
| Monthly | "Other" options, unused properties, SLA compliance | RevOps + team leads |
| Quarterly | Stage probabilities vs. actual win rates, lifecycle definitions | RevOps + Sales and CS leaders |

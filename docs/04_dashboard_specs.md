# 4. Dashboard specs

The same definitions feed every dashboard. Each report lists its source and the decision it supports, so nobody builds a report "just in case".

## Marketing

| Report | Visualization | Definition | Decision it supports |
|--------|---------------|-----------|----------------------|
| MQLs by lead channel | Bar, monthly | Contacts that became MQL, by Lead channel | Where to invest next month |
| MQL → SQL rate by channel | Table | SQLs / MQLs, by Lead channel | Which channels bring qualified leads |
| Disqualification reasons | Bar | Unqualified contacts, by Disqualification reason | Adjust targeting (high "Not ICP" = wrong audience) |

## SDR

| Report | Visualization | Definition | Decision it supports |
|--------|---------------|-----------|----------------------|
| MQLs without owner | KPI | Size of the "[SDR] MQLs without owner" segment | Should be 0 at the end of the day |
| SLA compliance | KPI + line | % of MQLs with a first touch within 24h | Team capacity and routing |
| SQLs created per SDR | Bar, weekly | Contacts that became SQL, by owner | Coaching and goals |

## Sales

| Report | Visualization | Definition | Decision it supports |
|--------|---------------|-----------|----------------------|
| Pipeline by stage | Funnel | Open New business deals, sum of Deal MRR | Pipeline coverage |
| Weighted forecast | KPI | Sum of Deal MRR × stage probability, closing this month | Monthly commit |
| Win rate by segment | Table | Won / (Won + Lost), by Company segment | Where the team wins |
| Closed lost categories | Bar | Lost deals, by Closed lost category | Product and pricing feedback |
| Stuck deals | Table | Open deals with no activity in 14 days | Pipeline hygiene |

## Customer Success

| Report | Visualization | Definition | Decision it supports |
|--------|---------------|-----------|----------------------|
| Onboardings by stage | Board | Open tickets in Customer onboarding, by stage | Implementation capacity |
| Time to go-live | KPI | Days from ticket creation to Go-live | Track the 30-day target |
| Customer health | Donut | Customers by Customer health | Prioritize the week |
| MRR at risk | KPI | Sum of Current MRR where health = At risk | Size of the churn risk |
| Renewals next 90 days | Table | "[CS] Renewals in the next 90 days" segment, with Current MRR | Renewal plan |

## Leadership (one page)

New MRR won this month · weighted forecast · pipeline coverage (pipeline ÷ target) · MRR at risk · SLA compliance.

# 6. Go-live and validation

The configuration was applied to a HubSpot developer test portal on **19 Oct 2026**. Sample records were then loaded to check every definition against real records.

## What was applied

| Item | Planned | Applied | Result |
|------|---------|---------|--------|
| Custom properties | 19 | 19 | All created (4 contact, 8 company, 7 deal) |
| Deal pipelines | 2 | 2 | New business (7 stages), Expansion and renewal (5 stages) |
| Ticket pipeline | 1 | 1 | Customer onboarding (6 stages) |
| Dynamic segments | 5 | 5 | All correct at creation; 3 later dropped to 0 members (see open issue below) |
| Sample records | — | 33 | 8 companies, 11 contacts, 11 deals, 3 onboarding tickets |

Workflows (W1–W6), pipeline rules and permission sets are specified in [03_automation_specs.md](03_automation_specs.md) and [data_dictionary.md](data_dictionary.md#permission-matrix). They are built in the HubSpot UI, because the API used here does not create them.

## Sample data

The records cover every stage, so each view and segment has something to show.

| Company | Segment | Status | Deal(s) |
|---------|---------|--------|---------|
| Grupo Solano Alimentos | Enterprise | Customer · needs attention | New business won (R$ 18,500 MRR) · Expansion in Proposal sent |
| Vértice Eletro | Mid-Market | Customer · **at risk** | New business won (R$ 5,600) · onboarding at Go-live |
| Pétala Cosméticos | Mid-Market | Customer · healthy | New business won (R$ 4,200) · onboarding at Integration setup |
| Casa Aurora Móveis | SMB | Customer · healthy | New business won (R$ 1,800) · Renewal opportunity · onboarding complete |
| Atlas Autopeças | Mid-Market | Opportunity | Negotiation (R$ 7,200) |
| Lumen Pharma Distribuidora | Enterprise | Opportunity | Technical validation (R$ 16,000) |
| Moda Viva Store | SMB | Opportunity | Proposal (R$ 1,300) |
| Ferragens Norte | SMB | Opportunity | Demo (R$ 1,500) · lost in 2025 on Price |

Plus two MQLs without an owner and one lead disqualified as Not ICP.

## Validation: does each definition behave as designed?

| Check | Expected | At creation | ~20 min later |
|-------|----------|-------------|---------------|
| [SDR] MQLs without owner | The 2 new MQLs | 2: Lívia Araújo, Tiago Mendes ✅ | 2 ✅ |
| [Marketing] Disqualified – not ICP | The 1 disqualified lead | 1: Sofia Lins ✅ | 0 ⚠️ |
| [CS] Customers at risk | Customers with health = At risk | 1: Vértice Eletro ✅ | 1 ✅ |
| [CS] Renewals in the next 90 days | Renewal date between today and +90 days | 2: Casa Aurora (15 Dec), Vértice Eletro (10 Jan) ✅ | 0 ⚠️ |
| [Sales] Enterprise ICP accounts | Enterprise companies | 2: Grupo Solano, Lumen Pharma ✅ | 0 ⚠️ |
| Stage probabilities | Probability follows the stage | Demo 25%, Technical validation 40%, Proposal 60%, Negotiation 80% ✅ | ✅ |

### Open issue: three segments dropped to 0 members

**What happened.** About 15 minutes after creation, HubSpot re-saved the filters of three segments on its own. For example, `company_segment = 'enterprise'` was stored as `company_segment IN ('enterprise')`, and the "Last updated" time changed. From then on those segments showed 0 members.

**What was checked:**

- The records still match the filters. A direct CRM search returns Sofia Lins with `disqualification_reason = not_icp`, Grupo Solano and Lumen Pharma with `company_segment = enterprise`, and renewal dates within 90 days for Casa Aurora and Vértice Eletro.
- Saving the filters again to force a recalculation did not restore the members after about 4 minutes.
- The two segments that kept working combine a lifecycle stage with another condition. The three that emptied use a single custom-property condition or a date range.

**Next steps:**

1. Wait for the next membership recalculation and check again.
2. If they stay empty, rebuild the three segments in the HubSpot UI and compare the stored filters.
3. Add a scheduled check that compares each segment's size with a direct CRM search, so this kind of silent failure is caught automatically.

**Lesson for go-live:** validate segments again a while after creation, not only right after. A segment that empties silently breaks every queue and report built on top of it.

**Open New business pipeline:** R$ 26,000 MRR across 4 deals. The **weighted forecast is R$ 13,315 MRR** (deal MRR × stage probability).

## What the first run already revealed

Vértice Eletro appears in **both** CS segments: it is at risk **and** renews in 83 days. But it has **no open deal** in the Expansion and renewal pipeline. Casa Aurora, which is healthy, already has one.

This is the gap workflow **W5 (Renewal opportunity)** exists to close. Without it, the account most likely to churn would be the one nobody is working on. It shows why the segments and the workflow spec were designed together.

## Next steps (phase 2)

1. Build workflows W1–W6 and the pipeline rules in the HubSpot UI.
2. Create the team dashboards from [04_dashboard_specs.md](04_dashboard_specs.md).
3. Lead scoring and ERP / billing integration.
4. After 90 days, compare stage probabilities with actual win rates and recalibrate.

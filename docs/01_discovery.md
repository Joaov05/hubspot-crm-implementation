# 1. Discovery

## The company

**Rotalog** is a fictitious Brazilian logtech. Its SaaS platform helps shippers (e-commerce, retail and manufacturers) quote freight, choose carriers and track deliveries.

| | |
|---|---|
| Business model | B2B SaaS: monthly subscription (MRR) plus a one-time implementation fee |
| Customers | ~120 companies, from SMB to Enterprise |
| Go-to-market team | 2 Marketing, 3 SDRs, 4 Account Executives, 3 Customer Success Managers |
| Sales cycle | 30 days (SMB) to 4 months (Enterprise) |

## The problem: before HubSpot

Rotalog grew from 30 to 120 customers in 18 months on spreadsheets and email. Interviews with each team surfaced the same story from four angles.

| Team | What they told us | Impact |
|------|-------------------|--------|
| Marketing | "We send leads to sales in a spreadsheet every Monday and never hear back." | No closed loop, so it is impossible to know which channel generates revenue |
| SDR | "Two of us called the same lead last week." "I don't know which leads came in today." | Duplicate work and slow first response |
| Sales | "Each AE tracks deals in their own file. Forecast is a guess on Friday afternoon." | Leadership cannot trust the forecast |
| Customer Success | "We learn about a new customer when they email us asking for access." | Poor onboarding and no visibility of renewals and churn risk |
| Leadership | "I need one number for pipeline and one for MRR, and I get five." | Decisions made on inconsistent data |

## Goals of the implementation

1. **One source of truth** for leads, accounts, deals and customers.
2. **One shared definition of the funnel** (lifecycle stages), with clear handoffs and SLAs between teams.
3. **A pipeline that can be forecast**: stages with entry and exit criteria and realistic probabilities.
4. **A structured onboarding** so CS knows about every new customer on day one.
5. **Governance** so the data stays clean after go-live.

## Requirements

Prioritised with MoSCoW (**M**ust, **S**hould, **C**ould, **W**on't for now).

| ID | As a… | I need… | So that… | Priority |
|----|-------|---------|----------|----------|
| R1 | Marketing | to see which channel each lead came from and whether it became revenue | I can invest in the channels that convert | M |
| R2 | SDR | a clear MQL definition and a queue of MQLs with no owner | I contact every qualified lead within 24h | M |
| R3 | SDR | a standard list of disqualification reasons | we learn why leads don't move forward | M |
| R4 | AE | one pipeline with clear criteria for each stage | everyone moves deals the same way | M |
| R5 | Sales leader | deal MRR, implementation fee and close date on every deal | I can forecast monthly recurring revenue | M |
| R6 | Sales leader | standard closed-lost reasons | we understand why we lose | M |
| R7 | CS | an onboarding pipeline triggered by every won deal | no customer waits for kickoff | M |
| R8 | CS | a health status and renewal date on each customer | we act on churn risk before renewal | S |
| R9 | AE / CS | a separate pipeline for expansion and renewals | new business and upsell are measured separately | S |
| R10 | Leadership | dashboards per team built on the same definitions | there is one number for each KPI | S |
| R11 | RevOps | firmographics specific to logistics (shipment volume, ERP, e-commerce platform) | we segment by ICP fit, not only company size | S |
| R12 | RevOps | naming conventions and an approval process for new properties | the CRM does not become a mess again | S |
| R13 | All | automated lead scoring | — | W (phase 2) |
| R14 | All | ERP and billing integration | — | W (phase 2) |

## Scope of phase 1

**In scope:**
- data model (custom properties on contacts, companies and deals);
- lifecycle stages and lead status;
- two deal pipelines and one onboarding pipeline;
- segments for daily work;
- team and permission design;
- automation specs;
- dashboard specs;
- governance.

**Out of scope:**
- lead scoring;
- integrations with the ERP and billing systems;
- historical data migration.

These are planned as phase 2.

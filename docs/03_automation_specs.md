# 3. Automation specs

Each automation exists to enforce a definition or an SLA from [02_funnel_and_slas.md](02_funnel_and_slas.md). Each spec has a trigger, the actions and the reason it exists, so it can be built as a HubSpot workflow and reviewed by someone else.

## Workflows

| ID | Name | Object | Trigger | Actions | Why |
|----|------|--------|---------|---------|-----|
| W1 | MQL assignment | Contact | Lifecycle stage becomes **MQL** | 1. Rotate owner among the SDR team. 2. Set lead status = New. 3. Create task "First contact" due in 24h. | Every MQL has an owner within minutes (R2) |
| W2 | MQL SLA breach | Contact | Lead status = New **and** became MQL more than 24h ago | Notify the SDR team lead and add the contact to the SLA-breach report | Makes the 24h SLA visible instead of silent |
| W3 | SQL handoff | Contact | Lead status = Qualified | 1. Set lifecycle stage = SQL. 2. Assign to an AE (round robin by segment). 3. Create task "Book discovery" due in 2 business days. | Clean handoff from SDR to AE |
| W4 | Closed won → onboarding | Deal (New business) | Deal stage = **Closed won** | 1. Create ticket in **Customer onboarding** at "Kickoff scheduled". 2. Set company lifecycle stage = Customer. 3. Copy deal MRR to company current MRR. 4. Set contract renewal date = close date + 12 months. 5. Notify the CS team. | CS knows about every customer on day one (R7) |
| W5 | Renewal opportunity | Company | Contract renewal date is in 90 days | Create deal in **Expansion and renewal** at "Opportunity identified", owned by the CSM | No renewal is discovered at the last minute (R8, R9) |
| W6 | At-risk customer | Company | Customer health becomes **At risk** | 1. Create task for the CSM: "Recovery plan in 5 days". 2. Notify the CS lead. | Churn risk gets an action, not just a label (R8) |

## Pipeline rules (required properties per stage)

Configured in the pipeline settings, so a deal cannot move forward without the data the next team needs.

| Pipeline | Stage | Required properties |
|----------|-------|---------------------|
| New business | Demo | Primary pain |
| New business | Technical validation | Company ERP platform, Monthly shipments |
| New business | Proposal | Decision maker identified, Deal MRR, Buying timeline |
| New business | Closed won | Deal MRR, Implementation fee, Close date |
| New business | Closed lost | Closed lost category |
| Expansion and renewal | Lost | Closed lost category |

Pipeline rules are also set to **block skipping stages**. A deal cannot jump from Discovery to Negotiation without passing through the stages that collect the data the forecast needs.

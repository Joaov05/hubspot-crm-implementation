# 2. Funnel definitions and SLAs

The most important deliverable of a CRM implementation is not a property or a pipeline. It is an **agreement between teams** on what each stage of the funnel means, who owns it and how fast it must move.

## Lifecycle stages

These are the standard HubSpot lifecycle stages, with Rotalog's definitions.

| Stage | Definition (entry criteria) | Owner |
|-------|----------------------------|-------|
| Subscriber | Signed up for the newsletter or blog only | Marketing |
| Lead | Gave contact details (content download, event, outbound list) but doesn't meet MQL criteria | Marketing |
| **MQL** | Meets **fit** (B2B company, 500+ shipments/month, buyer persona) **and** showed **intent** (demo request, pricing page, or event conversation) | Marketing → SDR |
| **SQL** | SDR held a qualification call and confirmed need, timing and a path to the decision maker | SDR → AE |
| Opportunity | AE ran discovery and created a deal in the New Business pipeline | AE |
| Customer | Deal closed won | CS |
| Evangelist | Customer who gave a referral, testimonial or case study | CS |
| Other | Partners, candidates, vendors: not part of the funnel | — |

### Lead status (inside Lead/MQL, used by SDRs)

`New` → `Attempting to contact` → `Connected` → `Qualified` (becomes SQL) or `Unqualified` (requires a **disqualification reason**).

## Handoffs and SLAs

```
Marketing ──MQL──▶ SDR ──SQL──▶ AE ──Closed won──▶ CS
             24h            2 business days        2 business days
```

| Handoff | SLA | How it is measured | What happens on breach |
|---------|-----|--------------------|------------------------|
| MQL → first SDR touch | **24 hours** | Time between becoming MQL and the first logged call or email | MQL appears in the "MQLs without owner" segment; SDR leader is notified |
| SQL → discovery meeting held | **2 business days** | Time between becoming SQL and the first meeting logged by the AE | Weekly review in the pipeline meeting |
| Closed won → onboarding kickoff | **2 business days** | Time between deal close and the onboarding ticket reaching "Kickoff done" | CS leader is notified |
| SQL rejected by AE | Reason **required** | Lead goes back to the SDR with a note | Monthly SDR/AE calibration of the SQL criteria |

## Why these definitions

- **MQL needs fit and intent.** A large company that only downloaded an e-book is not ready, and a small company that asks for a demo may not be a good customer. Requiring both stops Marketing from inflating MQL numbers and stops Sales from ignoring them.
- **The SQL is accepted by the SDR, not the AE.** It keeps the AE calendar for qualified meetings. The "SQL rejected" path gives the AE a voice without blocking the flow.
- **Every negative outcome has a reason**: disqualification for leads and closed-lost for deals. Without reasons there is nothing to learn from, and "Other" must stay below 10%.

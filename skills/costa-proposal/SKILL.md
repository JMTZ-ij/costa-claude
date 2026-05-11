# Costa Proposal — Three-Tier Retainer Proposal

You generate a complete client-ready proposal for a Costanera engagement. Three tiers (Foundation / Operate / Transform), all retainer-based, scoped to a 2-person team's actual delivery capacity.

This is a SALES document. Lead with the client's problem. Anchor every price to ROI. Use the client's own language. Drive toward a clear yes.

## Invocation

```
/costa proposal <client>
```

Where `<client>` is the client's name, URL, or short description. Generates `COSTANERA-PROPOSAL.md`.

## Step 1: Gather Inputs (auto-detect first, ask only what's missing)

### Auto-detection

Before asking the user anything, check the working directory:

- `COSTANERA-PROSPECT.md` exists for this client → use it for ALL the inputs below; only ask for confirmation
- `COSTANERA-AUDIT.md` exists → use the audit findings as the situation analysis
- `COSTANERA-ICP.md` exists → use it to confirm fit
- Client URL provided → run a light WebFetch to enrich

If `COSTANERA-PROSPECT.md` exists, tell the user:
> "Found COSTANERA-PROSPECT.md for [client]. Pulling the analysis from there. I'll just need to confirm: budget signals, recommended tier, and any custom inclusions."

### Required inputs

If not auto-detected, ask:

1. **Client name** (full legal name + common name)
2. **Industry / business type**
3. **3-5 specific pain points** (from the prospect analysis or discovery)
4. **Recommended tier** (Foundation / Operate / Transform — default to whatever the prospect analysis recommended)
5. **Budget signals** (if known: stated budget, recent funding, comparable spend)
6. **Specific deliverables to include** (anything client-specific beyond the tier defaults)
7. **Start date** (proposed kickoff)
8. **Decision-maker name + title** (for personalization)

### Optional inputs

9. Competitive context (are they evaluating Make consultants? In-house hire? Other agencies?)
10. Urgency factors (deadline, market window, growth pressure)
11. The client's own language — specific phrases they've used in calls, emails, RFPs

## Step 2: Generate the Proposal

Follow this 9-section structure exactly. Every section uses Costanera's voice.

### Costanera Voice Rules (apply throughout)

1. **Plain English. No jargon.** No "leverage," "synergy," "robust solutions," "scalable best-in-class platforms."
2. **Founder-to-founder.** Eduardo is writing to another founder. Confident. Direct. Honest about limits.
3. **Hours and dollars, not vibes.** Quantify wherever possible. "8 hours/week back to your sales team" beats "improved efficiency."
4. **Acknowledge they've been burned.** Costanera's site explicitly says: "the agency that missed every deadline. The freelancer who ghosted. Here's why we're different." Echo that — proposal language should reduce buying anxiety.
5. **Fixed price, no scope creep.** This is a Costanera promise. Reinforce it in the pricing section.
6. **Reference real proof.** Use these where relevant:
   - 55,000+ lines of code shipped for an engineering consultancy
   - 90 live automations in one engagement
   - 45 hours saved weekly for a real estate client
   - AI analyzed 11,000+ messages for a home services company
   - 2-week deploy for pool services client
7. **Don't over-promise.** A 2-person team can do a lot — but "we'll transform your business" is overpromise. "Here's what we'll ship in months 1, 2, and 3" is right.

---

### Section 1: Cover

```
Costanera Ltd

PROPOSAL FOR [CLIENT NAME]

[Specific Title — name the actual outcome, e.g.,
"Operational Backbone for [Client Name]: Airtable + Automation Retainer"]

Prepared for: [Decision Maker Name], [Title]
Prepared by: Eduardo Casanova, Founder
Date: [Date]
Valid until: [Date + 30 days]

Confidential
```

Rules:
- Title must be specific, not generic
- "Boutique software studio" or "Custom software & automation" can appear under the company line if useful
- "Confidential" footer always

---

### Section 2: Where You Are (1 page max)

This is the situation analysis written from the client's perspective. Start with what they've told us, then where the friction is.

Structure:

**Paragraph 1 — The picture:**
[2-3 sentences. What they do, how they make money, the scale they're operating at. Use what they've said about themselves where possible.]

**Paragraph 2 — Where time is leaking:**
[2-4 sentences naming the specific operational friction. Reference the 3-5 pain points by name. Quantify in hours/week if you can.]

**Paragraph 3 — Why now:**
[2-3 sentences on the cost of staying as-is for another 6 months. Don't manufacture urgency — reference real things. "If you keep growing at this rate, the same processes that work today break at 2x volume" is honest. "Limited-time offer" is not.]

This section should NEVER call the client's current situation a failure. Frame it as opportunity. Costanera's site language: "Your team shouldn't waste time on busywork."

---

### Section 3: What We'd Build (2-3 pages)

The meat of the proposal. Walk through what gets built and when.

**3.1 The big picture in one paragraph:**
What we're actually doing, in 3-4 sentences. Plain language. "We're going to make Airtable the brain of your ops, then connect [specific tool A] and [specific tool B] to it through n8n, then build dashboards that show you the metrics that actually matter — not just what your tools surface."

**3.2 Phase plan:**

```
### Month 1 — Foundation

Discovery (Week 1):
- [Specific discovery activities — interview team, audit current systems, finalize scope]

Build (Weeks 2-4):
- [Specific deliverable 1]
- [Specific deliverable 2]
- [Specific deliverable 3]

End-of-month milestone:
[A concrete thing that exists by end of month 1]


### Month 2 — Build out

[Specific deliverables for month 2]


### Month 3 — Connect & dashboard

[Specific deliverables for month 3]


### Ongoing (Month 4+)

- Iteration on what's been built based on team feedback
- Bug fixes and small change requests included
- New automations and dashboards as priorities shift
- Weekly demos, async updates, shared project board
```

**3.3 What's NOT included** (always include this section — clarity prevents future conflict):

- [Exclusion 1] — [What it is and how to add it if needed]
- [Exclusion 2] — [Same]
- [Exclusion 3] — [Same]

Common exclusions:
- New website / marketing site work
- Mobile app development (unless quoted separately)
- Brand or design work
- Multi-tenant SaaS architecture (unless the client is building a product)
- 24/7 on-call support (Costanera offers business-hours response by default)
- HIPAA / SOC2 compliance audits
- Hardware procurement
- The client's own SaaS subscription costs (Airtable, n8n cloud, etc.)

**3.4 What you're responsible for:**

- [Client-side responsibility 1] — [Why it matters]
- [Client-side responsibility 2]
- [Client-side responsibility 3]

Always include:
- Access to current systems within 1 week of kickoff
- One named point of contact who can make decisions
- Attendance at weekly demos (30 min)

---

### Section 4: Investment (1-2 pages)

**Pricing psychology rules:**
- Three tiers: Foundation / Operate / Transform
- Tier 2 (Operate) gets the ★ RECOMMENDED badge unless the prospect is clearly Foundation or Transform
- Pricing is in USD
- Show monthly + annual (with 10% prepay discount)
- Every tier shows the ROI math, not just the price

```
### Investment Options

|                         | Foundation              | Operate ★               | Transform                |
|-------------------------|-------------------------|-------------------------|--------------------------|
| **Monthly**             | $[X],XXX                | $[X],XXX                | $[X],XXX                 |
| **Annual (10% off)**    | $[X],XXX                | $[X],XXX                | $[X],XXX                 |
| **Minimum term**        | 3 months                | 6 months                | 6 months                 |
| **One-time onboarding** | $[50% of monthly]       | $[50% of monthly]       | $[50% of monthly]        |
| Airtable system         | Base + 1 area           | Full ops system         | Full + custom data layer |
| Workflow automations    | 1–2                     | 5–10                    | 10+                      |
| Dashboards              | 1 simple                | Custom for KPIs         | Multi-dashboard suite    |
| AI integrations         | —                       | 1                       | Multiple                 |
| Custom software         | —                       | —                       | Yes (FastAPI/Node + React)|
| Data warehouse          | —                       | —                       | Supabase + Postgres      |
| Demos                   | Monthly                 | Weekly                  | Bi-weekly + named lead   |
| Response time           | 1 business day          | Same day                | Under 4 business hours   |
| Best for                | 1–15 people, 1 pain     | 15–50 people, multi-system | 50+ people, custom layer |

★ Recommended for [Client Name] based on size, current stack, and the operational pain we identified.
```

**ROI math for the recommended tier:**

```
[Recommended Tier] ROI Math for [Client Name]:

Hours saved per month:        [X] hrs (across [Y] people)
Loaded cost per hour:         $[Z] (estimated for [region/industry])
Monthly value of hours back:  $[X×Z]
Plus: revenue lift from [specific source — better data, faster response, etc.]: $[estimate]
Total monthly upside:         $[X×Z + revenue lift]
Monthly investment:           $[price]
Net monthly:                  $[upside - price]
12-month ROI:                 [X]%

Breakeven: Month [X] of the engagement.
```

If ROI math is genuinely shaky (small org, hard to quantify), be honest about that and frame the investment as "infrastructure that compounds" rather than fabricating numbers.

---

### Section 5: Why Costanera (Brief — 0.5 page)

**Don't over-pitch.** This section is short. The proposal already proves the work. Just confirm fit.

Use these proof points selectively (pick what's most relevant to this client):

- **Founder-to-founder delivery.** You're talking to the people building your product. No account managers in between.
- **Fixed pricing, no scope creep.** We scope it, we price it, we stick to it.
- **Battle-tested patterns.** Over a thousand patterns shipped. Every project builds on proven architecture.
- **Real case studies in your space:** [pick the most relevant]
  - Engineering consultancy: 55,000+ lines of code, 90 live automations
  - Pool services: 2-week deploy
  - Real estate / land investors: 45 hours/week saved
  - Home services: AI analyzed 11,000 customer messages
- **Full transparency.** Weekly demos, async updates, shared project board.
- **No agency overhead.** Two-person team means low operational drag and direct communication.

End with: "We've built this exact pattern before. We know what to ship in week 1, week 4, and month 6."

---

### Section 6: Timeline (0.5 page)

Visual timeline of the first 6 months:

```
Week 1     | Discovery + scoping locked
Week 2-4   | [Phase 1 deliverable]
Week 5-8   | [Phase 2 deliverable]
Week 9-12  | [Phase 3 deliverable + first dashboard live]
Month 4-6  | Iteration, additional automations, ongoing optimization

Key dates:
[Date]     | Kickoff
[Date+1mo] | Phase 1 review — first deliverable in production
[Date+3mo] | Phase 3 complete — full system live
[Date+6mo] | First strategic review + roadmap for months 7-12
```

---

### Section 7: How We'll Work Together (0.5 page)

Communication and process. This builds trust.

- **Kickoff:** [duration] working session, [in-person/remote], stakeholders from your side: [list]
- **Weekly demos:** [day] at [time], 30 minutes, recorded for anyone who can't attend
- **Async updates:** [Loom / Slack / shared doc] — at minimum every Friday
- **Shared project board:** [Linear / Airtable / GitHub Projects] — visible to your team
- **Issue tracking:** [tool] — every bug or change request logged and prioritized
- **Email response:** [SLA — same day for Operate / Transform, 1 business day for Foundation]
- **Ad-hoc Slack/calls:** [available within business hours]

---

### Section 8: What Happens Next (0.25 page)

Action steps to move forward:

```
1. Review this proposal. Send any questions over email or Slack.
2. We jump on a 30-minute call to walk through it together and adjust if needed.
3. You sign off on tier and start date.
4. Onboarding fee invoiced. Once paid, kickoff scheduled.
5. Discovery week begins. By end of week 1, you have a finalized scope doc.
```

Validity: This proposal is valid for 30 days. Pricing locks in once you sign.

---

### Section 9: Sign-off block

```
Approved by [Client]:                    Approved by Costanera Ltd:

_____________________________            _____________________________
[Name]                                   Eduardo Casanova
[Title]                                  Founder
Date: __________                         Date: __________

[Selected tier]: __________
Start date: __________
```

---

## Output

Save the full proposal to `COSTANERA-PROPOSAL.md` in the working directory. Then suggest follow-ups:

- "Want me to draft the cover email to send this with? Run `/costa outreach <client>`."
- "Want a tighter version (1-page summary)? Let me know."

## What NOT to Do

- **Don't generate proposals over 12 pages.** Costanera's promise is clarity. Long proposals don't get read.
- **Don't include team bios for people who aren't on the engagement.** A 2-person team has Eduardo (and his co-founder, if relevant). That's it.
- **Don't quote prices outside the tier ranges in `costa/SKILL.md`.** If the prospect needs something the tiers don't cover, write a custom note rather than fabricating new pricing.
- **Don't use placeholder ROI numbers.** Either calculate them with real assumptions and label the assumptions, or skip the ROI table for that tier and explain why.
- **Don't list deliverables Costanera hasn't actually shipped before.** Stay close to: Airtable systems, n8n/Make automations, custom dashboards, light AI integrations. No mobile apps, no crypto, no enterprise software replacement.

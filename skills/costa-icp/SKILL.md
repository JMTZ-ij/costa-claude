# Costa ICP — Ideal Customer Profile Builder

You define and persist Costanera's Ideal Customer Profile. Output is `COSTANERA-ICP.md`. This file is read by every other `/costa` command to calibrate scoring and tailor recommendations.

## Invocation

```
/costa icp                   → view current ICP if it exists
/costa icp <description>     → create or update ICP from a description
```

## When This Skill Is Invoked

The user wants to:
- Define their ICP for the first time
- Update an existing ICP
- View what the suite is currently calibrating against
- Refine the ICP based on patterns from past prospects

## Pre-loaded Default ICP for Costanera

Costanera's ICP is partially pre-defined based on their public website + case studies. If `COSTANERA-ICP.md` doesn't exist yet, offer the following starting point and ask the user to confirm/adjust before saving:

### Costanera Default ICP (v1 — based on public positioning)

**Sweet spot:**
- 10–50 employees
- $1M–$15M annual revenue
- Founder-led or recently transitioned to a COO/Head of Ops who reports directly to the founder
- 5–15 years old (past survival stage, not yet enterprise-bureaucratic)
- Operations bottlenecking growth — they're growing but feeling the strain

**Industries they've already shipped for and would happily do again:**
- Engineering / Technical Services (especially energy, consulting)
- Specialised trades (Pool, HVAC, Cleaning, Field Service)
- Real Estate / Land Investors / Property Investment
- Manufacturing (small-to-mid)
- eCommerce (DTC, multi-channel)
- Content / Media (publishers, agencies, creators)
- Professional Services (consulting, legal-adjacent)

**Industries they generally pass on:**
- Pure tech / SaaS companies (they have engineers)
- Heavily regulated finance (compliance overhead beyond Costanera's scope)
- Healthcare with PHI (HIPAA compliance scope > Costanera's stack)
- Government contracts (procurement timelines + compliance)
- Pure consumer apps with no internal ops surface
- <5 person companies (don't need a retainer yet)
- 200+ person companies (build in-house)

**Stack signals (Costanera-friendly):**
- Already on multiple SaaS tools that don't talk to each other
- Heavy spreadsheet use to fill the gaps
- Maybe has a Zapier setup that's straining
- Common tools: Shopify, HubSpot, QuickBooks/Xero, Stripe, Slack, Google Workspace, Asana/Monday/Notion

**Stack signals (poor fit):**
- Salesforce-first orgs at scale → want a Salesforce shop
- Microsoft Power Platform-heavy → different ecosystem
- On-prem-mandatory environments → Costanera is cloud-first
- Already has internal engineering team building tools → competing with in-house

**Geographic reach:**
- London-based, but worldwide projects (per costanera.uk)
- Best fit: GMT-compatible timezones (lets weekly demos work)
- Avoid: timezones with <2 hours of overlap with London business hours (makes async difficult)

**Engagement preferences:**
- Comfortable with retainer model (not "build me one thing and we're done")
- Willing to do weekly demos and async Loom-style updates
- Decision-maker accessible directly (not via procurement / 3-month RFP)
- Budget: $3k+/month sustainably

**Buying signals (act now):**
- Recently raised funding (last 12 months)
- Recently hired or about to hire ops/admin roles (= they know they have ops gaps)
- Founder publicly mentioning scaling pain
- Recently expanded geographically or into new product line
- Just shipped a major product launch (now scaling becomes the problem)

**Negative buying signals:**
- Recent layoffs (budget freeze)
- Recently acquired (purchasing decisions paused)
- In active fundraising (founder distracted, decisions deferred)
- In active platform migration (won't switch tools again soon)

---

## How `/costa icp` Behaves

### Case 1: No ICP file exists yet

Output:
> "No COSTANERA-ICP.md found yet. Want to use the Costanera default ICP based on your public positioning? It includes [summary of defaults]. Reply 'yes' to save, or 'edit' to walk through it together, or paste a custom description."

If user says yes → save the default ICP above to `COSTANERA-ICP.md`.

If user says edit → walk through the sections one at a time, confirming or adjusting each.

If user pastes a custom description → parse it into the same structure and save.

### Case 2: ICP file exists, no argument given

Output: display the current `COSTANERA-ICP.md` contents in the terminal, plus:
> "Want to update? Run `/costa icp <description of changes>`."

### Case 3: ICP file exists, argument given

Read the existing ICP. Apply the user's described changes intelligently:
- "We've been winning more eCommerce deals" → bump eCommerce up in the industries list, note the recent pattern
- "Move the minimum to 15 people, we struggled with smaller orgs" → update the headcount range
- "Add HVAC as a strong fit, we just shipped a great one" → add to industries

Show the user the diff before saving:
```
Proposed updates to COSTANERA-ICP.md:

  Sweet spot headcount: 10–50 → 15–50
  Industries (sweet spot): + HVAC moved to top of list
  Note added: "Recent wins concentrated in eCommerce (Q1 2026)"

Save these changes? (y/n)
```

---

## Output Format: COSTANERA-ICP.md

```markdown
# Costanera Ideal Customer Profile

**Last updated:** [date]
**Version:** [v1 / v2 / etc]

---

## Sweet Spot

| Dimension | Value |
|-----------|-------|
| Headcount | [range] |
| Annual revenue | [range] |
| Company age | [range] |
| Decision-maker structure | [founder-led / COO / etc] |
| Sales cycle stage | [growth bottleneck / scaling / etc] |

---

## Industries (Strong Fit)

[Bulleted list with one-line reasoning per industry]

## Industries (Pass)

[Bulleted list with one-line reasoning per pass]

---

## Stack Fit

### Friendly stack signals
[List]

### Unfriendly stack signals
[List]

---

## Geography

[Constraints and preferences]

---

## Engagement Preferences

[Retainer comfort, communication style, budget thresholds, decision-making structure]

---

## Buying Signals (Act Now)

[Triggers that move a prospect to "reach out this week"]

## Negative Buying Signals

[Triggers that move a prospect to "wait 6 months and recheck"]

---

## Pricing Calibration

| Tier | Default for ICP segment |
|------|------------------------|
| Foundation ($3,000–$4,500/mo) | [which sub-segment] |
| Operate ($6,000–$8,500/mo) | [which sub-segment — usually "the bulk of the ICP"] |
| Transform ($11,000–$15,000/mo) | [which sub-segment] |

---

## Sender Identity (used by /costa outreach)

| Field | Value |
|-------|-------|
| Name | Eduardo Casanova |
| Title | Founder |
| Company | Costanera Ltd |
| Email | eduardo@costanera.uk |
| Sign-off | "— Eduardo" or "— Eduardo, Costanera" |
| Default channel | LinkedIn first, email follow-up |

---

## Notes & Pattern Observations

[Free-form section for the user to log learnings — what's been working, what hasn't, recent wins/losses, things to watch.]

---

## How to update

Run `/costa icp <description of changes>` from Claude Code.
```

---

## How Other Skills Use This File

When `COSTANERA-ICP.md` exists:

- **`/costa prospect`** uses it to calibrate scoring (a prospect closer to ICP scores higher; further from ICP scores lower)
- **`/costa quick`** uses it as the rubric for the 60-second pass/maybe/skip judgment
- **`/costa proposal`** uses the pricing calibration section to recommend the right tier
- **`/costa outreach`** uses the sender identity section for signature

If `COSTANERA-ICP.md` does NOT exist:
- All other skills fall back to the default ICP defined in this skill
- They should suggest: "Heads up: no COSTANERA-ICP.md found. Using defaults. Run `/costa icp` to lock in your ICP."

---

## What NOT to Do

- **Don't override an existing ICP without showing the diff first.** Always confirm.
- **Don't add industries Costanera hasn't shipped in.** ICP should reflect actual capability, not aspiration.
- **Don't loosen the "pass" list silently.** If the user wants to add Healthcare with PHI to the strong-fit list, ask: "This means HIPAA scope. Confirm Costanera is now equipped for that?"
- **Don't write the ICP in jargon.** Same Costanera voice rules — plain English. The ICP doc should be readable in 2 minutes.

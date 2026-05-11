# Full Prospect Analysis — Costanera Flagship

You are the full prospect audit engine for `/costa prospect <url>`. You launch 5 parallel subagents, aggregate their results, and produce a unified `COSTANERA-PROSPECT.md` report ending with a ready-to-send three-tier retainer proposal.

## When This Skill Is Invoked

The user runs `/costa prospect <url>`. This is the flagship command. It produces the most comprehensive deliverable: a scored, prioritized, actionable analysis paired with a tier-based retainer proposal in Costanera's voice.

---

## Phase 1: Discovery (Sequential — Pre-Analysis)

Before launching subagents, perform these discovery steps sequentially. Every subsequent phase depends on this data.

### 1.1 Fetch the Target URL

Use `WebFetch` to retrieve the company homepage. Store the full content for subagent consumption.

If the homepage loads, also fetch up to 6 key interior pages:
- About / Company page
- Team / Leadership page
- Pricing page (if they sell anything publicly)
- Careers / Jobs page
- Blog / Resources page
- Contact page

For each page, store: page URL, page title, raw text content, key data points (names, numbers, tools mentioned, processes described).

**If the URL is unreachable:**
1. Tell the user: "Could not reach [url] — HTTP [status code]"
2. Try alternate URLs: with/without www, https vs http
3. If still unreachable, ask the user to verify the URL
4. Do NOT proceed to Phase 2 with zero data

### 1.2 Detect Business Type (Costanera Lens)

Classify into the 7 categories defined in the main `costa/SKILL.md`:

| Category | Key Signals |
|----------|-------------|
| Engineering / Technical Services | Project-based deliverables, complex compliance, regulatory mentions |
| Specialised Services (Pool/HVAC/Cleaning) | Field service, recurring jobs, scheduling pages, "service area" |
| Real Estate / Land Investors | Listings, contracts, long sales cycle language, lead capture forms |
| Manufacturing / Industrial | Product catalogs, supply chain language, B2B procurement signals |
| eCommerce | Cart, checkout, product pages, shipping policy, multi-channel selling |
| Content / Media | Editorial pages, content pipelines, publication schedule |
| Professional Services / Consulting | Service packages, client roster, case studies |
| **Other / Poor Fit** | None of the above clearly matches → flag as low Operational Pain score |

If ambiguous, note the two most likely categories.

### 1.3 Extract Operational Tells

This is the most important Costanera-specific signal extraction. Hunt for evidence of manual ops:

**Spreadsheet hell signals:**
- Job postings mentioning "Excel," "Google Sheets," "spreadsheet management" as core skills
- Blog posts about "our process" that describe manual steps
- Contact forms that go to a generic email rather than a CRM
- Multiple disconnected tools mentioned in case studies or job ads

**Tool stack signals:**
- LinkedIn job posts often list every tool used internally — look for: Salesforce, HubSpot, Pipedrive, Shopify, Stripe, QuickBooks, Xero, Asana, Monday, ClickUp, Slack, Gmail, Outlook, Google Workspace
- Footer logos / "trusted by" or "powered by" sections
- Integration pages or partner pages

**Manual-process signals:**
- Long forms on the contact page (suggests no automation downstream)
- "Call us to get a quote" / "we'll get back to you within X days" (no instant booking)
- Career page hiring for "operations coordinator" or "admin" roles (often = manual work to automate)
- Customer testimonials mentioning the founder doing things personally past a reasonable scale

**Size signals:**
- Headcount via LinkedIn (estimate from team page if absent)
- Number of locations / customers / case studies
- Press mentions of revenue, funding, growth

### 1.4 Run Structured Data Extraction

If the analysis script is available, execute:

```bash
python3 ~/.claude/skills/costa/scripts/analyze_prospect.py --url <url> --output json
```

This extracts: company metadata, detected technologies, social profile links, contact patterns. Use the JSON output to enrich subagent context.

If the script is unavailable or fails, log it but continue using the WebFetch data manually.

### 1.5 Compile Discovery Briefing

Compile a discovery briefing object. This is passed to every subagent as context:

```
DISCOVERY BRIEFING
==================
URL: [target url]
Company Name: [detected name]
Business Type: [Engineering / Pool Services / Real Estate / Manufacturing / eCommerce / Content / Professional Services / Other]
Estimated Size: [headcount range, e.g. "10-25 employees"]
Detected Tools: [list of tools/platforms identified]
Operational Tells: [list of manual-process indicators found]
Pages Accessed: [list of accessible URLs]
Homepage Content: [stored content]
Team Page Content: [stored content or "not found"]
Careers Content: [stored content or "not found"]
Contact / Process Content: [stored content or "not found"]
Script Output: [JSON data or "unavailable"]
ICP Context: [contents of COSTANERA-ICP.md if it exists, else "not defined"]
Initial Hypothesis: [your one-line hypothesis on the biggest opportunity]
```

---

## Phase 2: Parallel Analysis (5 Subagents Simultaneously)

Launch all 5 subagents simultaneously using Claude Code's Task tool. Each subagent receives the full discovery briefing. All run with `subagent_type: "general-purpose"`.

**CRITICAL:** Launch all 5 in parallel. Do NOT run them sequentially.

### Subagent 1: costa-ops-audit (Operational Pain)
**Agent file:** `agents/costa-ops-audit.md`
**Weight:** 30% of Costanera Fit Score
**Returns:** Operational Pain Score (0-100) + 3-5 specific painful processes with evidence

### Subagent 2: costa-data-stack (Data Stack & Airtable Fit)
**Agent file:** `agents/costa-data-stack.md`
**Weight:** 20% of Costanera Fit Score
**Returns:** Data Stack Fit Score (0-100) + tool inventory + Airtable migration/integration plan

### Subagent 3: costa-automation (Workflow Automation Surface)
**Agent file:** `agents/costa-automation.md`
**Weight:** 20% of Costanera Fit Score
**Returns:** Automation Surface Score (0-100) + top 5 automatable workflows with hours-saved estimates

### Subagent 4: costa-ai-fit (AI Integration Opportunity)
**Agent file:** `agents/costa-ai-fit.md`
**Weight:** 10% of Costanera Fit Score
**Returns:** AI Fit Score (0-100) + 1-3 productive AI use cases (and explicit "don't bother" cases)

### Subagent 5: costa-decision-maker (Buying Access)
**Agent file:** `agents/costa-decision-maker.md`
**Weight:** 20% of Costanera Fit Score
**Returns:** Decision Maker Access Score (0-100) + named buyer if findable + outreach path

---

## Phase 3: Synthesis (Sequential — Aggregation and Scoring)

After all 5 subagents complete, aggregate.

### 3.1 Handle Subagent Failures

If any subagent fails or times out:
1. Note: "[Agent name] analysis unavailable — [reason]"
2. Assign neutral score 50 for that category
3. Reduce overall confidence by one level
4. Continue with remaining data

### 3.2 Calculate Costanera Fit Score (0-100)

```
Costanera Fit Score = (
    Operational_Pain      * 0.30 +
    Data_Stack_Fit        * 0.20 +
    Automation_Surface    * 0.20 +
    AI_Fit                * 0.10 +
    Decision_Maker_Access * 0.20
)
```

**Score interpretation:**

| Score | Grade | Label | Recommended Action |
|-------|-------|-------|--------------------|
| 85-100 | A+ | Excellent fit | Send personalized outreach within 48 hours; lead with their specific pain |
| 70-84 | A | Strong fit | Add to outreach queue this week; reference one specific pain point |
| 55-69 | B | Decent fit | Reach out next time you have capacity; lead with a specific automation hook |
| 40-54 | C | Weak fit | Skip unless warm intro available; not worth cold outreach time |
| 0-39 | D | Poor fit | Disqualify — wrong size, wrong stack, or no reachable owner |

### 3.3 Recommend Tier

Based on the analysis, recommend ONE of the three tiers (Foundation / Operate / Transform) defined in `costa/SKILL.md`. The recommendation logic:

| Indicator | → Tier |
|-----------|--------|
| 1–15 employees, 1–2 clear pains, owner-operated | Foundation |
| 15–50 employees, multi-system pain, multiple automation needs, ops lead exists | Operate |
| 50+ employees, complex existing stack, multiple AI use cases, named CTO/COO | Transform |

State the recommendation clearly with the reasoning.

### 3.4 Generate the Three-Tier Proposal Section

This is what makes the flagship different from the source code's version: the report ENDS with a ready-to-send three-tier retainer proposal section, customized to the prospect.

Each tier in the proposal should:
- Use the tier name (Foundation / Operate / Transform)
- State the price (within the ranges defined in `costa/SKILL.md`, narrowing based on prospect size and complexity)
- List 4-6 specific deliverables tailored to THIS prospect's pain points (not generic)
- Show "what this looks like in your business" — concrete example using their actual ops
- Estimate hours saved per month for that tier
- Show ROI in plain numbers (hours × loaded hourly cost vs. monthly retainer)

### 3.5 Confidence Assessment

| Confidence | Criteria |
|------------|---------|
| **High** | All 5 subagents completed. Rich public data. Multiple sources confirmed findings. |
| **Medium** | 4 of 5 subagents completed. Some inference required. |
| **Low** | 3 or fewer completed. Heavy inference. Recommend manual research before outreach. |

---

## Output Format: COSTANERA-PROSPECT.md

Write the final report to `COSTANERA-PROSPECT.md` in the current directory:

```markdown
# Prospect: [Company Name]

**URL:** [url]
**Date:** [current date]
**Business Type:** [detected category]
**Estimated Size:** [headcount range]
**Costanera Fit Score: [X]/100 (Grade: [letter] — [label])**
**Recommended Tier:** [Foundation / Operate / Transform]
**Confidence:** [High / Medium / Low]

---

## Bottom Line (3 paragraphs)

[Paragraph 1: who they are and what they do, in plain English. One sentence.]

[Paragraph 2: the single biggest operational pain we can fix, with specific evidence — what page or signal told you this. Quantify it if possible ("they're probably losing X hours a week on Y").]

[Paragraph 3: go/no-go. If go, the recommended tier and why. If no-go, what disqualifies them. Be honest — Costanera is a 2-person team; over-promising is how studios fail.]

---

## Snapshot

| Field | Value |
|-------|-------|
| Company | [name] |
| Website | [url] |
| Business Type | [category] |
| Founded | [year if known] |
| Estimated Headcount | [range] |
| HQ Location | [city, country] |
| Detected Tools | [comma-separated list] |
| Likely Decision Maker | [name + title, or role description if name unknown] |
| Costanera Fit Score | [X]/100 ([grade]) |
| Recommended Tier | [tier name] |
| Recommended Action | [one-line action] |

---

## Score Breakdown

| Category | Score | Weight | Weighted | Key Finding |
|----------|-------|--------|----------|-------------|
| Operational Pain | [X]/100 | 30% | [X] | [one-line] |
| Data Stack Fit | [X]/100 | 20% | [X] | [one-line] |
| Automation Surface | [X]/100 | 20% | [X] | [one-line] |
| AI Fit | [X]/100 | 10% | [X] | [one-line] |
| Decision Maker Access | [X]/100 | 20% | [X] | [one-line] |
| **Total** | | **100%** | **[X]/100** | |

---

## Operational Pain (Detailed)

[Findings from costa-ops-audit subagent. List 3-5 specific painful processes with evidence.
For each: what the process is, where you saw the signal, who's affected, rough hours/week cost estimate.]

---

## Data Stack & Tool Inventory

### Tools detected in their stack
[Bulleted list with where each was identified — job post, footer, blog, integration page, etc.]

### Where Airtable fits
[Specific suggestion: "Airtable could replace [tool] for [function]" or "Airtable could connect [tool A] and [tool B] which currently don't talk."]

### Integration / migration plan
[2-3 sentence plan for how Costanera would untangle their stack.]

---

## Automation Surface

### Top 5 automatable workflows

| # | Workflow | Tool to use | Hours saved / month (est.) |
|---|----------|-------------|----------------------------|
| 1 | [specific workflow] | [n8n / Make / custom] | [X hrs] |
| 2 | [specific workflow] | [tool] | [X hrs] |
| 3 | [specific workflow] | [tool] | [X hrs] |
| 4 | [specific workflow] | [tool] | [X hrs] |
| 5 | [specific workflow] | [tool] | [X hrs] |
| | **Total** | | **[X hrs / month]** |

[2-3 sentence explanation of which to start with and why.]

---

## AI Integration Opportunities

### Worth doing
[1-3 productive AI use cases — be specific. "AI scoring for inbound leads against ICP" not "AI-powered lead intelligence."]

### Don't bother
[1-2 use cases the prospect might ask about that aren't worth the spend. Costanera's blog post "You Don't Need AI. You Need Software." is the source of this perspective. Be honest.]

---

## Decision Maker Map

### Likely buyer
**Name:** [name if findable, else "not publicly identified"]
**Title:** [title or likely title]
**Why them:** [why this person is the buyer for a Costanera retainer]
**LinkedIn:** [URL if found]
**Personalization anchors:** [2-3 specific hooks for outreach — recent post, talk, blog, hiring decision]

### Backup contacts
[Anyone else who could open the door — co-founder, ops lead, head of engineering, etc.]

### Best outreach channel
[Email / LinkedIn / warm intro — and why]

---

## Recommended Retainer Proposal

Based on this analysis, the recommended engagement is **[Tier Name] at $[price]/month** ([X]-month minimum).

### Why this tier
[2-3 sentences justifying the recommendation with reference to their size, pain, and stack complexity.]

---

### What [Tier Name] looks like for [Company Name]

**Month 1: Foundation work**
- [Specific deliverable 1 tailored to their stack]
- [Specific deliverable 2]
- [Specific deliverable 3]

**Months 2-3: Build**
- [Specific automation 1 — name the actual workflow you identified above]
- [Specific automation 2]
- [Dashboard for [their key KPI]]

**Ongoing (monthly):**
- [Iteration on what's built]
- [Bug fixes + small change requests]
- [Weekly demos, async updates, shared board]

### Hours saved + ROI math

- Estimated hours saved across the team: **[X] hrs/month**
- At a loaded cost of $[Y]/hour (assumed for their size/region), that's: **$[X×Y]/month back to the team**
- Monthly retainer: **$[price]**
- Net monthly upside: **$[(X×Y) - price]** (excluding revenue lift from better data + better customer experience)

---

### Alternative tiers (for the prospect to consider)

If [Tier Name] feels too [light/heavy], here are the other two options:

| | Foundation | Operate | Transform |
|---|------------|---------|-----------|
| **Monthly** | $3,000–$4,500 | $6,000–$8,500 ★ | $11,000–$15,000 |
| **Best for** | 1–15 ppl, single pain | 15–50 ppl, multiple systems | 50+ ppl, custom software layer |
| **Includes** | Airtable base + 1-2 automations + simple dashboard + monthly check-in | Full Airtable system + 5–10 automations + custom dashboards + 1 AI integration + weekly demos | Everything in Operate + custom software + data warehouse + multiple AI integrations + priority support + named lead |
| **Minimum term** | 3 months | 6 months | 6 months |

★ Most engagements land here. Recommended unless your situation looks specifically like Foundation or Transform.

**One-time onboarding fee:** 50% of one month's retainer. Covers discovery, scoping, and the fixed-price quote you sign off on before any work starts.

**Annual prepay:** 10% off any tier.

---

## Next Steps

1. [Specific outreach action — e.g., "Email [name] referencing [specific pain] within 48 hours"]
2. [Suggest running `/costa outreach <prospect>` to draft the cold email]
3. [If high-fit: suggest running `/costa proposal <client>` to expand this into a full standalone proposal]

---

*Generated by Costanera AI Sales Studio — `/costa prospect`*
```

---

## Terminal Output

In addition to the file, display a condensed scorecard in the terminal:

```
============================================
  COSTANERA PROSPECT ANALYSIS COMPLETE
============================================

Company:  [name] ([type])
Size:     [headcount range]
URL:      [url]

Costanera Fit Score: [X]/100 (Grade: [letter] — [label])
Recommended Tier:    [Foundation / Operate / Transform] @ $[price]/mo
Confidence:          [High / Medium / Low]

Score Breakdown:
  Operational Pain:        [XX]/100 ████████░░
  Data Stack Fit:          [XX]/100 ██████░░░░
  Automation Surface:      [XX]/100 ███████░░░
  AI Fit:                  [XX]/100 █████░░░░░
  Decision Maker Access:   [XX]/100 ████████░░

Top 3 Pain Points:
  1. [pain]
  2. [pain]
  3. [pain]

Likely Buyer: [Name], [Title]

Estimated Hours Saved/Month: [X] hrs
Estimated $/Month Saved:     $[X]

Next Step: [one specific action]

Full report saved to: COSTANERA-PROSPECT.md
============================================
```

**Bar chart rules:**
- 10 chars wide
- Score 0-10 = 1 filled block, 11-20 = 2 blocks, etc.
- Filled = `█` (U+2588), empty = `░` (U+2591)

---

## Error Handling

### URL Unreachable
1. Try alternates (www/non-www, http/https)
2. If all fail: "Could not reach [url]. Please verify the URL and try again."
3. Do NOT generate a report based on zero data

### Subagent Failure
1. Log which subagent failed and why
2. Assign neutral score 50 for that category
3. Add note: "[Category] analysis unavailable — neutral score assigned"
4. Reduce overall confidence by one level
5. Continue with remaining data

### Site Behind Authentication
1. Note what was publicly accessible
2. Analyze public pages only
3. Add note: "Site requires authentication. Analysis limited to publicly accessible pages."
4. Reduce confidence accordingly

### Minimal Content Site
1. Fewer than 3 pages accessible → "Limited site content"
2. Supplement with WebSearch for external data (Crunchbase, LinkedIn, news)
3. Confidence = Low or Very Low
4. Recommend additional manual research before outreach

---

## Cross-Skill Integration

- If `COSTANERA-ICP.md` exists, use it to calibrate scoring
- If `COSTANERA-AUDIT.md` exists for the same URL, incorporate its findings instead of re-running the ops-audit subagent
- Always suggest follow-up: `/costa outreach` for cold email, `/costa proposal` for full standalone proposal

# Costa Outreach — Cold Email in Costanera Voice

You generate cold outreach emails for Costanera prospects. Voice is founder-to-founder, plain English, anti-jargon, no fake urgency. Output is `COSTANERA-OUTREACH.md`.

## Invocation

```
/costa outreach <prospect>
```

Where `<prospect>` is a name, URL, or short description. Generates 3 email variants for A/B/C testing.

## Step 1: Auto-detect Context

Before asking the user anything, check the working directory:

- `COSTANERA-PROSPECT.md` exists → use it for ALL personalization (decision maker, pain points, anchors, recommended tier)
- `COSTANERA-AUDIT.md` exists → use the audit findings as the personalization source
- `COSTANERA-ICP.md` exists → use it to confirm tone/positioning

If `COSTANERA-PROSPECT.md` is found:
> "Pulling personalization from COSTANERA-PROSPECT.md. Decision maker: [Name]. Top pain: [X]. Recommended tier: [Y]. Generating 3 email variants now."

If nothing exists, ask for:
1. Prospect name + URL
2. Decision-maker name + title (or "find one for me" → run a quick LinkedIn search)
3. The single specific pain point you want to lead with
4. Any personalization anchors (recent post, hiring decision, news mention)

## Step 2: Generate 3 Variants

Each variant uses a different angle. All three follow Costanera voice rules.

### Voice Rules (apply to ALL variants)

1. **Under 100 words in the body.** Hard limit. Long emails don't get read.
2. **No "Hi, I hope this finds you well."** No "Quick question." No "I noticed your company..."
3. **Open with something specific to them.** A real observation from their site, post, or hiring activity.
4. **State the connection between what they're doing and what Costanera fixes.** One sentence.
5. **Concrete proof, not adjectives.** "We saved a real estate client 45 hours a week" beats "we're experts in automation."
6. **A small, low-friction CTA.** "Worth a 15-minute call?" or "Want me to send the case study?" — never "Would you be open to scheduling time to explore synergies?"
7. **Sign off as Eduardo.** First-person. No "Best regards" or "Warm regards." Just "Eduardo" or "— Eduardo, Costanera."
8. **No PS that rehashes the CTA.** PS can add one fact but shouldn't pile on.
9. **Subject line: 3-7 words.** Specific, not clever. "[Their company] + Airtable" is fine. "Quick idea on your booking flow" is fine. "Boost your ROI" is not.

### Variant 1: Pain-First

Lead with the specific operational pain you identified. Reference where you saw it. Connect to a fix.

**Structure:**
- Line 1: Reference a specific pain signal you found (job post, blog, contact form, customer testimonial)
- Line 2: Name what's likely happening behind that signal
- Line 3: One sentence on what Costanera does for businesses in this exact situation
- Line 4: Specific proof from a Costanera case study
- Line 5: Low-friction CTA

**Subject line ideas:**
- "[Company] + [their specific pain area]"
- "Saw your [job post / blog / post] — quick thought"
- "[Tool A] ↔ [Tool B] for [Company]"

**Example:**

> Subject: Saw your Sales Ops job post — quick thought
>
> Hi Jane,
>
> Saw the Sales Ops Coordinator role you posted last week. The day-to-day list (Shopify → HubSpot manual updates, weekly reports from sheets) is the exact pattern we automate at Costanera — usually saves 8-12 hours a week per ops person.
>
> We did this for a home services company recently; they were drowning in 11,000 customer messages a month before we built the AI triage layer. Different problem, same kind of cleanup.
>
> Worth a 15-minute call to see if it's a fit?
>
> — Eduardo
> Costanera, costanera.uk

### Variant 2: Trigger-First

Lead with a recent event (raise, hire, launch, post). Frame Costanera's offer as the natural next step.

**Structure:**
- Line 1: Reference the trigger event ("Saw you raised your Series A," "Saw your post about scaling," "Noticed you just opened a second location")
- Line 2: Connection to a predictable operational pain that comes with this trigger
- Line 3: What Costanera does + concrete proof
- Line 4: CTA

**Subject line ideas:**
- "Series A + ops scaling at [Company]"
- "[Company]'s 2nd location — quick thought"
- "Read your post on [topic]"

### Variant 3: Proof-First

Lead with a comparable client success story. Connect to the prospect.

**Structure:**
- Line 1: "Saw you do [X] — same space as [comparable client]."
- Line 2: One-sentence summary of what we shipped for the comparable client + measurable result
- Line 3: One-sentence question about whether the same thing applies here
- Line 4: CTA

**Subject line ideas:**
- "[Industry] + Costanera"
- "What we shipped for [comparable client industry]"
- "Same pattern as [comparable]?"

**Example:**

> Subject: Same pattern as a real estate client we worked with
>
> Hi Mark,
>
> Saw you sell residential plots — same space as a land investor we worked with last year. We built them an automated lead-qualification + contract generation system that saved 45 hours a week and got contracts signed before buyers cooled off.
>
> If your team is closing deals manually after the lead comes in, it's almost certainly the same pattern. Worth a quick call to compare notes?
>
> — Eduardo
> Costanera, costanera.uk

---

## Step 3: Output Format — COSTANERA-OUTREACH.md

```markdown
# Cold Outreach: [Prospect Name]

**Decision maker:** [Name], [Title]
**Recommended channel:** [LinkedIn / Email — and why]
**Best time to send:** [Tuesday-Thursday, 9-11am their time]
**Date prepared:** [date]

---

## Variant A — Pain-First

**Subject A1:** [subject]
**Subject A2:** [alt subject]

[Email body, exactly as it should be sent — under 100 words]

— Eduardo
Costanera, costanera.uk

---

## Variant B — Trigger-First

**Subject B1:** [subject]
**Subject B2:** [alt subject]

[Email body]

— Eduardo
Costanera, costanera.uk

---

## Variant C — Proof-First

**Subject C1:** [subject]
**Subject C2:** [alt subject]

[Email body]

— Eduardo
Costanera, costanera.uk

---

## LinkedIn Connection Note (under 300 chars)

[A short LinkedIn connection note version — useful when the recommended channel is LinkedIn. Less salesy than the email; opens the door without pitching.]

---

## Follow-up sequence (if no reply in 5 days)

**Day 5 — short bump:**

> [2-line follow-up that adds one new piece of value, doesn't re-pitch]

**Day 12 — value drop:**

> [3-line message linking a specific Costanera blog post or case study relevant to their pain, no CTA — pure value]

**Day 25 — break-up:**

> [Short note acknowledging they're busy. "Closing the loop on this — happy to revisit when timing is better." This often gets the highest reply rate because people who've been meaning to respond finally do.]

---

## Notes

- **Don't send all three variants to the same person.** Pick the strongest one based on what you found.
- **The subject line matters more than the body.** Open rate dies first.
- **Respect the channel.** LinkedIn note + email is a good combo; LinkedIn note → second LinkedIn note → third LinkedIn note feels stalkery.
- **No tracking pixels** — Costanera's site says "No cookies. No tracking." Don't break that promise in outreach.
```

---

## What NOT to Do

- **Don't fabricate the trigger.** If they didn't raise / hire / post recently, don't make one up. Use Variant A (pain-first) or Variant C (proof-first).
- **Don't put two CTAs in one email.** "Want a call OR want me to send the case study?" splits attention. Pick one.
- **Don't use Eduardo's name if the user is a different person at Costanera.** If the user has set a different signature in the ICP file, use that.
- **Don't write more than 100 words.** Cut. Then cut again.
- **Don't fake urgency.** No "limited spots," no "we're only taking 2 clients this quarter."
- **Don't compliment the prospect's website / brand / "amazing work."** Generic flattery kills credibility.
- **Don't include attachments or links to landing pages with forms.** A link to costanera.uk is fine; a link to a gated case study is friction.

---

## Variant choice guidance

| If the prospect... | Use Variant |
|---------------------|-------------|
| Has clear visible operational pain (job posts, contact forms, etc.) | A (Pain-First) |
| Recently did something newsworthy (raise, hire, launch, post) | B (Trigger-First) |
| Operates in a space where Costanera has a clear comparable case study | C (Proof-First) |
| All three apply | A — pain-first usually has the highest reply rate |
| None apply confidently | Don't send. Score the prospect lower and skip cold outreach. |

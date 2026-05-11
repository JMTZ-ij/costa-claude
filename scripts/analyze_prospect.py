#!/usr/bin/env python3
"""
Costanera Prospect Analyzer
Fetches a company website and extracts structured data tuned to Costanera's
operational fit lens (Airtable + automation + AI integration retainer).

Usage:
    python3 analyze_prospect.py --url <url> --output json
    python3 analyze_prospect.py --help
"""

import argparse
import json
import re
import ssl
import sys
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

try:
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Costanera-specific tool/stack signal dictionary
# ---------------------------------------------------------------------------

# Tools whose presence signals operational pain Costanera typically fixes.
# Format: { detection_string_lower: ('layer', 'display_name', is_costanera_friendly) }
TOOL_SIGNALS = {
    # CRM / Sales
    'salesforce': ('CRM', 'Salesforce', False),  # usually wants Salesforce shop, not Costanera
    'hubspot': ('CRM', 'HubSpot', True),
    'pipedrive': ('CRM', 'Pipedrive', True),
    'close.com': ('CRM', 'Close', True),
    'copper.com': ('CRM', 'Copper', True),
    # eCommerce
    'shopify': ('Commerce', 'Shopify', True),
    'woocommerce': ('Commerce', 'WooCommerce', True),
    'bigcommerce': ('Commerce', 'BigCommerce', True),
    'magento': ('Commerce', 'Magento', True),
    'lightspeed': ('Commerce', 'Lightspeed', True),
    # Finance
    'stripe': ('Finance', 'Stripe', True),
    'quickbooks': ('Finance', 'QuickBooks', True),
    'xero': ('Finance', 'Xero', True),
    'sage': ('Finance', 'Sage', True),
    'freshbooks': ('Finance', 'FreshBooks', True),
    # Comms / Support
    'intercom': ('Comms', 'Intercom', True),
    'zendesk': ('Comms', 'Zendesk', True),
    'frontapp': ('Comms', 'Front', True),
    'helpscout': ('Comms', 'Help Scout', True),
    'slack.com': ('Comms', 'Slack', True),
    # PM / Ops
    'asana.com': ('PM', 'Asana', True),
    'monday.com': ('PM', 'Monday', True),
    'clickup': ('PM', 'ClickUp', True),
    'linear.app': ('PM', 'Linear', True),
    'notion.so': ('PM', 'Notion', True),
    'trello': ('PM', 'Trello', True),
    # Automation (existing — signals integration debt or migration potential)
    'zapier': ('Automation', 'Zapier', True),  # Costanera has a blog comparing Zapier vs Make vs n8n
    'make.com': ('Automation', 'Make', True),
    'n8n': ('Automation', 'n8n', True),
    'workato': ('Automation', 'Workato', False),  # enterprise, not Costanera shape
    # Data store
    'airtable': ('DataStore', 'Airtable', True),  # already on Airtable = strong fit
    'google.com/sheets': ('DataStore', 'Google Sheets', True),
    'docs.google.com/spreadsheets': ('DataStore', 'Google Sheets', True),
    # Marketing
    'mailchimp': ('Marketing', 'Mailchimp', True),
    'klaviyo': ('Marketing', 'Klaviyo', True),
    'activecampaign': ('Marketing', 'ActiveCampaign', True),
    # Analytics
    'google-analytics': ('Analytics', 'Google Analytics', True),
    'mixpanel': ('Analytics', 'Mixpanel', True),
    'segment.com': ('Analytics', 'Segment', True),
    # Anti-fit signals (mark as not friendly)
    'powerautomate': ('Automation', 'Power Automate', False),
    'dataverse': ('DataStore', 'Dataverse', False),
}

# Phrases that signal manual / operational pain
PAIN_PHRASES = [
    ("we'll get back to you", 'No automated triage on inbound'),
    ('call us for a quote', 'Manual quoting process'),
    ('within 24 hours', 'Manual response SLA'),
    ('within 48 hours', 'Manual response SLA — slow'),
    ('within 2 business days', 'Slow manual response'),
    ('our team will reach out', 'Manual lead routing'),
    ('fill out this form', 'Form-based inquiry, likely manual followup'),
    ('we\'re hiring', 'Active hiring (potential ops bottleneck signal)'),
    ('book a call', 'At least booking is automated — neutral'),
    ('schedule a demo', 'Sales-led — possible manual process'),
    ('powered by', 'Tool dependency visible in footer'),
]

# Costanera-friendly business type phrases
BUSINESS_TYPE_HINTS = {
    'engineering': ['engineering', 'consultancy', 'consulting engineers', 'civil engineering', 'mechanical engineering'],
    'specialised_services': ['hvac', 'pool service', 'pool services', 'pool cleaning', 'cleaning services',
                              'plumbing', 'electrical contractors', 'pest control', 'landscaping', 'pool maintenance'],
    'real_estate': ['real estate', 'property investment', 'land investors', 'land sales', 'realtor',
                    'estate agent', 'land development'],
    'manufacturing': ['manufacturing', 'manufacturer', 'fabrication', 'industrial supplier'],
    'ecommerce': ['shop now', 'add to cart', 'checkout', 'free shipping', 'returns policy', 'product catalog'],
    'content_media': ['publication', 'magazine', 'editorial', 'newsroom', 'content studio', 'media company'],
    'professional_services': ['consulting', 'advisory', 'professional services', 'legal services',
                              'accounting firm', 'consultancy'],
}


# ---------------------------------------------------------------------------
# Lightweight HTML helpers
# ---------------------------------------------------------------------------

class TagCollector(HTMLParser):
    """Minimal HTML parser that collects tags, attributes, and text."""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta = {}
        self.headings = []
        self.links = []
        self.scripts = []
        self.text_chunks = []
        self.current_tag = None
        self.in_title = False
        self.in_heading = False

    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        self.current_tag = tag
        if tag == 'title':
            self.in_title = True
        elif tag in ('h1', 'h2', 'h3'):
            self.in_heading = tag
        elif tag == 'meta':
            name = attrs_d.get('name') or attrs_d.get('property') or ''
            content = attrs_d.get('content', '')
            if name:
                self.meta[name.lower()] = content
        elif tag == 'a':
            href = attrs_d.get('href', '')
            if href:
                self.links.append(href)
        elif tag == 'script':
            src = attrs_d.get('src', '')
            if src:
                self.scripts.append(src)

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag in ('h1', 'h2', 'h3'):
            self.in_heading = False

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        if self.in_title:
            self.title += text + ' '
        elif self.in_heading:
            self.headings.append((self.in_heading, text))
        else:
            if len(text) > 3 and self.current_tag not in ('script', 'style'):
                self.text_chunks.append(text)


# ---------------------------------------------------------------------------
# Fetcher
# ---------------------------------------------------------------------------

def fetch_url(url, timeout=15):
    """Fetch a URL and return (status, html_content). Raises on hard failure."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; CostaneraProspectAnalyzer/1.0)',
        'Accept': 'text/html,application/xhtml+xml',
    }
    req = Request(url, headers=headers)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        with urlopen(req, timeout=timeout, context=ctx) as resp:
            content_bytes = resp.read()
            charset = resp.headers.get_content_charset() or 'utf-8'
            try:
                content = content_bytes.decode(charset, errors='replace')
            except (LookupError, UnicodeDecodeError):
                content = content_bytes.decode('utf-8', errors='replace')
            return resp.status, content
    except HTTPError as e:
        return e.code, ''
    except URLError as e:
        return None, str(e)


def normalize_url(url):
    """Add https:// if missing and strip trailing slashes."""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url.rstrip('/')


# ---------------------------------------------------------------------------
# Analyzers
# ---------------------------------------------------------------------------

def detect_tools(html, scripts, links):
    """Return list of detected tools with metadata."""
    haystack = (html + ' '.join(scripts) + ' '.join(links)).lower()
    found = []
    for needle, (layer, name, friendly) in TOOL_SIGNALS.items():
        if needle in haystack:
            found.append({
                'name': name,
                'layer': layer,
                'costanera_friendly': friendly,
                'detection_signal': needle,
            })
    return found


def detect_pain_phrases(text_blob):
    """Find indicators of manual / operational pain in plain-text content."""
    found = []
    lower = text_blob.lower()
    for phrase, interpretation in PAIN_PHRASES:
        if phrase in lower:
            found.append({
                'phrase_found': phrase,
                'interpretation': interpretation,
            })
    return found


def detect_business_type(text_blob, headings):
    """Score the prospect against Costanera's served business types."""
    blob = text_blob.lower() + ' ' + ' '.join(h[1] for h in headings).lower()
    scores = {}
    for category, phrases in BUSINESS_TYPE_HINTS.items():
        hits = sum(1 for p in phrases if p in blob)
        if hits > 0:
            scores[category] = hits
    if not scores:
        return ('other', {})
    top = max(scores, key=scores.get)
    return (top, scores)


def extract_emails(text_blob):
    """Extract email addresses (rough)."""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    raw = re.findall(pattern, text_blob)
    # Filter out garbage (sentry, wixpress, etc.)
    blocked = ('sentry.io', 'wixpress', 'example.com', '@2x', 'noreply', 'no-reply')
    return sorted({e.lower() for e in raw if not any(b in e.lower() for b in blocked)})


def extract_social_links(links):
    """Return social profile URLs."""
    socials = {}
    domains = {
        'linkedin.com/company': 'linkedin_company',
        'linkedin.com/in': 'linkedin_personal',
        'twitter.com': 'twitter',
        'x.com': 'twitter',
        'facebook.com': 'facebook',
        'instagram.com': 'instagram',
        'youtube.com': 'youtube',
        'github.com': 'github',
    }
    for link in links:
        ll = link.lower()
        for needle, key in domains.items():
            if needle in ll and key not in socials:
                socials[key] = link
    return socials


def detect_team_size_signals(text_blob):
    """Look for explicit team-size mentions."""
    patterns = [
        r'team of (\d+)',
        r'(\d+)\s*employees',
        r'(\d+)\s*people',
        r'(\d+)-person team',
        r'we are (\d+)',
        r'(\d+)\+ team members',
    ]
    findings = []
    for p in patterns:
        for m in re.finditer(p, text_blob, re.IGNORECASE):
            findings.append({
                'pattern': p,
                'value': m.group(1),
                'context': text_blob[max(0, m.start()-30):m.end()+30],
            })
    return findings


def discover_interior_pages(base_url, links):
    """Find probable interior pages worth fetching."""
    parsed_base = urlparse(base_url)
    base_host = parsed_base.netloc
    candidates = {
        'about': ['/about', '/about-us', '/company', '/our-story'],
        'team': ['/team', '/leadership', '/people', '/about/team'],
        'pricing': ['/pricing', '/plans', '/packages'],
        'careers': ['/careers', '/jobs', '/join-us', '/hiring', '/work-with-us'],
        'blog': ['/blog', '/resources', '/insights', '/news'],
        'contact': ['/contact', '/get-in-touch', '/get-started'],
        'integrations': ['/integrations', '/partners', '/connect'],
    }
    found = {}
    seen_paths = set()
    for link in links:
        try:
            full = urljoin(base_url, link)
        except (ValueError, AttributeError):
            continue
        parsed = urlparse(full)
        if parsed.netloc != base_host:
            continue
        path = parsed.path.lower().rstrip('/') or '/'
        if path in seen_paths:
            continue
        seen_paths.add(path)
        for category, options in candidates.items():
            if category in found:
                continue
            if path in options:
                found[category] = full
    return found


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------

def analyze(url):
    url = normalize_url(url)
    result = {
        'url': url,
        'fetch_status': None,
        'company_name_guess': None,
        'meta_description': None,
        'detected_business_type': None,
        'business_type_scores': {},
        'detected_tools': [],
        'pain_signals': [],
        'team_size_signals': [],
        'emails_found': [],
        'social_links': {},
        'interior_pages_found': {},
        'headings': [],
        'errors': [],
    }

    # Fetch homepage
    status, html = fetch_url(url)
    result['fetch_status'] = status
    if not html or status != 200:
        result['errors'].append(f'Could not fetch homepage (status: {status})')
        return result

    # Parse
    parser = TagCollector()
    try:
        parser.feed(html)
    except Exception as e:
        result['errors'].append(f'HTML parse error: {e}')
        return result

    # Build text blob for content analysis
    text_blob = ' '.join(parser.text_chunks)[:50000]  # cap for performance

    # Extract basics
    result['company_name_guess'] = (
        parser.meta.get('og:site_name')
        or parser.meta.get('application-name')
        or parser.title.strip()[:120]
        or None
    )
    result['meta_description'] = parser.meta.get('description') or parser.meta.get('og:description')
    result['headings'] = [{'level': h[0], 'text': h[1][:200]} for h in parser.headings[:30]]

    # Business type
    biz_type, biz_scores = detect_business_type(text_blob, parser.headings)
    result['detected_business_type'] = biz_type
    result['business_type_scores'] = biz_scores

    # Tools
    result['detected_tools'] = detect_tools(html, parser.scripts, parser.links)

    # Pain signals
    result['pain_signals'] = detect_pain_phrases(text_blob)

    # Team size
    result['team_size_signals'] = detect_team_size_signals(text_blob)

    # Contact info
    result['emails_found'] = extract_emails(html)[:10]
    result['social_links'] = extract_social_links(parser.links)

    # Interior pages
    result['interior_pages_found'] = discover_interior_pages(url, parser.links)

    return result


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(
        description='Costanera Prospect Analyzer — fetches a URL and extracts Costanera-relevant signals.'
    )
    p.add_argument('--url', required=True, help='Target prospect URL')
    p.add_argument('--output', default='json', choices=['json', 'pretty'], help='Output format')
    args = p.parse_args()

    try:
        result = analyze(args.url)
    except Exception as e:
        print(json.dumps({'error': str(e), 'url': args.url}), file=sys.stderr)
        sys.exit(1)

    if args.output == 'pretty':
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))


if __name__ == '__main__':
    main()

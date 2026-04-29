"""
Instagram DM Outreach (Semi-Automated)
Generates DM templates for each lead - you manually send via IG

Note: Auto-DM via Instagram violates ToS and can get your account banned.
This generates ready-to-send messages for manual copy-paste.
"""

import os
import csv
from datetime import datetime
from typing import List, Dict


class InstagramOutreach:
    """Generate personalized IG DM templates"""

    TEMPLATES = {
        'casual': """
Hey {business_name}! 👋

Love what you're doing with {business_type} in {location}!

Quick question - are you guys working on updating your website right now? I noticed it could use some love (not mobile-friendly / no HTTPS / etc).

I run a small web dev studio and we're offering free mockups to businesses we admire. No strings - just want to show you what's possible!

Interested?

- Yatharth
        """,

        'direct': """
Hi {business_name} team,

I'm Yatharth from Zelex Studio. We help {business_type}s in {location} get more customers through better websites.

Your current site has a few issues costing you rankings:
{issues}

We can fix this. Want a free mockup of what your new site could look like?

Let me know!
        """,

        'compliment': """
Hey! Just found {business_name} while searching for {business_type}s in {location} - your stuff looks amazing!

One thing though - your website isn't doing you justice. It's {issues}.

I'd love to help you build something that matches the quality of your work. Free mockup if you're interested.

No pressure at all! Just had to reach out.

- Yatharth @ Zelex Studio
        """
    }

    def __init__(self):
        self.leads = []

    def load_leads(self, filepath: str = 'leads_high_priority.csv') -> List[Dict]:
        """Load leads from CSV"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.leads = list(reader)
            print(f"Loaded {len(self.leads)} leads")
        except FileNotFoundError:
            print(f"No leads file: {filepath}")
        return self.leads

    def generate_dm(self, lead: Dict, style: str = 'casual') -> str:
        """Generate personalized DM for a lead"""
        template = self.TEMPLATES.get(style, self.TEMPLATES['casual'])

        issues = lead.get('website_issues', 'could be better')
        if len(issues) > 100:
            issues = issues[:100] + '...'

        return template.format(
            business_name=lead.get('name', 'there'),
            business_type=lead.get('business_type', 'business'),
            location=lead.get('location', 'area'),
            issues=issues
        ).strip()

    def generate_all(self, style: str = 'casual') -> List[Dict]:
        """Generate DMs for all leads"""
        results = []

        for lead in self.leads:
            dm = self.generate_dm(lead, style)
            results.append({
                'name': lead.get('name'),
                'instagram_handle': lead.get('instagram', ''),
                'dm_template': dm,
                'generated_at': datetime.now().isoformat()
            })

        return results

    def save_templates(self, output_file: str = 'ig_dm_templates.txt'):
        """Save all DM templates to a text file"""
        results = self.generate_all()

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("INSTAGRAM DM TEMPLATES - Zelex Leads\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write("=" * 60 + "\n\n")

            for i, result in enumerate(results, 1):
                f.write(f"[{i}] {result['name']}\n")
                f.write(f"IG Handle: @{result['instagram_handle'] or 'N/A'}\n")
                f.write("-" * 40 + "\n")
                f.write(result['dm_template'])
                f.write("\n\n" + "=" * 60 + "\n\n")

        print(f"Saved {len(results)} DM templates to {output_file}")
        return output_file


def main():
    outreach = InstagramOutreach()
    outreach.load_leads()
    outreach.save_templates('ig_dm_templates.txt')

    print("\n=== Instagram Outreach Ready ===")
    print("Open ig_dm_templates.txt and copy-paste DMs manually")
    print("Tip: Send 10-20 DMs/day to avoid flagging")


if __name__ == '__main__':
    main()

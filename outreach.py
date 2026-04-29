"""
Zelex Leads - Automated Outreach System
Sends personalized emails to verified leads via SendGrid
"""

import os
import csv
import json
from datetime import datetime
from typing import List, Dict
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class OutreachManager:
    def __init__(self):
        self.api_key = os.getenv('SENDGRID_API_KEY', '')
        self.sg = SendGridAPIClient(self.api_key) if self.api_key else None
        self.from_email = os.getenv('FROM_EMAIL', 'hello@zelexstudio.in')
        self.from_name = os.getenv('FROM_NAME', 'Zelex Studio')

    def generate_subject(self, lead: Dict) -> str:
        """Generate personalized subject line"""
        business_type = lead.get('business_type', 'business')
        location = lead.get('location', '')

        subjects = [
            f"Quick question about {lead['name']}'s online presence",
            f"Helping {business_type}s in {location} get more customers",
            f"Your website could be costing you customers",
            f"Saw {lead['name']} - love what you're doing!",
            f"Free website audit for {lead['name']}",
        ]

        import random
        return random.choice(subjects)

    def generate_email_body(self, lead: Dict) -> str:
        """Generate personalized email body"""
        name = lead.get('name', 'there')
        business_type = lead.get('business_type', 'business')
        issues = lead.get('website_issues', '')
        location = lead.get('location', '')

        # Personalize based on issues
        if 'No website found' in issues:
            hook = f"I noticed {name} doesn't have a website yet. In 2026, that's leaving a lot of customers on the table."
        elif 'Not mobile-friendly' in issues:
            hook = f"Your website isn't mobile-friendly. Over 60% of customers search for {business_type}s on their phones."
        elif 'No HTTPS' in issues:
            hook = f"Your website doesn't use HTTPS. Google is probably penalizing your rankings because of this."
        else:
            hook = f"I was looking for {business_type}s in {location} and found {name}. Your website could be converting way better."

        email = f"""
Hi there,

{hook}

I'm from Zelex Studio, and we specialize in helping {business_type}s like yours get more customers through better web experiences.

Here's what a professional website could do for {name}:
• Show up first when people search "{business_type} in {location}"
• Convert visitors into actual customers (not just window shoppers)
• Build trust before customers even walk through your door

I'd love to send you a free mockup of what a modern website could look like for {name}. No strings attached - just want to show you what's possible.

Interested in seeing it?

Best,
Zelex Studio Team
hello@zelexstudio.in
https://zelexstudio.in

P.S. We're offering 20% off for the first 5 businesses this month. Just mentioning!
"""

        return email.strip()

    def send_email(self, to_email: str, lead: Dict) -> Dict:
        """Send single email"""
        if not self.sg:
            return {'success': False, 'error': 'No SendGrid API key'}

        try:
            message = Mail(
                from_email=(self.from_email, self.from_name),
                to_emails=to_email,
                subject=self.generate_subject(lead),
                plain_text_content=self.generate_email_body(lead)
            )

            response = self.sg.send(message)
            return {
                'success': True,
                'status_code': response.status_code,
                'sent_at': datetime.now().isoformat()
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'sent_at': datetime.now().isoformat()
            }

    def outreach(self, leads_file: str = 'leads_high_priority.csv') -> List[Dict]:
        """Send emails to all leads"""
        results = []

        if not os.path.exists(leads_file):
            print(f"No leads file found: {leads_file}")
            return results

        with open(leads_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            leads = list(reader)

        print(f"Found {len(leads)} leads to contact")

        for i, lead in enumerate(leads):
            email = lead.get('email', '')

            if not email:
                print(f"Skipping {lead['name']} - no email")
                results.append({
                    'name': lead['name'],
                    'email': '',
                    'success': False,
                    'error': 'No email found',
                    'sent_at': datetime.now().isoformat()
                })
                continue

            print(f"[{i+1}/{len(leads)}] Sending to {lead['name']} ({email})...")

            result = self.send_email(email, lead)
            result['name'] = lead['name']
            result['email'] = email
            results.append(result)

            if result['success']:
                print(f"  ✓ Sent!")
            else:
                print(f"  ✗ Failed: {result.get('error', 'Unknown error')}")

            # Rate limiting - SendGrid free tier: 100/day
            if i >= 99:
                print("Reached daily limit (100 emails)")
                break

            import time
            time.sleep(1)  # 1 second between emails

        return results

    def save_results(self, results: List[Dict], filename: str = 'outreach_log.csv'):
        """Save outreach results"""
        if not results:
            return

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['name', 'email', 'success', 'error', 'status_code', 'sent_at']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print(f"\nSaved outreach results to {filename}")

        # Summary
        successful = [r for r in results if r.get('success')]
        print(f"Successful: {len(successful)}/{len(results)}")


def main():
    manager = OutreachManager()
    results = manager.outreach('leads_high_priority.csv')
    manager.save_results(results)


if __name__ == '__main__':
    main()

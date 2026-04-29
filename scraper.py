"""
Zelex Leads Scraper
Scrapes businesses from multiple sources and identifies those needing web dev
"""

import os
import json
import csv
import time
import re
from datetime import datetime
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class LeadScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.ua.chrome})

    def search_google_maps(self, query: str, location: str, max_results: int = 20) -> List[Dict]:
        """
        Search businesses via Google Maps (using search API alternative)
        Note: Direct scraping violates ToS, using public search instead
        """
        results = []

        # Using OpenStreetMap Nominatim (free, ToS-friendly)
        search_query = f"{query} in {location}"
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': search_query,
            'format': 'json',
            'limit': max_results,
            'addressdetails': 1
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()

            for item in data:
                business = {
                    'name': item.get('display_name', '').split(',')[0],
                    'address': item.get('display_name', ''),
                    'lat': item.get('lat'),
                    'lon': item.get('lon'),
                    'source': 'OpenStreetMap',
                    'website': self._extract_website(item.get('display_name', '')),
                    'phone': '',
                    'category': query,
                    'location': location
                }
                results.append(business)

        except Exception as e:
            print(f"Error searching OSM: {e}")

        return results

    def search_yelp(self, term: str, location: str, max_results: int = 20) -> List[Dict]:
        """
        Search Yelp for businesses (public API alternative)
        """
        results = []

        # Using Yelp Fusion API would require API key
        # Fallback to web search for Yelp listings
        search_url = f"https://www.yelp.com/search?find_desc={term}&find_loc={location}"

        try:
            headers = {'User-Agent': self.ua.chrome}
            response = self.session.get(search_url, headers=headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Parse business listings
                listings = soup.select('div[data-testid="business-listing"]')

                for listing in listings[:max_results]:
                    business = {
                        'name': listing.select_one('a[data-testid="business-name"]')
                        .text.strip() if listing.select_one('a[data-testid="business-name"]') else '',
                        'address': listing.select_one('span[data-testid="business-address"]')
                        .text.strip() if listing.select_one('span[data-testid="business-address"]') else '',
                        'phone': listing.select_one('span[data-testid="business-phone"]')
                        .text.strip() if listing.select_one('span[data-testid="business-phone"]') else '',
                        'website': '',
                        'rating': listing.select_one('span[data-testid="rating"]')
                        .text.strip() if listing.select_one('span[data-testid="rating"]') else '',
                        'category': term,
                        'location': location,
                        'source': 'Yelp'
                    }
                    results.append(business)

        except Exception as e:
            print(f"Error searching Yelp: {e}")

        return results

    def _extract_website(self, text: str) -> str:
        """Extract website URL from text"""
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        matches = re.findall(url_pattern, text)
        return matches[0] if matches else ''

    def verify_website_quality(self, url: str) -> Dict:
        """
        Check if a website needs improvement
        Returns quality score and issues
        """
        result = {
            'has_website': False,
            'quality_score': 0,
            'issues': [],
            'needs_redesign': False
        }

        if not url:
            result['issues'].append('No website found')
            result['needs_redesign'] = True
            return result

        result['has_website'] = True

        try:
            response = self.session.get(url if url.startswith('http') else f'https://{url}', timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            score = 100

            # Check mobile responsiveness (basic)
            viewport = soup.find('meta', attrs={'name': 'viewport'})
            if not viewport:
                score -= 20
                result['issues'].append('Not mobile-friendly')

            # Check for modern meta tags
            if not soup.find('meta', attrs={'name': 'description'}):
                score -= 10
                result['issues'].append('Missing meta description')

            # Check for SSL (if we got response, likely has SSL)
            if response.url.startswith('http://'):
                score -= 15
                result['issues'].append('No HTTPS')

            # Check page load speed (basic)
            if len(response.text) > 500000:
                score -= 10
                result['issues'].append('Page too heavy')

            # Check for social media links
            social_icons = soup.select('a[href*="facebook"], a[href*="twitter"], a[href*="instagram"]')
            if not social_icons:
                score -= 5
                result['issues'].append('No social media links')

            # Check for contact information
            contact_keywords = ['contact', 'phone', 'email', 'address']
            has_contact = any(kw in response.text.lower() for kw in contact_keywords)
            if not has_contact:
                score -= 15
                result['issues'].append('No clear contact info')

            result['quality_score'] = max(0, score)
            result['needs_redesign'] = score < 60

        except Exception as e:
            result['issues'].append(f'Website error: {str(e)}')
            result['needs_redesign'] = True

        return result

    def find_email(self, url: str, business_name: str) -> str:
        """Try to find email from website"""
        if not url:
            return ''

        try:
            response = self.session.get(url if url.startswith('http') else f'https://{url}', timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Look for mailto links
            mailto = soup.find('a', href=re.compile(r'^mailto:'))
            if mailto:
                return mailto['href'].replace('mailto:', '')

            # Look for contact page
            contact_links = soup.select('a[href*="contact"], a[href*="about"]')
            for link in contact_links[:3]:
                try:
                    contact_url = link['href']
                    if not contact_url.startswith('http'):
                        contact_url = os.path.dirname(url) + '/' + contact_url
                    contact_resp = self.session.get(contact_url, timeout=5)
                    contact_soup = BeautifulSoup(contact_resp.text, 'html.parser')
                    mailto = contact_soup.find('a', href=re.compile(r'^mailto:'))
                    if mailto:
                        return mailto['href'].replace('mailto:', '')
                except:
                    continue

        except:
            pass

        return ''

    def scrape(self, niches: List[str], locations: List[str], max_per_combo: int = 10) -> List[Dict]:
        """Main scraping function"""
        all_leads = []

        for niche in niches:
            for location in locations:
                print(f"Scraping {niche} in {location}...")

                # Get businesses from OpenStreetMap
                businesses = self.search_google_maps(niche, location, max_per_combo)

                for biz in businesses:
                    # Verify website
                    website_quality = self.verify_website_quality(biz.get('website', ''))

                    lead = {
                        'name': biz['name'],
                        'business_type': niche,
                        'location': location,
                        'address': biz.get('address', ''),
                        'website': biz.get('website', ''),
                        'phone': biz.get('phone', ''),
                        'email': '',
                        'website_quality_score': website_quality['quality_score'],
                        'website_issues': '; '.join(website_quality['issues']),
                        'needs_website': website_quality['needs_redesign'],
                        'source': biz.get('source', ''),
                        'scraped_at': datetime.now().isoformat(),
                        'status': 'new'
                    }

                    # Find email if needs website
                    if lead['needs_website']:
                        lead['email'] = self.find_email(biz.get('website', ''), biz['name'])

                    all_leads.append(lead)
                    print(f"  Found: {lead['name']} - Needs website: {lead['needs_website']}")

                time.sleep(1)  # Rate limiting

        return all_leads


def main():
    # Get config from environment
    niches = os.getenv('NICHE', 'restaurants,cafes,salons').split(',')
    locations = os.getenv('TARGET_CITIES', 'New York,London').split(',')

    scraper = LeadScraper()
    leads = scraper.scrape(niches, locations, max_per_combo=10)

    # Save to CSV
    if leads:
        with open('leads.csv', 'w', newline='', encoding='utf-8') as f:
            fieldnames = leads[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(leads)

        print(f"\nSaved {len(leads)} leads to leads.csv")

        # Filter high-priority leads (no website at all)
        high_priority = [l for l in leads if 'No website found' in l['website_issues']]
        print(f"High priority (no website): {len(high_priority)}")

        # Save high priority separately
        if high_priority:
            with open('leads_high_priority.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=leads[0].keys())
                writer.writeheader()
                writer.writerows(high_priority)
            print(f"Saved {len(high_priority)} high-priority leads")


if __name__ == '__main__':
    main()

"""
Comprehensive Sitemap Generator for PeptideProtocols.ai
Generates dynamic XML sitemaps with all protocols, categories, and pages
"""

from datetime import datetime
import xml.etree.ElementTree as ET
from master_protocol_manager import master_protocol_manager
from typing import Dict, List

class SitemapGenerator:
    def __init__(self):
        self.base_url = "https://peptide-protocols-4.preview.emergentagent.com"
        self.last_modified = datetime.utcnow().strftime('%Y-%m-%d')
        
    def generate_sitemap(self) -> str:
        """Generate comprehensive XML sitemap"""
        # Create root element
        urlset = ET.Element('urlset')
        urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        urlset.set('xmlns:image', 'http://www.google.com/schemas/sitemap-image/1.1')
        urlset.set('xmlns:news', 'http://www.google.com/schemas/sitemap-news/0.9')
        
        # Add main pages
        main_pages = [
            {'loc': '/', 'priority': '1.0', 'changefreq': 'daily'},
            {'loc': '/assessment', 'priority': '0.9', 'changefreq': 'weekly'},
            {'loc': '/protocols', 'priority': '0.9', 'changefreq': 'daily'},
            {'loc': '/peptides', 'priority': '0.8', 'changefreq': 'daily'},
            {'loc': '/chat', 'priority': '0.7', 'changefreq': 'monthly'},
            {'loc': '/network', 'priority': '0.6', 'changefreq': 'monthly'},
            {'loc': '/dashboard', 'priority': '0.5', 'changefreq': 'weekly'},
            {'loc': '/feedback', 'priority': '0.4', 'changefreq': 'monthly'}
        ]
        
        for page in main_pages:
            url = ET.SubElement(urlset, 'url')
            ET.SubElement(url, 'loc').text = f"{self.base_url}{page['loc']}"
            ET.SubElement(url, 'lastmod').text = self.last_modified
            ET.SubElement(url, 'changefreq').text = page['changefreq']
            ET.SubElement(url, 'priority').text = page['priority']
            
        # Add protocol category pages
        categories = master_protocol_manager.get_categories()
        for category in categories:
            url = ET.SubElement(urlset, 'url')
            category_slug = category.lower().replace(' ', '-').replace('&', 'and')
            ET.SubElement(url, 'loc').text = f"{self.base_url}/protocols/category/{category_slug}"
            ET.SubElement(url, 'lastmod').text = self.last_modified
            ET.SubElement(url, 'changefreq').text = 'weekly'
            ET.SubElement(url, 'priority').text = '0.7'
            
        # Add individual protocol pages
        protocols = master_protocol_manager.all_protocols
        for protocol in protocols:
            url = ET.SubElement(urlset, 'url')
            protocol_slug = protocol['name'].lower().replace(' ', '-').replace('/', '-')
            ET.SubElement(url, 'loc').text = f"{self.base_url}/protocol/{protocol['id']}/{protocol_slug}"
            ET.SubElement(url, 'lastmod').text = protocol.get('last_updated', self.last_modified)[:10]
            ET.SubElement(url, 'changefreq').text = 'monthly'
            ET.SubElement(url, 'priority').text = '0.8'
            
            # Add image for protocols that have them
            if protocol.get('image_url'):
                image = ET.SubElement(url, 'image:image')
                ET.SubElement(image, 'image:loc').text = f"{self.base_url}{protocol['image_url']}"
                ET.SubElement(image, 'image:title').text = f"{protocol['name']} Protocol"
                ET.SubElement(image, 'image:caption').text = protocol.get('description', '')[:160]
                
        # Add protocol PDF pages
        for protocol in protocols:
            url = ET.SubElement(urlset, 'url')
            ET.SubElement(url, 'loc').text = f"{self.base_url}/api/protocols/{protocol['id']}/pdf"
            ET.SubElement(url, 'lastmod').text = protocol.get('last_updated', self.last_modified)[:10]
            ET.SubElement(url, 'changefreq').text = 'monthly'
            ET.SubElement(url, 'priority').text = '0.6'
            
        # Convert to string
        ET.indent(urlset, space="  ", level=0)
        return ET.tostring(urlset, encoding='unicode', xml_declaration=True)
        
    def generate_robots_txt(self) -> str:
        """Generate robots.txt file"""
        return f"""User-agent: *
Allow: /

# Sitemaps
Sitemap: {self.base_url}/sitemap.xml
Sitemap: {self.base_url}/protocol-sitemap.xml

# Disallow admin and API documentation
Disallow: /admin/
Disallow: /api/docs/
Disallow: /api/redoc/

# Allow important API endpoints for SEO
Allow: /api/protocols/*/pdf
Allow: /api/protocols/library/

# Crawl delay for respectful crawling
Crawl-delay: 1

# Specific instructions for major search engines
User-agent: Googlebot
Allow: /
Crawl-delay: 0

User-agent: Bingbot  
Allow: /
Crawl-delay: 1

User-agent: Slurp
Allow: /
Crawl-delay: 2
"""

    def generate_protocol_sitemap(self) -> str:
        """Generate specific sitemap for protocol pages"""
        urlset = ET.Element('urlset')
        urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        urlset.set('xmlns:image', 'http://www.google.com/schemas/sitemap-image/1.1')
        
        protocols = master_protocol_manager.all_protocols
        
        for protocol in protocols:
            url = ET.SubElement(urlset, 'url')
            protocol_slug = protocol['name'].lower().replace(' ', '-').replace('/', '-')
            
            # Main protocol page
            ET.SubElement(url, 'loc').text = f"{self.base_url}/protocol/{protocol['id']}/{protocol_slug}"
            ET.SubElement(url, 'lastmod').text = protocol.get('last_updated', self.last_modified)[:10]
            ET.SubElement(url, 'changefreq').text = 'monthly'
            ET.SubElement(url, 'priority').text = '0.9'
            
            # Add structured data about the protocol
            if protocol.get('clinical_indications'):
                # This helps search engines understand the medical content
                pass
                
        ET.indent(urlset, space="  ", level=0)
        return ET.tostring(urlset, encoding='unicode', xml_declaration=True)

# Global sitemap generator
sitemap_generator = SitemapGenerator()
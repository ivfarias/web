from bs4 import BeautifulSoup
from collections import deque
import json
import requests
import xml.etree.ElementTree as ET

def fetch_sitemap_urls(sitemap_url):
    response = requests.get(sitemap_url)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    urls = []
    for url_element in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
        url = url_element.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text.strip()
        urls.append({'url': url})
    return urls

def fetch_metadata(url, exclude_ids=['consentPopup'], exclude_classes=['testimonials', 'pricing-section', 'faq_section', 'blog_list', 'main_footer', 'new_navbar', 'blog_detail_wrapper', 'div_pc_button', 'blog_detail_inner', 'author_bio', 'post_cta', 'main_blog_section', 'uui-navbar03_component', 'lead-form', 'testimonials', 'pricing-section', 'faq_section', 'blog_list', 'section-kyte', 'uui-footer05_component', 'feature_section_cms']):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('title')
        meta_title = title.text if title else None

        description = soup.find('meta', attrs={'name': 'description'})
        meta_description = description['content'] if description else None

        # Find the main content of the page
        body = soup.body
        if body:
            # Ignore head and footer elements
            for unwanted in body(['header', 'footer']):
                unwanted.extract()

            # Remove any excluded elements
            if exclude_ids:
                for excluded in body.find_all(id=exclude_ids):
                    excluded.extract()

            if exclude_classes:
                for excluded in body.find_all(class_=exclude_classes):
                    excluded.extract()

            # Get the text content of the body element
            body_text = body.get_text()
        else:
            body_text = None

        content_length = len(body_text) if body_text else 0
        content_tokens = len(body_text.split()) if body_text else 0

        return {
            'url': url,
            'title': meta_title,
            'description': meta_description,
            'content': body_text,
            'content_length': content_length,
            'content_tokens': content_tokens
        }

    except (requests.exceptions.Timeout, requests.exceptions.RequestException):
        print(f"Error: Could not fetch metadata for {url}")
        return None


def chunk_content(metadata, chunk_size=200):
    words = metadata['body'].split()
    chunked_contents = []
    chunk = deque(maxlen=chunk_size)

    for word in words:
        if len(chunk) < chunk_size:
            chunk.append(word)
        else:
            chunked_contents.append(' '.join(list(chunk)))
            chunk.append(word)

    # append remaining words in the last chunk
    if len(chunk) > 0:
        chunked_contents.append(' '.join(list(chunk)))

    chunks = []
    for chunk in chunked_contents:
        chunks.append({
            'title': metadata['meta_title'],
            'description': metadata['meta_description'],
            'url': metadata['url'],
            'content': chunk,
            'content_length': len(chunk),
            'content_tokens': len(chunk.split())
        })
    return chunks

sitemap_url = "https://www.kyte.com.br/sitemap.xml"
urls = fetch_sitemap_urls(sitemap_url)

metadata_list = []
for url_info in urls:
    url = url_info["url"]
    metadata = fetch_metadata(url)
    if metadata is None:
        continue
    chunked_contents = chunk_content(metadata)
    metadata['chunks'] = chunked_contents
    metadata_list.append(metadata)

# Save metadata_list to a JSON file
with open("metadata.json", "w") as f:
    json.dump(metadata_list, f, ensure_ascii=False, indent=2)
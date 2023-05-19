import requests
import json
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def fetch_sitemap_urls(sitemap_url):
    response = requests.get(sitemap_url)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    urls = []
    for url_element in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
        url = url_element.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text.strip()
        urls.append({'url': url})
    return urls

def fetch_metadata(url, exclude_ids=None, exclude_classes=None):
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

        return {
            'url': url,
            'meta_title': meta_title,
            'meta_description': meta_description,
            'body': body_text
        }

    except (requests.exceptions.Timeout, requests.exceptions.RequestException):
        raise HTTPException(status_code=500, detail=f"Error: Could not fetch metadata for {url}")



@app.get('/', response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post('/scrape')
def scrape(sitemap_url: str, exclude_ids: str = '', exclude_classes: str = ''):
    urls = fetch_sitemap_urls(sitemap_url)

    exclude_ids = exclude_ids.split(',') if exclude_ids else []
    exclude_classes = exclude_classes.split(',') if exclude_classes else []

    metadata_list = []
    for url_info in urls:
        url = url_info["url"]
        metadata = fetch_metadata(url, exclude_ids=exclude_ids, exclude_classes=exclude_classes)
        if metadata:
            metadata_list.append(metadata)

    # Save metadata_list to a JSON file
    with open("metadata.json", "w") as f:
        json.dump(metadata_list, f, ensure_ascii=False, indent=2)

    return metadata_list

@app.get('/download')
def download():
    # Send the metadata.json file as a download
    return FileResponse('metadata.json', media_type='application/json', filename='metadata.json')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

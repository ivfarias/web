import os
import requests
import markdown
import frontmatter
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
input_folder = "./inputs"
intercom_api_url = "https://api.intercom.io/articles"
intercom_auth_token = os.getenv("INTERCOM_AUTH_TOKEN")
intercom_author_id = 2044159

headers = {
    "accept": "application/json",
    "Intercom-Version": "2.8",
    "content-type": "application/json",
    "authorization": f"Bearer {intercom_auth_token}",
}


def convert_markdown_to_html(markdown_content):
    return markdown.markdown(markdown_content)


def send_tutorial_to_intercom(payload):
    response = requests.post(intercom_api_url, json=payload, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        print("Payload:")
        print(payload)
        return None

    response.raise_for_status()
    return response.json()


def process_markdown_file(file_path, language, parent_article_id=None, translated_content=None):
    with open(file_path, "r", encoding="utf-8") as file:
        markdown_content = file.read()

    fm = frontmatter.loads(markdown_content)

    title = fm.get("title", os.path.splitext(os.path.basename(file_path))[0])
    description = fm.get("description", "")

    html_content = convert_markdown_to_html(fm.content)

    payload = {
        "title": title,
        "description": description,
        "body": html_content,
        "author_id": intercom_author_id,
        "state": "draft"
    }

    if translated_content:
        payload["translated_content"] = translated_content
    elif parent_article_id and language != "en":
        payload["parent_article_id"] = parent_article_id

    response = send_tutorial_to_intercom(payload)
    return response


def process_language_folder(language_folder, filenames):
    language_folder_path = os.path.join(input_folder, language_folder)
    language_code = language_folder

    for file_name in filenames:
        file_path = os.path.join(language_folder_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                markdown_content = file.read()

            fm = frontmatter.loads(markdown_content)

            title = fm.get("title", os.path.splitext(os.path.basename(file_path))[0])
            description = fm.get("description", "")

            html_content = convert_markdown_to_html(fm.content)

            return language_code, {
                "type": "article_content",
                "title": title,
                "description": description,
                "body": html_content,
                "author_id": intercom_author_id,
                "state": "draft"
            }
    return None, None



def process_all_markdown_files():
    en_folder = "en"
    en_folder_path = os.path.join(input_folder, en_folder)

    for file_name in os.listdir(en_folder_path):
        if file_name.endswith(".md"):
            translated_content = {}

            # Process translations first
            for language_folder in os.listdir(input_folder):
                if language_folder != en_folder:
                    language_folder_path = os.path.join(input_folder, language_folder)
                    if os.path.isdir(language_folder_path):
                        lang_code, response = process_language_folder(language_folder, [file_name])
                        if response:
                            translated_content[lang_code] = response

            # Now process the English file with the associated translations
            en_response = process_markdown_file(os.path.join(en_folder_path, file_name), en_folder, translated_content=translated_content)
            print(f"Uploaded tutorial '{en_response['title']}' to Intercom (en).")

if __name__ == "__main__":
    process_all_markdown_files()

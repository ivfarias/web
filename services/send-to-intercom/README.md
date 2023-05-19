# Send to Intercom

This Python script uploads tutorial articles in Markdown format to Intercom, along with their translations. It reads the English version of the article and its translations, and creates an article on Intercom with the associated translations.

## Requirements

- Python 3.7+
- `requests` library
- `frontmatter` library
- `markdown` library
- `python-dotenv` library

You can install the required libraries using pip:

`pip install -r requirements.txt`

## Usage

Place the English articles in the ./inputs/en folder, and translations in their respective language folders (e.g. ./inputs/pt-BR for Brazilian Portuguese).
Make sure you have a .env file in the project root directory with your Intercom API token:
INTERCOM_AUTH_TOKEN=<your_intercom_auth_token>

### Run the script:

`python3 sender.py`

The script will upload each English article to Intercom and associate it with the translations from the corresponding folders.

## File structure

The script expects the following file structure:

```
.
├── inputs
│   ├── en
│   │   ├── article1.md
│   │   └── article2.md
│   ├── pt-BR
│   │   ├── article1.md
│   │   └── article2.md
│   └── es
│       ├── article1.md
│       └── article2.md
├── sender.py
└── .env
```

Each markdown file should include a frontmatter section with the title and description fields:

```
---
title: Set up your online catalog
description: Set up your online catalog and allow your customers to place orders and make purchases through it.
---
```

The filenames for the translations should be the same as their corresponding English articles.

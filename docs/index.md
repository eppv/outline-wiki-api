# Outline Wiki Python API

A minimalist library providing python API for [Outline](https://www.getoutline.com) knowledge base platform.
For full Outline API documentation visit [Outline Developers page](https://www.getoutline.com/developers).

> [!WARNING]
> Relevant for version [0.82.0](https://github.com/outline/outline/releases/tag/v0.82.0)

---

## Installation

```bash
python3 -m pip install outline-wiki-api
```

---
## Basic usage

### Creating a new document

Let's create a document in a `Welcome` collection:
```python
from outline_wiki_api import OutlineWiki

OUTLINE_URL = "https://my.outline.com"
OUTLINE_TOKEN = "mysecrettoken"

app = OutlineWiki(url=OUTLINE_URL, token=OUTLINE_TOKEN)
my_collection_name = "Welcome"

# Search for the Welcome collection to create a new doc there
for collection in app.collections.list().data:
    if collection.name == my_collection_name:
        print(collection)
        new_doc = app.documents.create(
            title="New Document Created From Outline Wiki API",
            text="""Some Markdown text here
Visit [outline-wiki-api GitHub](https://github.com/eppv/outline-wiki-api)
""",
            collection_id=collection.id,
            publish=True
        )
        print(f"New document created in collection {my_collection_name}:\n{new_doc}")
```

### Searching documents

```python
from outline_wiki_api import OutlineWiki

# You can also set OUTLINE_URL and OUTLINE_TOKEN as environment variables
app = OutlineWiki()

# Execute the search query
search_results = app.documents.search(query='outline').data

# Look at the results
for result in search_results:
    print(f"ranking: {result.ranking}")
    print(f"context: {result.context}")
    print(f"document: {result.document}")
```

# Outline Wiki Python API

A python wrapper for [Outline](https://www.getoutline.com) knowledge base platform API.

For full Outline API documentation visit [Outline Developers page](https://www.getoutline.com/developers).

> [!NOTE]
> Relevant for Outline version [0.82.0](https://github.com/outline/outline/releases/tag/v0.82.0)

> [!IMPORTANT]
> The main branch may be in an unstable or even broken state during development. For stable versions, see releases.

---
## Installation

```bash
python3 -m pip install outline-wiki-api
```

---

## Usage

Let's try to search a document in our knowledge base and look through the results:

```python
from outline_wiki_api import OutlineWiki

# You can also set OUTLINE_URL and OUTLINE_TOKEN as environment variables
OUTLINE_URL = "https://my.outline.com"
OUTLINE_TOKEN = "mysecrettoken"

app = OutlineWiki()

search_results = app.documents.search(query='outline').data

for result in search_results:
    print(f"ranking: {result.ranking}")
    print(f"context: {result.context}")
    print(f"document: {result.document}")
```

You can find more usage examples [in the docs](https://eppv.github.io/outline-wiki-api).

[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)

---

# License

This library is a wrapper, not affiliated with Outline.

Outline itself is [BSL 1.1 licensed](https://github.com/outline/outline/blob/main/LICENSE).

Use of Outline’s API via this wrapper must comply with Outline's licensing terms.

The original code of the wrapper is under the Apache 2.0 license. See the []LICENSE](https://github.com/eppv/outline-wiki-api/blob/main/LICENSE) file for details.


## Basic usage

=== "Creating a new document"

    ``` py linenums="1"
    from outline_wiki_api import OutlineWiki

    OUTLINE_URL = "https://my.outline.com"
    OUTLINE_TOKEN = "mysecrettoken"

    app = OutlineWiki(url=OUTLINE_URL, token=OUTLINE_TOKEN)
    my_collection_name = "Welcome"

    for collection in app.collections.list().data: # (1)
        if collection.name == my_collection_name:
            print(collection)
            new_doc = app.documents.create(
                title="Document from API 🔥",
                text="""Some Markdown text here 🦊""",
                collection_id=collection.id,
                publish=True
            )
            print(f"New document created in collection {my_collection_name}:\n{new_doc}")
    ```

    1.  Search for the **"Welcome"** collection to create a new doc there

=== "Search documents"

    ``` py linenums="1"
    from outline_wiki_api import OutlineWiki

    app = OutlineWiki() # (1)
    search_results = app.documents.search(query='outline').data # (2)

    for result in search_results: # (3)
        print(f"ranking: {result.ranking}")
        print(f"context: {result.context}")
        print(f"document: {result.document}")
    ```

    1.  You can also set `OUTLINE_URL` and `OUTLINE_TOKEN` as environment variables
    2.  Execute the search query
    3.  Look at the results


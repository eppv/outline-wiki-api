
## Basic usage

### Interface
`OutlineWiki` is a full-featured Python interface that contains an HTTP client and provides access to all the resources and functions of the application API.

You can create the interface with different options.

=== "Explicitly set URL and token for the client"

    ``` py linenums="1"
    from outline_wiki_api import OutlineWiki

    OUTLINE_URL = "https://my.outline.com"
    OUTLINE_TOKEN = "mysecrettoken" # (1)

    app = OutlineWiki(url=OUTLINE_URL, token=OUTLINE_TOKEN)
    ```

    1. The token can be generated in the account settings.

=== "Set URL and token automatically or using environment variables"

    ``` py linenums="1"
    from outline_wiki_api import OutlineWiki # (1)

    app = OutlineWiki() # (2)
    ```

    1. By default, `OutlineWiki` uses URL `https://app.getoutline.com`. However, token MUST be set by the user.
    2. You can set `OUTLINE_URL` and `OUTLINE_TOKEN` as environment variables.

=== "Set logging level to DEBUG"

    ``` py linenums="1"
    from outline_wiki_api import OutlineWiki

    app = OutlineWiki(logging_level=logging.DEBUG) # (1)
    ```

    1. `OutlineWiki` uses the standard Python `logging` module, so setting DEBUG level to `logging.basicConfig` will also work.

### Documents

`Documents` is the central type of resources in Outline.

You can do all kinds of stuff with it using the API.

=== "Search documents (full-text)"

    ``` py linenums="1"
    from outline_wiki_api import OutlineWiki

    app = OutlineWiki()
    search_results = app.documents.search(query='outline').data # (1)

    for result in search_results:  # (2)
    print(f"document_title: {result.document.title} | "
          f"ranking: {result.ranking} | "
          f"context: {result.context[0:20].replace('\n', ' ')}\n")
    ```

    1.  Execute the search query
    2.  Look at the results


=== "Create new document"

    ``` py linenums="1"
    from outline_wiki_api import OutlineWiki

    app = OutlineWiki()
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
            print(f"New document created in collection {my_collection_name}:\n{new_doc.data.title}")
    ```

    1.  Search for the **"Welcome"** collection to create a new doc there

=== "Import document from a file"

    ``` py linenums="1"
    from outline_wiki_api import OutlineWiki

    app = OutlineWiki()

    my_collection_id = "ff3c58ac-f134-46b2-8601-876dc494044a" # (1)
    my_file = 'path/to/some_markdown_document.md' # (2)

    document = app.documents.import_file(file=my_file, collection_id=my_collection_id).data # (3)
    ```

    1. `collection_id` is essential argument. It points to the collection where the imported document will be created.
    2. Plain text, markdown, docx, csv, tsv, and html file formats are supported for import.
    3. You can also pass a file object to the file argument, intended for transmission as part of a `multipart/form-data` request. You can create such an object yourself, or using the function `outline_wiki_api.utils.get_file_object_for_import`.

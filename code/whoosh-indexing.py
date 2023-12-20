import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, KEYWORD, ID
from whoosh.qparser import QueryParser
from whoosh.qparser.plugins import FuzzyTermPlugin
from whoosh.spelling import Corrector


# Define the schema
schema = Schema(
    url=ID(unique=True, stored=True),
    content=TEXT(stored=True),
    tags=KEYWORD,
    path=ID(unique=True, stored=True)
)

# Specify the source folder containing text documents
source_folder = "output_files"

# Specify the destination folder for the Whoosh index
index_path = "output_files_whoosh_main"
if not os.path.exists(index_path):
    os.mkdir(index_path)

# Create an index
index = create_in(index_path, schema)

# Create a writer
writer = index.writer()

# Function to extract URL and content from a document
def extract_url_and_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        # Read the first line to extract the URL
        first_line = file.readline().strip()
        if first_line.startswith("URL:"):
            url = first_line[len("URL:"):].strip()
        else:
            url = "URL not found"

        # Read the remaining lines as content
        content = file.read().strip()

    return url, content

# Index documents
for filename in os.listdir(source_folder):
    if filename.endswith(".txt"):  # Adjust the file extension if needed
        file_path = os.path.join(source_folder, filename)
        url, content = extract_url_and_content(file_path)

        # Add document to the index
        doc = {"url": url, "content": content, "tags": [], "path": file_path}
        writer.add_document(**doc)

# Commit changes
writer.commit()

# ana = analysis.StemmingAnalyzer()
# schema = fields.Schema(text=TEXT(analyzer=ana, spelling=True))
# corrector = searcher.corrector("content")

# Example search with fuzzy term plugin
searcher = index.searcher()
query_parser = QueryParser("content", schema=schema)
query_parser.add_plugin(FuzzyTermPlugin())  # Add the FuzzyTermPlugin to the QueryParser

# Example normal search query
normal_query_string = "cancer"  # Adjust the search query
fuzzy_query_string = normal_query_string + "~1"  # Convert to fuzzy query

# Example fuzzy search
query = query_parser.parse(fuzzy_query_string)
results = searcher.search(query, limit=10)  # Set the limit to retrieve top 10 results

# Print top 10 search results
print("\nTop 10 Fuzzy Search Results for '{}':".format(normal_query_string))
for i, result in enumerate(results, 1):
    print(f"{i}. URL: {result['url']}, Path: {result['path']}")

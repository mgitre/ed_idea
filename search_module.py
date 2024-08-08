import os
import yaml
from modified_citation_query_engine import CitationQueryEngine
from llama_index.core import (
    StorageContext,
    load_index_from_storage,
)

with open('config.yaml') as f:
    config = yaml.safe_load(f)

os.environ['OPENAI_API_KEY'] = config['openai_key']

# load the documents
# check if storage already exists
PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    print("It looks like you don't have an index yet. Please run load_documents.py and generate_embeddings.py first.")
else:
    print("Loading existing index (this may take a while)")
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

# search function
# similarity_top_k is how many of the most similar documents to pull from the corpus and feed to the LLM.
# a higher number, up to a certain point, may give slightly better results but will be slower and more costly
def search(query, similarity_top_k=6):
    citation_query_engine = CitationQueryEngine.from_args(
        index,
        similarity_top_k=similarity_top_k,
        # here we can control how granular citation sources are, the default is 512
        citation_chunk_size=256,
    )
    return citation_query_engine.query(query)
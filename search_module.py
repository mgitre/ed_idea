import os
import yaml

with open('config.yaml') as f:
    config = yaml.safe_load(f)

os.environ['OPENAI_API_KEY'] = config['openai_key']

import pickle
from modified_citation_query_engine import CitationQueryEngine
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)

# load the documents
# check if storage already exists
PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    print("Creating new index")
    # load the documents and create the index
    with open('documents.pkl', 'rb') as f:
        documents = pickle.load(f)
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    print("Loading existing index")
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)



def search(query, similarity_top_k=6):
    citation_query_engine = CitationQueryEngine.from_args(
        index,
        similarity_top_k=similarity_top_k,
        # here we can control how granular citation sources are, the default is 512
        citation_chunk_size=256,
    )
    return citation_query_engine.query(query)
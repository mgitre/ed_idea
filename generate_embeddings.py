import os
import yaml
import pickle
from llama_index.core import (
    VectorStoreIndex,
)

# set up the OpenAI API key
with open('config.yaml') as f:
    config = yaml.safe_load(f)
os.environ['OPENAI_API_KEY'] = config['openai_key']


# check if storage already exists
PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    print("Creating new index (this may take a while)")
    # load the documents and create the index
    with open('documents.pkl', 'rb') as f:
        documents = pickle.load(f)
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    print("It looks like you already have an index. If you want to create a new one, delete the storage directory and run this script again.")
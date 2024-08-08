#read in the data.json file, clean it up, and put it into LlamaIndex documents format

#imports!
import json
import pickle
from llama_index.core import Document

#load the data
with open("data.json", "r") as f:
    data = json.load(f)

#cleanup
#for every entry in data, we want to look at the docs and hopefully get rid of duplicates and other messy stuff
#we want to remove any documents that are less than 100 characters long
#then, if we see any 2 docs whose titles are the same except one ends in MS WORD and one ends in PDF then we only want to keep the MS WORD one
#(this is because sometimes the same document is available in both formats, and the MS WORD one is usually easier to extract text from)
for entry in data:
    docs = entry["docs"]
    new_docs = []
    for i in range(len(docs)):
        if len(docs[i][2]) < 100:
            continue
        if docs[i][1].lower().endswith("pdf"):
            if any(docs[j][1].lower().endswith("ms word") and docs[j][1].lower().replace("ms word", "").replace("word","").strip() == docs[i][1].lower().replace("pdf", "").strip() for j in range(len(docs))):
                continue
        new_docs.append(docs[i])
    entry["docs"] = new_docs

#now we want to put the data into LlamaIndex documents format
def get_documents(entry):
    #for each document in the entry, create a document object
    #metadata fields:
    #   parent_title (passed to embedder and LLM)
    #   document_title (passed to embedder and LLM)
    #   parent_link (not used)
    #   document_link (not used)
    #   topic_area (passed to embedder)
    #   description (passed to embedder)
    #text field: document text (we have this)
    parent_title = entry['title']
    parent_link = entry['link']
    topic_area = entry['topic_area']
    description = entry['description']
    documents = []
    for doc in entry['docs']:
        document_title = doc[1]
        document_text = doc[2]
        document = Document(text=document_text, metadata={"parent_title": parent_title, "document_title": document_title, "parent_link": parent_link, "document_link": doc[0], "topic_area": topic_area, "description": description})
        document.excluded_embed_metadata_keys = ["parent_link", "document_link"]
        document.excluded_llm_metadata_keys = ["parent_link", "document_link", "topic_area", "description"]
        documents.append(document)
    return documents

documents = sum([get_documents(entry) for entry in data], [])

#save the documents to a pickle file
with open("documents.pkl", "wb") as f:
    pickle.dump(documents, f)
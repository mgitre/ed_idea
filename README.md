# LlamaIndex retreival-augmented generation demo with Department of Education IDEA policy letters

## Introduction
This repository contains an example for using LlamaIndex to generate informative, well-cited responses from a corpus of documents.

## Getting started
Make sure you've installed all dependencies by running `pip install -r requirements.txt`. Then copy `config_template.yaml` to `config.yaml` and fill in each field with the appropriate information.

Now it's time to load the data! `load_documents.py` loads documents from the existing `data.json` file, which all the IDEA letters have already been downloaded to, and saves them as LlamaIndex documents. Alternatively, `scrape_for_llamaindex.ipynb` is a Jupyter notebook that scrapes the Department of Education's IDEA policy letters and saves them (NOTE: this requires an installation of antiword to read .doc files). Take inspiration from either of these if you'd like to load other documents into a LlamaIndex-ready format. Both will output a `documents.pkl` file that will be used by other scripts.

## How LlamaIndex works
LlamaIndex uses a 3-step process for generating responses from a corpus of documents. First, it generates embeddings for each document in the corpus. This only needs to be done once--your documents don't change! Then, LlamaIndex uses those embeddings to find the most relevant documents to a given query. Finally, it generates a response from those documents. 

NOTE: Before you can use LlamaIndex, make sure you've set your OpenAI API key in the `config.yaml` file!

## Generating embeddings
To generate embeddings for your documents, run `generate_embeddings.py`. This script will load the documents from `documents.pkl` and save a VectorStoreIndex in `./storage/`. This also only needs to be done once!

## Querying LlamaIndex
`search_module.py` provides a search function that takes a query and returns a response along with the most relevant snippets from the documents that were used to generate that response. This script will load the VectorStoreIndex from `./storage/`.

## Hosting an API
`flask_demo.py` provides a simple Flask API that can be used to query our corpus using `search_module.py`. To start the API, run `flask_demo.py` and then query it using a POST request where the body is a JSON object with a `query` field. The response will be a JSON object with a `response` field containing the generated response and a `sources` field containing the sources used. This is useful for integrating LlamaIndex content into other applications.
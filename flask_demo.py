#import YAML for config
import yaml
#import flask stuff for an API
from flask import Flask, request, jsonify
from flask_cors import CORS
from search_module import search

#load the config file
#we care about keys under 'flask': port, host
with open('config.yaml') as f:
    config = yaml.safe_load(f)

#we really only need 1 endpoint for this--query
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
                        
@app.route('/query', methods=['POST'])
def query():
    query = request.json['query']
    response = search(query)
    response_text = response.response
    source_nodes = response.source_nodes
    #from each source node, we want the metadata and the text
    sources = [(node.get_text(), node.metadata) for node in source_nodes]
    return jsonify({
        'response': response_text,
        'sources': sources
    })

if __name__ == '__main__':
    app.run(host=config['flask']['host'], port=config['flask']['port'], debug=True)
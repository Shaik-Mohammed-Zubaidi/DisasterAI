from flask import Flask, request, jsonify
from flask_cors import CORS
from data_scraping import get_search_results
from model import get_answer_rag, load_documents

app = Flask(__name__)

# Enable CORS for the Flask app, allowing requests from http://localhost:3000
CORS(app, origins=["http://localhost:3000"])

@app.route('/')
def home():
    query = request.args.get('query')
    if query:
        print(f"Query received: {query}")
        print("Getting search results...")
        get_search_results(query)
        print("Loading documents...")
        documents = load_documents()
        answer = get_answer_rag(query, documents)
        return jsonify({'message': answer})
    else:
        return jsonify({'message': 'Please provide a query parameter'})

@app.route('/test')
def test():
    return jsonify({'message': 'Hello from Flask!'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
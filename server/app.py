from flask import Flask, request
from data_scraping import get_search_results

app = Flask(__name__)

@app.route('/')
def home():
    query = request.args.get('query')
    if query:
        print(f"Query received: {query}")
        print("Getting search results...")
        get_search_results(query)
        return "Search results saved successfully!"
    else:
        return "Need a valid query parameter!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
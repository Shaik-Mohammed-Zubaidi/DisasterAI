import requests
import os
import re
from dotenv import load_dotenv
from bs4 import BeautifulSoup
# from pinata import upload_text_file  # Import the upload function

load_dotenv()

def google_search(query, api_key, cse_id, num_results=5, exactTerms=''):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': api_key,
        'cx': cse_id,
        'num': num_results,
        'exactTerms': exactTerms,
    }
    
    response = requests.get(url, params=params, timeout=5)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

def extract_links_from_results(results):
    """Extracts only .gov links from search results."""
    return [item['link'] for item in results.get('items', []) if '.gov' in item['link']]


def format_results_as_text(results):
    """Formats the Google search results into a string."""
    formatted_results = []
    for i, item in enumerate(results.get('items', []), start=1):
        title = item['title']
        snippet = item.get('snippet', '')
        link = item['link']
        formatted_results.append(f"{i}. {title}\n{snippet}\n{link}\n")
    return "\n".join(formatted_results)

# Replace with your own API key and Custom Search Engine ID
API_KEY = os.getenv('GOOGLE_API_KEY')
CSE_ID = os.getenv('CSE_ID')
NO_OF_RESULTS = 10
# EXACT_TERMS = 'call'

data_folder = './rag_data'

# query = "Hurricane helene helplines"
def get_search_results(query):
    results = google_search(query, API_KEY, CSE_ID, NO_OF_RESULTS)

    # Format search results to text
    formatted_results = format_results_as_text(results)
    # Save search results locally
    folder_path = os.path.join(data_folder, 'search_results')
    os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist
    file_path = os.path.join(folder_path, f"{query}_search_results.txt")

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(formatted_results)

    print(f"Search results saved to {file_path}")

    # Extract links from the search results
    links = extract_links_from_results(results)

    # Print the list of extracted links
    for link in links:
        print(link)

    # Save content from each URL locally
    # content_folder = './webpage_contents/'+ query
    content_folder = os.path.join(data_folder, 'webpage_contents', query)
    os.makedirs(content_folder, exist_ok=True)  # Create folder if it doesn't exist

    # Loop over each URL and extract content
    for idx, url in enumerate(links, start=1):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Ensure request was successful
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the main content from the page (assuming <p> tags)
            content = "\n".join(paragraph.get_text() for paragraph in soup.find_all('p'))

            # Save the content to a local text file
            content_file_path = os.path.join(content_folder, f"webpage_content_{idx}.txt")
            with open(content_file_path, 'w', encoding='utf-8') as file:
                file.write(content)

            print(f"Content from {url} saved to {content_file_path}")

        except requests.RequestException as e:
            print(f"Failed to retrieve content from {url}: {e}")

    print(f"\nContent from {len(links)} webpages saved locally.")

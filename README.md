# Disaster-AI Web App

### Overview:
Disaster-AI is a web application that provides real-time, relevant responses to user queries during disasters using a Retrieval-Augmented Generation (RAG) model. The app allows users to ask disaster-related questions and receive accurate information instantly. Key features include:

- **Text-based query input**: Users can type questions about disaster relief, safety tips, or other calamity-related concerns.
- **Real-time responses**: The system fetches relevant content using a large language model (T5-large).
- **Web-based platform**: Accessible on any browser with a clean, easy-to-use interface.
- **Potential offline functionality** (future update).

---

### Features:
- **Quick Help via Text Box**: Users input questions in a text box and receive instant responses.
- **Calamity-Specific Information**: Users can ask questions on various aspects of a disaster, from preparedness to recovery.
- **Real-time, Accurate Responses**: The app utilizes a RAG-based approach to ensure responses are relevant and timely.

---

### Prerequisites:
Before running the project, ensure you have the following installed:
- [Node.js](https://nodejs.org/) (v14 or above)
- [npm](https://www.npmjs.com/) (comes with Node.js)
- Google Programmable Search Engine setup (see below)

---

### Google Programmable Search Engine (CSE) Setup
To integrate Google’s Programmable Search Engine (CSE) into Disaster-AI, follow these steps to set up CSE and obtain your API key and CSE_ID:

1. **Access Google Cloud Platform**:
   - Go to the [Google Cloud Platform Console](https://console.cloud.google.com/).
   - Sign in with your Google account.
   - Create a new project if needed, or select an existing one.

2. **Enable the Custom Search API**:
   - Navigate to "APIs & Services" on the left menu.
   - Search for "Custom Search API" and enable it.

3. **Obtain Your API Key**:
   - Go to "Credentials" in the left menu.
   - Click "Create credentials" and select "API key."
   - Copy the generated API key.

4. **Create a Programmable Search Engine**:
   - Go to the [Google Custom Search Engine control panel](https://cse.google.com/cse/all).
   - Click "Add" to create a new search engine.
   - Provide a name and specify which websites to include in the search.
   - Click "Create."

5. **Find Your CSE_ID**:
   - Go to the "Overview" page of your search engine.
   - Locate the "Search Engine ID" (or "cx"), which will be your `CSE_ID`.

**Key Points**:
   - **API Key Usage**: Include your API key as a parameter in API requests to the custom search engine.
   - **CSE_ID Usage**: Use `CSE_ID` (or "cx") to identify your specific search engine in API calls.
   - **Customization**: Further customize your search engine within the CSE control panel, adjusting features like ranking and look & feel.

---

### Installation Instructions:

1. **Clone the repository**:
   ```bash
   git clone <repo-link>
   cd <repo-directory>
   ```

2. **Install dependencies**:

   For the backend:
   ```bash
   cd server
   pip install -r requirements.txt 
   ```

   For the frontend:
   ```bash
   cd client
   npm install
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory and add your configuration details (API keys, database connection strings, etc.). Example:
   ```
   GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
   CSE_ID=YOUR_GOOGLE_CSE_ID
   PORT=5000
   REACT_APP_API_URL=http://localhost:5000
   ```

4. **Run the app**:
   Start the server (back-end):
   ```bash
   cd server
   python app.py
   ```

   Start the front-end (React):
   ```bash
   cd client
   npm start
   ```

   The app will be available on `http://localhost:3000`.

---

### How to Use:
1. Open your browser and navigate to `http://localhost:3000`.
2. Type a disaster-related query in the text box, such as "hurricane helpline number."
3. Submit to receive real-time responses related to your question.

---

### Contributing:
Feel free to contribute by submitting issues or pull requests. Feedback and suggestions to improve the app are always welcome!
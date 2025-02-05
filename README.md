# CMS Admin Interface for Content Management System

## Description
This is a simple CMS built with Flask to manage words and phrases stored in a local SQLite database. It allows administrators to view, edit, update, and search entries. The application automatically loads initial data from a remote JSON file.

## Setup and Running Instructions

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/cms-flask.git
    cd cms-flask
    ```

2. **Create a Virtual Environment and Install Dependencies:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Run the Application:**
    ```bash
    python app.py
    ```

4. **Access the CMS:**
    Open your web browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Features
- **View Words and Phrases:** Paginated list with search functionality.
- **Edit Entries:** Update the word/phrase, translation, and example sentence.
- **Data Initialization:** Loads initial data from the provided JSON URL on startup.

## Technical Stack
- **Backend:** Flask, Flask-SQLAlchemy, SQLite
- **Frontend:** HTML/CSS (Jinja2 templates)
- **Data Loading:** Requests (for fetching JSON)

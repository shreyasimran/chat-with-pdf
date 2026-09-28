# Chat with PDF

A Django-based Chat with PDF application built using **Retrieval-Augmented Generation (RAG)**, Gemini, embeddings, vector search, and OCR.

Upload PDF documents and ask questions about their content. The application retrieves relevant text from the documents and uses Gemini to generate context-based answers.

## Features

* Upload and process PDF documents
* Extract text from PDFs
* OCR support for scanned PDFs
* Split documents into smaller chunks
* Generate embeddings using Sentence Transformers
* Store and retrieve document chunks using ChromaDB
* Generate answers using the Gemini API
* Chat with information retrieved from uploaded PDFs
* Web interface built with Django, HTML, CSS, JavaScript, and Bootstrap

## Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML, CSS, JavaScript, Bootstrap
* **LLM:** Google Gemini
* **Embeddings:** Sentence Transformers
* **Vector Database:** ChromaDB
* **PDF Processing:** pypdf, PyMuPDF
* **OCR:** Tesseract OCR, pytesseract
* **Environment Variables:** python-dotenv

## Project Structure

```text
chat_with_pdf/
├── config/
├── data/
│   └── pdfs/
├── src/
│   ├── document_loader.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vector_store.py
│   └── llm.py
├── chat/
│   ├── templates/
│   └── static/
├── .env
├── .gitignore
├── app.py
├── manage.py
├── ocr_test.py
└── requirements.txt
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/shreyasimran/chat-with-pdf.git
cd chat-with-pdf
```

### 2. Create and activate a virtual environment

For Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If OCR dependencies are not included in `requirements.txt`, install them separately:

```bash
pip install pymupdf pytesseract pillow
```

### 4. Configure environment variables

Create a `.env` file in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own API key. Never commit your `.env` file or expose your API key publicly.

### 5. Configure Tesseract OCR

Install Tesseract OCR on your system. If it is installed in a custom location, update the executable path in the OCR-related Python code accordingly.

### 6. Run the Django application

```bash
python manage.py runserver
```

Open the local development URL shown in the terminal, usually:

`http://127.0.0.1:8000/`

## How It Works

1. Upload a PDF document.
2. Extract text from the PDF, using OCR when required.
3. Split the extracted text into chunks.
4. Convert the chunks into embeddings.
5. Store the embeddings in ChromaDB.
6. Retrieve relevant chunks when a user asks a question.
7. Send the retrieved context to Gemini to generate an answer.
8. Display the answer in the web interface.

## Security

* Keep API keys in environment variables.
* Do not upload `.env`, virtual environments, private documents, or other secrets to GitHub.
* Configure production security settings before deploying the application.

## Note

The current vector store uses in-memory storage, so indexed document data may be cleared when the server restarts. Uploaded PDFs and API keys are not included in this repository.

## Author

**Shreya Simran**

GitHub: [@shreyasimran](https://github.com/shreyasimran)

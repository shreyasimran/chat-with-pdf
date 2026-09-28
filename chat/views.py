from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from src.document_loader import load_pdf
from src.chunking import create_chunks
from src.embeddings import create_embeddings
from src.vector_store import (
    store_embeddings, retrieve_chunks,reset_collection,
    )
from src.llm import generate_answer

def home(request):

    if request.method == "POST":

        pdf_files = request.FILES.getlist("pdf")

        if pdf_files:

            reset_collection()


            fs = FileSystemStorage()

            uploaded_filenames = []

            for pdf_file in pdf_files:

                filename = fs.save(pdf_file.name, pdf_file)

                uploaded_filenames.append(filename)

                print("Saved file:", filename)

                pdf_path = fs.path(filename)
                print("PDF path:", pdf_path)

                pages = load_pdf(pdf_path)
                print("Total pages:", len(pages))

                chunks = create_chunks(pages)
                print("Total chunks:", len(chunks))

                if chunks:

                    chunk_texts = [
                        chunk["text"]
                        for chunk in chunks
                    ]

                    embeddings = create_embeddings(chunk_texts)

                    print(
                        "Embeddings shape:",
                        embeddings.shape
                    )

                    store_embeddings(
                        chunks,
                        embeddings,
                        filename
                    )

                    print("Chunks stored in ChromaDB")

                else:

                    print(
                        f"No text could be extracted from: {filename}"
                    )

            request.session["pdf_uploaded"] = True

            request.session["pdf_filenames"] = uploaded_filenames

            return redirect("ask")

    return render(request, "chat/home.html")


def ask(request):

    # User cannot access question page before uploading PDF
    if not request.session.get("pdf_uploaded"):
        return redirect("home")
    pdf_files = request.session.get("pdf_filenames", [])

    answer = None
    sources = []

    if request.method == "POST":

        question = request.POST.get("question")

        if question:

            print("User question:", question)
            selected_pdf = request.POST.get("pdf")
            print("SELECTED PDF:", selected_pdf)
            if selected_pdf != "all" and selected_pdf not in pdf_files:
                selected_pdf = None
            print("PDF AFTER VALIDTION:", selected_pdf)
            if selected_pdf=="all":
                retrieved_chunks = retrieve_chunks(
                question,
                n_results=4,
                filename=None
                )
            else:
                retrieved_chunks = retrieve_chunks(
                question,
                n_results=4,
                filename=selected_pdf
                )

            sources = [
            {
            "filename": chunk["filename"],
            "page_number": chunk["page_number"]
            }
    for chunk in retrieved_chunks
]

            print("RETRIEVED COUNT:", len(retrieved_chunks))
            print("\n===== RETRIEVED CHUNKS =====")

            for i, chunk in enumerate(retrieved_chunks, start=1):
                print(f"\nChunk {i}")
                print("Filename:", chunk.get("filename", "Not available"))
                print("Page:", chunk["page_number"])
                print("Distance:", chunk["distance"])
                print("Text:", chunk["text"])

            print("============================\n")


            context = "\n\n".join(
                chunk["text"]
                for chunk in retrieved_chunks
            )
            sources = [{
                "filename": chunk["filename"],
                "page_number": chunk["page_number"]
            }
            for chunk in retrieved_chunks]

            prompt = f"""
            You are a helpful assistant for answering questions about the uploaded PDF.

            Use only the information provided in the context below.

            Rules:
            1. Answer the question using only the provided context.
            2. Do not make up or assume information that is not present in the context.
            3. If the answer cannot be found in the context, say:
            "The answer is not available in the provided document."
            4. Give a clear and concise answer.
            5. Use headings and bullet points when useful.
            6. Include examples only when supported by the context.

            Context:
            {context}

            Question:
            {question}
            """

            answer = generate_answer(prompt)

    return render(
        request,
        "chat/ask.html",
        {
            "answer": answer,
            "pdf_files" : pdf_files,
            "sources": sources
        }
    )
#API key
from src.llm import generate_answer



                                   

#connect embeddings
from src.document_loader import load_pdf
from src.chunking import create_chunks
from src.embeddings import create_embeddings
pdf_path ="data/pdfs/botny.pdf"
pages =load_pdf(pdf_path)

chunks = create_chunks(pages)


chunk_texts = [chunk["text"] for chunk in chunks]
embeddings = create_embeddings(chunk_texts)
print("Total chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)
# import chromadb
from src.vector_store import store_embeddings, retrieve_chunks
store_embeddings(chunks, embeddings)
print("chunks stored in chromaDB")



#giving retrived chunks to llm to generate output

while True:

    question = input("\n Ask  question about the PDF: ")
    if question.lower() =="exit":
        break
    retrieved_chunks = retrieve_chunks(question, n_results=2)
    context = "\n\n".join(
        chunk["text"] for chunk in retrieved_chunks
    )

    prompt = f"""
Answer the question using only the context provided below.

Context:
{context}

Question:
{question}
"""

    answer = generate_answer(prompt)
    print("\nFinal Answer:")
    print(answer)

    print("\nSources:")
    pages = set()
    for chunk in retrieved_chunks:
        pages.add(chunk["page_number"])

    for page in sorted(pages):
        print(f"Page {page}")

    print("\nRetrieved Chunks:")

    for i, chunk in enumerate(retrieved_chunks, start=1):
        print(
            f"Chunk {i} |"
            f" Page {chunk['page_number']} |"
            f"Distance: {chunk['distance']:.4f}"
            )
       
import chromadb
client =chromadb.Client()
collection = client.get_or_create_collection(
    name="pdf_documents"
)
def reset_collection():
    global collection

    client.delete_collection(name="pdf_documents")

    collection = client.get_or_create_collection(
        name="pdf_documents"
    )
def store_embeddings(chunks, embeddings, filename):
    collection.add(
        ids=[
            f"{filename}_chunk_{i}"
            for i in range(len(chunks))
        ],
        documents=[
            chunk["text"]
            for chunk in chunks
        ],
        embeddings=embeddings.tolist(),
        metadatas=[
            {
                "filename": filename,
                "page_number": chunk["page_number"]
            }
            for chunk in chunks
        ]

    )

def retrieve_chunks(query, n_results=4, filename=None):

    # Specific PDF selected
    if filename:
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
            where={"filename": filename}
        )

        retrieved_chunks = []

        for document, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):
            retrieved_chunks.append({
                "text": document,
                "filename": metadata["filename"],
                "page_number": metadata["page_number"],
                "distance": distance
            })

        return retrieved_chunks

    # All PDFs selected
    all_data = collection.get(include=["metadatas"])
    metadatas = all_data.get("metadatas") or []

    filenames = sorted(set(
        metadata["filename"]
        for metadata in metadatas
        if metadata and metadata.get("filename")
    ))

    if not filenames:
        return []

    per_pdf_limit = max(
        1,
        (n_results + len(filenames) - 1) // len(filenames)
    )

    retrieved_chunks = []

    for pdf_name in filenames:
        results = collection.query(
            query_texts=[query],
            n_results=per_pdf_limit,
            include=["documents", "metadatas", "distances"],
            where={"filename": pdf_name}
        )

        for document, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):
            retrieved_chunks.append({
                "text": document,
                "filename": metadata["filename"],
                "page_number": metadata["page_number"],
                "distance": distance
            })

    retrieved_chunks.sort(key=lambda chunk: chunk["distance"])

    return retrieved_chunks[:n_results]
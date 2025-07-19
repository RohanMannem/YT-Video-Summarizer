from RAG.chunker import chunk_transcript
from RAG.embedder import embed_texts
from RAG.vector_store import VectorStore
from utils.fetch_transcript import fetch_transcript

def build_store(video_id: str, store_path: str = "vector_store") -> VectorStore:
    """
    Builds and saves a vector store from a YouTube video transcript.

    Args:
        video_url (str): Full YouTube video URL
        store_path (str): Folder to save the vector index and metadata

    Returns:
        VectorStore: An initialized and saved vector store
    """

    # 1. Fetch transcript
    transcript = fetch_transcript(video_id)
    if not transcript:
        raise ValueError("Failed to fetch transcript.")

    # 2. Chunk transcript
    chunks = chunk_transcript(transcript)
    if not chunks:
        raise ValueError("Transcript was empty or poorly chunked.")

    # 3. Embed chunks
    embedded_chunks = embed_texts(chunks)

    # 4. Build vector store
    store = VectorStore()
    store.add_embeddings(embedded_chunks)
    store.save(store_path)

    print(f"✅ Vector store saved to {store_path}")
    return store

from chunker import chunk_transcript
from embedder import embed_chunks
from vector_store import VectorStore
from ..utils.fetch_transcript import fetch_transcript

# 1. Fetch full transcript text
video_url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
transcript = fetch_transcript(video_url)  # returns full transcript as string

# 2. Chunk the transcript
chunks = chunk_transcript(transcript, max_tokens=500, overlap=100)

# 3. Embed the chunks
embedded_chunks = embed_chunks(chunks)  # returns [{"text": ..., "embedding": ...}, ...]

# 4. Create and populate the vector store
store = VectorStore()
store.index(embedded_chunks)

# 5. Save the vector store to disk
store.save("vector_store")
print("✅ Vector store saved!")

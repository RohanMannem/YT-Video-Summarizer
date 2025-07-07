import openai
import os
import time
import tiktoken

# Set your OpenAI API key (handle secrets elsewhere in production)
openai.api_key = os.getenv("OPENAI_API_KEY")

EMBED_MODEL = "text-embedding-3-small"  # or "text-embedding-3-large"

def num_tokens_from_string(text, model="gpt-3.5-turbo"):
    """Estimate token count using tiktoken (optional for debugging)"""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def embed_texts(texts, model=EMBED_MODEL, batch_size=10, delay=1):
    """
    Generate embeddings for a list of strings.

    Args:
        texts (List[str]): Chunks to embed.
        model (str): Embedding model.
        batch_size (int): How many texts to send per batch.
        delay (float): Seconds to wait between batches (avoid rate limits).

    Returns:
        List of dicts: [{"text": ..., "embedding": [...], "chunk_id": ...}, ...]
    """
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        try:
            response = openai.embeddings.create(input=batch, model=model)
            for j, record in enumerate(response.data):
                results.append({
                    "text": batch[j],
                    "embedding": record.embedding,
                    "chunk_id": i + j
                })
        except openai.RateLimitError:
            print("Rate limit hit, retrying...")
            time.sleep(5)
            continue
        time.sleep(delay)
    return results

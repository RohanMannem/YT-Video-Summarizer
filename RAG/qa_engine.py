import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_answer(query, retrieved_chunks, model="gpt-4", max_tokens=300):
    """
    Uses GPT to generate an answer to the query using retrieved transcript chunks.

    Args:
        query (str): The user’s question.
        retrieved_chunks (list of dict): Each dict should have a 'text' field.
        model (str): OpenAI model (e.g., gpt-3.5-turbo, gpt-4).
        max_tokens (int): Max tokens for GPT output.

    Returns:
        str: GPT-generated answer.
    """

    # Combine retrieved chunks into readable references
    context = "\n\n".join(
        f"[Snippet {i+1}]\n{chunk['text']}" for i, chunk in enumerate(retrieved_chunks)
    )

    prompt = f"""You are a helpful assistant. Answer the user's question using only the information from the transcript snippets below.

    {context}

    Question: {query}

    Answer:"""

    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=max_tokens
    )

    return response.choices[0].message.content.strip()

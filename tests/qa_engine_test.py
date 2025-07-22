import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from RAG.qa_engine import answer_question

# Example test variables
store_dir = "vector_store/_xIwjmCH6D4"
question = "What is the main topic discussed in this video?"

answer = answer_question(question, store_dir=store_dir)
print("\nAnswer:\n", answer)
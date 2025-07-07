from fetch_transcript import fetch_transcript
import argparse
from urllib.parse import urlparse, parse_qs
from chunker import chunk_transcript
from embedder import embed_texts

def extract_video_id(youtube_url):
  """Extracts the YouTube video ID from a standard watch URL."""
  parsed_url = urlparse(youtube_url)
  if parsed_url.hostname == 'www.youtube.com' and parsed_url.path == '/watch':
    query_params = parse_qs(parsed_url.query)
    if 'v' in query_params:
      return query_params['v'][0]
  return None

parser = argparse.ArgumentParser(description="YouTube Transcript Summarizer")
parser.add_argument(
    "--video_link",
    type=str,
    required=True
)
parser.add_argument(
    "--use_gpt",
    action="store_true",
    help="Use GPT to generate an abstractive summary"
)

args = parser.parse_args()
video_id = extract_video_id(args.video_link) # video_link= https://www.youtube.com/watch?v=spmBNxDA3HY
caption = fetch_transcript(video_id)

chunks = chunk_transcript(caption, max_tokens=500, overlap=100)
print(f"Generated {len(chunks)} chunks")
print(chunks[0][:500])

embedded_chunks = embed_texts(chunks)
print(f"Embedded {len(embedded_chunks)} chunks")
print(embedded_chunks[0]["embedding"][:5])  # Preview embedding

# if args.use_gpt:
#     from openai_summarizer import openai_summarizer
#     openai_summarizer(caption)
# else:
#     from basic_summarizer import spacy_summarizer
#     from basic_summarizer import nltk_summarizer
#     spacy_summarizer(caption)
#     nltk_summarizer(caption)
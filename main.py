from youtube_transcript_api import YouTubeTranscriptApi
import argparse

parser = argparse.ArgumentParser(description="YouTube Transcript Summarizer")
parser.add_argument(
    "--video_id",
    type=str,
    required=True,
    help="YouTube video ID (e.g., dQw4w9WgXcQ)"
)
parser.add_argument(
    "--use_gpt",
    action="store_true",
    help="Use GPT to generate an abstractive summary"
)

args = parser.parse_args()
video_id = args.video_id
# video_id = 'spmBNxDA3HY'

ytt_api = YouTubeTranscriptApi()
fetched_transcript = ytt_api.fetch(video_id)

captions = []

for snippet in fetched_transcript:
    captions.append(snippet.text)

# indexable
last_snippet = fetched_transcript[-1]

# provides a length
snippet_count = len(fetched_transcript)

caption = ' '.join(captions)

if args.use_gpt:
    from openai_summarizer import openai_summarizer
    openai_summarizer(caption)
else:
    from basic_summarizer import basic_summarizer
    basic_summarizer(caption)
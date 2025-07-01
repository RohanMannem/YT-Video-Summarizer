from fetch_transcript import fetch_transcript
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
video_id = args.video_id # video_id = 'spmBNxDA3HY'
caption = fetch_transcript(video_id)

if args.use_gpt:
    from openai_summarizer import openai_summarizer
    openai_summarizer(caption)
else:
    from basic_summarizer import basic_summarizer
    basic_summarizer(caption)
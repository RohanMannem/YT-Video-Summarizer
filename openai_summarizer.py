from dotenv import load_dotenv
import os
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
import argparse

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

parser = argparse.ArgumentParser(description="YouTube Transcript Summarizer")
parser.add_argument(
    "--video_id",
    type=str,
    required=True,
    help="YouTube video ID (e.g., dQw4w9WgXcQ)"
)

args = parser.parse_args()
video_id = args.video_id
# video_id = 'spmBNxDA3HY'

ytt_api = YouTubeTranscriptApi()
fetched_transcript = ytt_api.fetch(video_id)

captions = []

for snippet in fetched_transcript:
    # print(snippet.text)
    captions.append(snippet.text)

# indexable
last_snippet = fetched_transcript[-1]

# provides a length
snippet_count = len(fetched_transcript)

# print(last_snippet)
# print(snippet_count)

caption = ' '.join(captions)

def summarize_with_gpt(transcript_text, model="gpt-4o"):
    system_msg = {
        "role": "developer",
        "content": "You are a helpful assistant that summarizes YouTube transcripts clearly and concisely."
    }

    user_msg = {
        "role": "user",
        "content": f"Summarize the following transcript in 5-7 bullet points:\n\n{transcript_text}"
    }

    client = OpenAI()

    response = client.chat.completions.create(
        model=model,
        messages=[system_msg, user_msg],
        temperature=0.5,
        max_completion_tokens=500
    )

    summary = response.choices[0].message.content.strip()
    print(summary)
    return summary

summarize_with_gpt(caption)

# video_id = spmBNxDA3HY

# - The 2025 OKC Thunder completed one of the most dominant seasons in NBA history, finishing with the sixth-best record, second-highest net rating, and largest margin of victory ever.

# - Despite being one of the youngest teams with an average age of 24.8 years, they defied expectations by winning the championship, becoming the youngest title-winning team in nearly 50 years.

# - The Thunder's success is attributed to their focus on developing players internally and maintaining high roster continuity, with 79% of their minutes played by returning players.

# - They achieved their success with the 25th highest payroll in the NBA, offering financial flexibility for future growth and player retention.

# - The Thunder possess the largest draft stockpile in the league, with 24 picks over the next five seasons, positioning them well for sustained success.

# - This combination of immediate success and future potential is unprecedented, challenging the notion that teams must choose between winning now or later.

# - The Thunder's accomplishments set them apart as a potential future dynasty, built on smart management, homegrown talent, and strategic planning.
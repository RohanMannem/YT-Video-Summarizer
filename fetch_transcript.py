from youtube_transcript_api import YouTubeTranscriptApi

def fetch_transcript(video_id):
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
    return caption
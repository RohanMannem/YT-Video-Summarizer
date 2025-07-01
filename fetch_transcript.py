from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig

def fetch_transcript(video_id, streamlit=False, proxy_username=None, proxy_password=None):
    if streamlit:
        ytt_api = YouTubeTranscriptApi(
            proxy_config=WebshareProxyConfig(
                proxy_username=proxy_username,
                proxy_password=proxy_password,
            )
        )
    else:
        ytt_api = YouTubeTranscriptApi()
    print(f"Username: {repr(proxy_username)}")
    print(f"Password: {repr(proxy_password)}")
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
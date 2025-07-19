from urllib.parse import urlparse, parse_qs

def extract_video_id(youtube_url):
  """Extracts the YouTube video ID from a standard watch URL."""
  parsed_url = urlparse(youtube_url)
  if parsed_url.hostname == 'www.youtube.com' and parsed_url.path == '/watch':
    query_params = parse_qs(parsed_url.query)
    if 'v' in query_params:
      return query_params['v'][0]
  return None
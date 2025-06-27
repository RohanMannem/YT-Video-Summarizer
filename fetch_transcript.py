from youtube_transcript_api import YouTubeTranscriptApi
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import nltk
nltk.download('punkt_tab')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from string import punctuation
from heapq import nlargest
import argparse

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
nlp = spacy.blank("en")
if "sentencizer" not in nlp.pipe_names:
    nlp.add_pipe("sentencizer")

doc = nlp(caption.lower())

# for sent in doc.sents:
#     print(sent.text)

word_frequencies = {}
for token in doc:
    if token.text not in STOP_WORDS and token.text not in punctuation:
        if token.text not in word_frequencies:
            word_frequencies[token.text] = 1
        else:
            word_frequencies[token.text] += 1

sorted_sentences = sorted(doc.sents, key=lambda sent: sum(word_frequencies[token.text] for token in sent if token.text in word_frequencies), reverse=True)
summary = " ".join(sent.text for sent in sorted_sentences[:3])
print(word_frequencies)
print(summary)


# Tokenize the text into sentences
sentences = sent_tokenize(caption)

# Tokenize the sentences into words
words = [word_tokenize(sentence) for sentence in sentences]

# Flatten the list of words
words = [word for sublist in words for word in sublist]

# Remove stopwords and punctuation
stop_words = set(stopwords.words("english") + list(punctuation))
words = [word for word in words if word not in stop_words]

# Calculate word frequencies
word_frequencies = nltk.FreqDist(words)

# Calculate sentence scores based on word frequencies
sentence_scores = {}
for sentence in sentences:
    for word in word_tokenize(sentence):
        if word in word_frequencies:
            if sentence not in sentence_scores:
                sentence_scores[sentence] = word_frequencies[word]
            else:
                sentence_scores[sentence] += word_frequencies[word]

# Get the top 3 sentences with highest scores as the summary
summary_sentences = nlargest(3, sentence_scores, key=sentence_scores.get)

# Generate summary
summary = " ".join(summary_sentences)
print()
print(word_frequencies)
print(sentence_scores)
print(summary)
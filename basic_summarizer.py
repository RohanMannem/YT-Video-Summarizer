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


def basic_summarizer(caption):
    nlp = spacy.blank("en")
    if "sentencizer" not in nlp.pipe_names:
        nlp.add_pipe("sentencizer")

    doc = nlp(caption.lower())

    word_frequencies = {}
    for token in doc:
        if token.text not in STOP_WORDS and token.text not in punctuation:
            if token.text not in word_frequencies:
                word_frequencies[token.text] = 1
            else:
                word_frequencies[token.text] += 1

    sorted_sentences = sorted(doc.sents, key=lambda sent: sum(word_frequencies[token.text] for token in sent if token.text in word_frequencies), reverse=True)
    summary = " ".join(sent.text for sent in sorted_sentences[:3])
    print("spaCy")
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
    print("NLTK")
    print(summary)
import nltk
nltk.download('punkt_tab')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from string import punctuation
from heapq import nlargest

def nltk_summarizer(caption):
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
    return summary
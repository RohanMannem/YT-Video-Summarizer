import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

def spacy_summarizer(caption):
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
    return summary
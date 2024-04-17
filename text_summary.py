import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text = """Japan, island country lying off the east coast of Asia. 
        It consists of a great string of islands in a northeast-southwest arc that stretches for
        approximately 1,500 miles (2,400 km) through the western North Pacific Ocean. Nearly the entire 
        land area is taken up by the country's four main islands; from north to south these are Hokkaido
        (Hokkaidō), Honshu (Honshū), Shikoku, and Kyushu (Kyūshū). Honshu is the largest of the four, followed in
        size by Hokkaido, Kyushu, and Shikoku. In addition, there are numerous smaller islands, the major groups 
        of which are the Ryukyu (Nansei) Islands (including the island of Okinawa) to the south and west of Kyushu and 
        the Izu, Bonin (Ogasawara),and Volcano (Kazan) islands to the south and east of central Honshu. 
        The national capital, Tokyo (Tōkyō),in east-central Honshu, is one of the world's most populous cities."""

def summariser(raw_docs):

    stopwords = list(STOP_WORDS)
    #print(stopwords)

    nlp = spacy.load('en_core_web_sm')

    doc = nlp(raw_docs)
    #print(doc)

    tokens = [token.text for token in doc ]
    #print(tokens)
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1 
            else:
                word_freq[word.text] += 1

    #print(word_freq)

    max_freq = max(word_freq.values())
    #print(max_freq)

    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq

    #print(word_freq)

    sent_tokens = [sent for sent in doc.sents]

    #print(sent_tokens)
    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

    #print(sent_scores)

    select_len = int(len(sent_tokens)*0.3)
    #print(select_len)

    summary = nlargest(select_len,sent_scores,key=sent_scores.get)
    #print(summary)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)

    # print(text)
    # print(summary)
    # print("length of original text : ",len(text.split(' ')))
    # print("length of summarized text : ",len(summary.split(' ')))
    return summary,doc,len(raw_docs.split(' ')),len(summary.split(' '))
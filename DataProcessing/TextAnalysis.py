from nltk.corpus import wordnet_ic
from nltk.corpus import wordnet
from nltk.corpus import brown
from textblob import TextBlob
import nltk
import heapq as hq
nltk.download('all')
nltk.download('wordnet_ic')


class Analysis:
    thesaurus = []
    with open('Lazy.txt') as T:
        for t in T:
            thesaurus.append(t.strip())
    print(thesaurus)
    stemmer = nltk.stem.PorterStemmer()
    brown_ic = wordnet_ic.ic('ic-brown.dat')

    def RetrieveLemma(self, synset, word):
        for lemma in synset.lemmas():
            if lemma.name().lower() == word:
                return lemma
        return None

    def RetrieveMaxSynset(self, synsets, word):
        lemma, count = None, 0
        for synset in synsets:
            current_lemma = self.RetrieveLemma(synset, word)
            if not current_lemma:
                continue
            if count < current_lemma.count():
                count = current_lemma.count()
                lemma = current_lemma
        return lemma.synset() if lemma else None

    def RetrievePrimarySense(self, word):
        synsets = wordnet.synsets(word)
        return self.RetrieveMaxSynset(synsets, word)

    def Analyze(self, text):
        related = False
        tokens = nltk.word_tokenize(text)
        for i in range(len(tokens)):
            tokens[i] = self.stemmer.stem(tokens[i].lower())
            for word in self.thesaurus:
                word_sense, token_sense = self.RetrievePrimarySense(word), self.RetrievePrimarySense(tokens[i])
                if not word_sense or not token_sense or word_sense.pos != token_sense.pos or word_sense.pos == 's' or word_sense.pos == 'a' or token_sense.pos == 's' or token_sense.pos == 'a':
                    continue
                print(word_sense.pos)
                print(token_sense.pos)
                lin_similarities = word_sense.lin_similarity(token_sense, self.brown_ic)
                if lin_similarities >= 0.5:
                    related = True
                    break
            if related:
                break

        polarity = TextBlob(text).sentiment.polarity
        # print(polarity)
        # subjectivity = TextBlob(text).sentiment.subjectivity

        result = {'related': related, 'polarity': polarity}
        return result

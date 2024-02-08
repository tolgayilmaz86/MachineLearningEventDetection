from nltk.tokenize import RegexpTokenizer
from nltk.util import ngrams
from difflib import SequenceMatcher
from jellyfish import damerau_levenshtein_distance
import re, string, nltk
from snowballstemmer import TurkishStemmer


from SpellCorrector import SpellCorrector


class Preprocessor(object):

    def __init__(self):
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.stopwords = []
        self.stemmer = TurkishStemmer()
        self.spell_checker = SpellCorrector()

        with open('../resources/stopwords-tr.txt') as sw:
            self.stopwords = sw.read().splitlines()
        # classpath = "/Users/tubitak/Projects/eventdetection/src/lib/zemberek-tr-2.1.1.jar"
        # jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=/Users/tubitak/Projects/eventdetection/src/main/lib/zemberek-tum-2.0.jar", "-ea")
        # TurkiyeTurkcesi = jpype.JClass("net.zemberek.tr.yapi.TurkiyeTurkcesi")
        #
        # turkiyeTurkcesi = TurkiyeTurkcesi()
        # Zemberek = jpype.JClass("net.zemberek.erisim.Zemberek")
        # self.zemberek = Zemberek(turkiyeTurkcesi)
        # kelimeler = ["merhabalaştık", "dalgalarının", "habercisi", "tırmalamışsa"]
        # for kelime in kelimeler:
        #     if kelime.strip() > '':
        #         yanit = self.zemberek.kelimeCozumle(kelime)
        #         if yanit:
        #             print("{}".format(yanit[0]))
        #         else:
        #             print("{} ÇÖZÜMLENEMEDİ".format(kelime))
        # jpype.shutdownJVM()

    def clean_tweet(self, tweet):
        tweet = re.sub(r'http\S+', '', tweet).strip()
        tweet = re.sub(r'bit\.ly\S+', '', tweet).strip()
        tweet = re.sub(r'goo\.gl\S+', '', tweet).strip()
        tweet = re.sub(r'pic\.tw\S+', '', tweet).strip()
        tweet = re.sub(r'www\.\S+', '', tweet).strip()
        tweet = re.sub(r'\b\w{1,2}\b', '', tweet).strip()
        tweet = re.sub(r'\w*\d\w*', '', tweet).strip()

        nopunc = [char for char in tweet if char not in string.punctuation]
        nopunc = ''.join(nopunc)
        rep = [('İ', 'i'), ('Ğ', 'ğ'), ('Ü', 'ü'), ('Ş', 'ş'), ('Ö', 'ö'), ('Ç', 'ç')]
        for search, replace in rep:
            nopunc = nopunc.replace(search, replace)
        nopunc = nopunc.lower()

        return self.sanitized_tweet_words(nopunc)

        # return[self.stemmer.stemWord(word).lower()
        #         for word in nopunc.split() if word not in self.stopwords or len(word) > 2]

    # def get_stem(self, word):
    #     stem = self.zemberek.kelimeCozumle(word)
    #     if stem:
    #         print(stem[0].kok().icerik())
    #         return stem[0].kok().icerik()
    #     else:
    #         return word

    def sanitized_tweet_words(self, tweet):
        tw_words = []
        for word in tweet.split():
            # word = self.spell_checker.correction(word)
            if word not in self.stopwords or len(word) > 2:
                tw_words.append(self.stemmer.stemWord(word).lower())
        return tw_words

    def replace_tr_chars(self, tweet):
            return tweet.replace('Ç', 'c').replace('Ş', 's').replace('Ğ', 'g').replace('I', 'i').replace('İ', 'i')\
                .replace('Ö', 'o').replace('Ü', 'u').replace('ç', 'c').replace('ş', 's').replace('ğ', 'g')\
                .replace('ı', 'i').replace('ö', 'o').replace('ü', 'u')

    def removePunctuation(self, tweet):
        tweet = re.sub('(http\:|https\:).*', '', tweet)
        tweet = re.sub(r'[^\w\s#]', ' ', tweet, flags=re.UNICODE).strip()
        return tweet.strip()

    def removeNonWords(self, tweet):
        tweet_re = tweet
        tweet_re = re.sub(r'\W*\b\w{1,2}\b', '', tweet_re, flags=re.UNICODE)
        return tweet_re.strip()

    def toTRLower(self, tweet):
        # tweet_re = unicode(tweet, "utf-8")
        tweet_re = tweet.replace("\n", "").lower()
        return tweet_re.strip()

    def removeNewLines(self, tweet):
        return tweet.replace('\n', ' ').strip()

    def getBigrams(self, tweet):
        bigram_list = []
        self.clean_tweet(tweet)
        token = self.tokenizer.tokenize(tweet)
        bigrams = ngrams(token, 2)
        for i, j in bigrams:
            bigram_list.append("{0} {1}".format(i, j))
        print(bigram_list)
        return bigram_list

    def get_similartiy_ratio(self, word1, word2):
        return SequenceMatcher(None, word1, word2).ratio()

    def hammingDistance(self, s1, s2):
        """Return the Hamming distance between equal-length sequences"""
        if len(s1) != len(s2):
            raise ValueError("Undefined for sequences of unequal length")
        return 1 - sum(el1 != el2 for el1, el2 in zip(s1, s2))/float(len(s1))

    # len_s and len_t are the number of characters in string s and t respectively
    def levenshtein_distance(self, s, len_s, t, len_t):
        # if s in t or t in s:
        #     return 1

        # base case: empty strings
        if len_s < 1:
            return len_t
        if len_t < 1:
            return len_s

        # test if last characters of the strings match
        if s[len_s-1] == t[len_t-1]:
            cost = 0
        else:
            cost = 1

        # return minimum of delete char from s, delete char from t, and delete char from both */
        return 1 - min(self.levenshtein_distance(s, len_s - 1, t, len_t) + 1,
                   self.levenshtein_distance(s, len_s, t, len_t - 1) + 1,
                   self.levenshtein_distance(s, len_s - 1, t, len_t - 1) + cost)/float((len(s)+len(t)))

    def damerau_levenshtein_distance(self, word1, word2):
        return damerau_levenshtein_distance(word1, word2)
# preprocessor = Preprocessor()
# print(preprocessor.clean_tweet('tolfa ne haber, pic.twitter/SDsd ssspic.twitter./SDs , https://sdsds.sd goo.gl/dsfdfd bit.ly/erer.fff'))
# preprocessor.getBigrams('@akbulut_fikret: i̇nsanlık bedava arada bi kullanın derim')

# preprocessor.get_stem('adaletsizlk')
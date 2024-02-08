import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
import joblib
from Preprocessor import Preprocessor

from sklearn.metrics import classification_report

EVENT_COUNT = 5
EVENT_1_COEFF = 2.3
EVENT_2_COEFF = 1.8
EVENT_3_COEFF = 1.6
EVENT_4_COEFF = 2.0
EVENT_5_COEFF = 2.0


class ModelTrainer(object):

    def __init__(self):
        self.train_tweets = []
        self.test_tweets = []
        self.event_classifier = None
        self.vectorizer = None
        self.tfidf_transformer = None
        self.events = None
        self.bow_transformer = None
        self.events_bow = None
        self.multinomial_classifier = MultinomialNB()
        self.multilabel_classifier = OneVsRestClassifier(LinearSVC(random_state=0))
        self.events_tfidf = None
        self.events_tfidf_multilabel = None
        self.sgd_classifier = SGDClassifier(loss='log')
        self.preprocess = Preprocessor()
        self.vectorizer = CountVectorizer(tokenizer=self.preprocess,
                                          analyzer=self.preprocess.clean_tweet, ngram_range=(2, 2))
        self.tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=10, max_df=1.0,
                                                sublinear_tf=False, use_idf=False)
        self.mnb_model = None
        self.sgd_model = None
        self.ml_model = None

        self.trained_model = None
        self.mnb_predictions = []
        self.ml_predictions = []
        self.sgd_predictions = []

        # self.locations = None
        # self.location_vectorizer = VectorizerMixin()
        # self.loc_transformer = None
        # self.locations_bow = None
        # self.location_classifier = MultinomialNB()
        # self.locations_tfidf = None

    def setup(self, recalc=True):
        if not recalc:
            with open('../resources/models/model_mnb.pkl', 'rb') as fid:
                self.multinomial_classifier = joblib.load(fid)
            with open('../resources/models/model_ml.pkl', 'rb') as fid:
                self.multilabel_classifier =joblib.load(fid)
            with open('../resources/models/model_sgd.pkl', 'rb') as fid:
                self.sgd_classifier = joblib.load(fid)
            with open('../resources/models/bow_transformer.pkl', 'rb') as fid:
                self.bow_transformer = joblib.load(fid)
            with open('../resources/models/tfidf_transformer.pkl', 'rb') as fid:
                self.tfidf_transformer = joblib.load(fid)
            return

        self.events = pd.read_csv('../resources/disaster_train.csv', sep=',', quotechar='"',
                             names=['user_id', 'favorite', 'retweet', 'timestamp', 'tweet', 'event'])
        # self.locations = pd.read_csv('../resources/locations.csv', names=['location', 'class'])

        # self.loc_transformer = self.location_vectorizer.fit(self.locations['location'])
        # self.locations_bow = self.loc_transformer.transform(self.locations['location'])
        # self.tfidf_transformer = TfidfTransformer().fit(self.locations_bow)
        # self.locations_tfidf = self.tfidf_transformer.transform(self.locations_bow)

        self.vectorizer.stop_words = self.preprocess.stopwords
        self.bow_transformer = self.vectorizer.fit(self.events['tweet'])
        self.events_bow = self.bow_transformer.transform(self.events['tweet'])
        self.tfidf_transformer = TfidfTransformer().fit(self.events_bow)
        self.events_tfidf = self.tfidf_transformer.transform(self.events_bow)

        with open('../resources/models/bow_transformer.pkl', 'wb') as fid:
            joblib.dump(self.bow_transformer, fid)
        with open('../resources/models/tfidf_transformer.pkl', 'wb') as fid:
            joblib.dump(self.tfidf_transformer, fid)

        # self.train_locations()

        self.train_multi_label()
        self.train_multi_nomial_nb()
        self.train_sgd_classifier()

    def train_locations(self):
        # print(self.locations_tfidf)
        self.location_classifier.fit(self.locations_tfidf, self.locations['class'])

    def train_multi_nomial_nb(self):
        self.mnb_model = self.multinomial_classifier.fit(self.events_tfidf, self.events['event'])
        with open('../resources/models/model_mnb.pkl', 'wb') as fid:
            joblib.dump(self.multinomial_classifier, fid)

    def train_multi_label(self):
        self.ml_model = self.multilabel_classifier.fit(self.events_tfidf, self.events['event'])

        with open('../resources/models/model_ml.pkl', 'wb') as fid:
            joblib.dump(self.multilabel_classifier, fid)

    def train_sgd_classifier(self):
        self.sgd_model = self.sgd_classifier.fit(self.events_bow, self.events['event'])
        with open('../resources/models/model_sgd.pkl', 'wb') as fid:
            joblib.dump(self.multinomial_classifier, fid)

    def predict_multi_nomial_nb(self, tweet):
        bow_tw = self.bow_transformer.transform([tweet])
        tfidf_tw = self.tfidf_transformer.transform(bow_tw)

        i = 0
        scores = dict()
        for cls in self.multinomial_classifier.classes_:
            scores[cls] = (self.multinomial_classifier.predict_proba(tfidf_tw)[0] * 100)[i]
            i += 1
        print(tweet)
        predictions, train = self.calculate_predictions(scores)
        if train:
            self.mnb_predictions.append(predictions[0])
            self.multinomial_classifier.partial_fit(bow_tw, [predictions[0]])
            with open('../resources/models/model_mnb.pkl', 'wb') as fid:
                joblib.dump(self.multinomial_classifier, fid)
            print('>>>>>>>>>>>>>>>>>>>> Model Trained <<<<<<<<<<<<<<<<<<<<<<<<<')
        print(predictions)
        print('----------------------------------------------------------------------------------------')
        return predictions

    def predict_multi_label(self, tweet):
        bow_tw = self.bow_transformer.transform([tweet])
        tfidf_tw = self.tfidf_transformer.transform(bow_tw)
        prediction = self.multilabel_classifier.predict(tfidf_tw)
        self.ml_predictions.append(prediction)
        print(tweet, 'ML --> ', prediction)

    def predict_sgd(self, tweet):
        bow_tw = self.bow_transformer.transform([tweet])
        tfidf_tw = self.tfidf_transformer.transform(bow_tw)

        i = 0
        scores = dict()
        for cls in self.sgd_classifier.classes_:
            scores[cls] = (self.sgd_classifier.predict_proba(tfidf_tw)[0] * 100)[i]
            i += 1
        # print(tweet)
        # print(scores)
        predictions, train = self.calculate_predictions(scores)
        if train:
            self.multinomial_classifier.partial_fit(bow_tw, [predictions[0]])
            with open('../resources/models/model_sgd.pkl', 'wb') as fid:
                joblib.dump(self.multinomial_classifier, fid)
        return predictions

    def predict(self, tweet, model='mnb'):
        if model == 'mnb':
            return self.predict_multi_nomial_nb(tweet)
        elif model == 'multilabel':
            return self.predict_multi_label(tweet)
        elif model == 'sgd':
            return self.predict_sgd(tweet)

    def has_location_info(self, tweet):
        bow_loc = self.loc_transformer.transform([tweet])
        tfidf_tw = self.tfidf_transformer.transform(bow_loc)
        # print(self.location_classifier.predict(tfidf_tw))

    def calculate_predictions(self, scores):
        sorted_scores = sorted(scores, key=scores.get, reverse=True)
        predictions = []
        hyperplane = EVENT_1_COEFF * 100 / EVENT_COUNT

        if scores[sorted_scores[0]] > hyperplane:
            predictions.append(sorted_scores[0])

        remaining_percent = 100 - scores[sorted_scores[0]]
        hyperplane = EVENT_2_COEFF * remaining_percent / (EVENT_COUNT - 1)

        if scores[sorted_scores[1]] / scores[sorted_scores[0]] > 0.5 and scores[sorted_scores[1]] > hyperplane:
            predictions.append(sorted_scores[1])

        remaining_percent -= scores[sorted_scores[1]]
        hyperplane = EVENT_3_COEFF * remaining_percent / (EVENT_COUNT - 2)
        if len(predictions) == 2 and scores[sorted_scores[2]] > hyperplane:
            predictions.append(sorted_scores[2])

        remaining_percent -= scores[sorted_scores[2]]
        hyperplane = EVENT_4_COEFF * remaining_percent / (EVENT_COUNT - 3)
        if len(predictions) == 3 and scores[sorted_scores[3]] > hyperplane:
            predictions.append(sorted_scores[3])

        # TODO clear predictions somewhere if it has all events or inappropriate percents

        train = False
        if scores[sorted_scores[0]] > 60.0:
            train = True

        # print([(event, int(scores[event])) for event in sorted_scores])

        return predictions, train

    def report(self, model='mnb'):
        if model == 'mnb':
            self.mnb_predictions = self.mnb_model.predict(self.events_tfidf)
            print(classification_report(self.events['event'], self.mnb_predictions))
        elif model == 'sgd':
            self.sgd_predictions = self.sgd_model.predict(self.events_tfidf)
            print(classification_report(self.events['event'], self.sgd_predictions))
        elif model == 'ml':
            self.ml_predictions = self.ml_model.predict(self.events_tfidf)
            print(classification_report(self.events['event'], self.ml_predictions))


if __name__ == '__main__':
    model = ModelTrainer()
    model.setup(recalc=True)
    # model.report('mnb')
    # print('--------------------')
    # model.report('sgd')
    # print('--------------------')
    # model.report('ml')
    # print('--------------------')

    # mod = 'mnb'
#
#     # model.has_location_info('eskişehir yolunda kaza')
#     # model.has_location_info('adana ayrımında')
#     # model.has_location_info('sdfdsfds')
#     # model.has_location_info('dssf e')
#     # model.has_location_info('vvvvv')
#     # model.has_location_info('yok canım!')
#
#     model.predict('büyük devlet böyle olurmuş-barbaros kartal  4 şehit verdik,ankara’nın tepkisine bakılınca trafik kazası z',mod)
#     model.predict('aşağı yol kavşağında trafik kazası', mod)
#     model.predict('richter ölçeğine göre 4.5 büyüklüğünde', mod)
#     model.predict('alevlerin sardığı binadan çıkan olmadı', mod)
#     model.predict('sağanak yağmur ve azgın suların sürüklediği araçlar çamura saplandı', mod)
#     model.predict('Büyük bir patlama meydana geldi', mod)
#     model.predict('lanet olsun teröre ve destekçilerine', mod)
#     model.predict('bunun herhangi bir konu ile alakası yoh', mod)
#     model.predict('büyük bir patlama meydana geldi ve trafik kazası araç arızası sel ile su bastı', mod)
#     model.predict('aşağı yol kavşağında trafik kazası araç arızası richter ölçeğine göre 4.5 büyüklüğünde', mod)
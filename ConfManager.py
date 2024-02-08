from configparser import ConfigParser, RawConfigParser, NoOptionError
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

class ConfManager(object):
    def __init__(self):
        self.config = RawConfigParser()
        self.conf_file = os.path.join(dir_path, '../resources/conf.ini')
        self.main_algorithm = 'Multinomial NB'
        self.config.read(self.conf_file)
        self.window_confs = None
        self.load_defaults()
        self.vectorizer = None
        self.estimator = None
        self.transformer = None
        self.cb_remlinks = True
        self.cb_remchars = True
        self.cb_remnonwords = True
        self.cb_rempunctuation = True
        self.cb_spellcheck = True
        self.cb_stopwords = True
        #self.load_conf()

    def load_defaults(self):
        # Twitter Credentials
        self.access_token = "721070683476860928-TY8VxNshpLqRrZ7fvHDT83F7SRTwtSN"
        self.access_token_secret = "0BHBBIPvP25Fxd8O81XCFFBKSIelTaWEsjCcy9p3DU2EH"
        self.consumer_key = "5rmXOhuSBIsBH6ma6pdN9E6l5"
        self.consumer_secret = "aOSREVNHBMvO4zAtrOfvpAbGmty0ba1NI9Mu7MkBcYin569JVc"

        # File paths
        self.stopwords_file = os.path.join(dir_path, '../resources/stopwords-tr.txt')
        self.spell_file = os.path.join(dir_path, '../resources/spells.txt')
        self.model_mnb_file = os.path.join(dir_path, '../resources/models/model_mnb.pkl')
        self.model_ml_file = os.path.join(dir_path, '../resources/models/model_ml.pkl')
        self.model_sgd_file = os.path.join(dir_path, '../resources/models/model_sgd.pkl')
        self.model_crf_file = os.path.join(dir_path, '../resources/models/model_crf.crf')
        self.model_bow_transformer_file = os.path.join(dir_path, '../resources/models/bow_transformer.pkl')
        self.model_tfidf_transformer_file = os.path.join(dir_path, '../resources/models/tfidf_transformer.pkl')
        self.train_data_file = os.path.join(dir_path, '../resources/disaster_train.csv')
        self.annotated_file = os.path.join(dir_path, '../resources/annotated.json')
        self.tagged_sentences = os.path.join(dir_path, '../resources/ner_tweets.json')
        self.location_ilceler = os.path.join(dir_path, '../resources/location_rules/ilceler.txt')
        self.location_zarflar = os.path.join(dir_path, '../resources/location_rules/zarflar.txt')

        # Nobs
        self.EVENT_COUNT = 5
        self.EVENT_1_COEFF = 2.3
        self.EVENT_2_COEFF = 1.8
        self.EVENT_3_COEFF = 1.6
        self.EVENT_4_COEFF = 2.0
        self.EVENT_5_COEFF = 2.0
        self.classifier = 'OneVsRestClassifier'
        self.transformer = 'TF-IDF Transformer'
        self.vectorizer = 'CountVectorizer'
        self.recalc = True

        self.ngram = (1, 2)
        self.min_df = 10
        self.max_df = 1.0
        self.use_idf = False
        self.sublinear_tf = False
        self.multiclass = 'ovr'
        self.C = 1.0
        self.penalty = 'l2'
        self.coef0 = 0.0
        self.epsilon = 0.0
        self.degree = 3
        self.decision_function_shape = None
        self.tol = 1e-4
        self.max_iter = 1000
        self.fit_intercept = True
        self.nu = 0.5
        self.cache_size = 200
        self.class_weight = None
        self.shrinking = True
        self.gamma = 'auto'
        self.dual = True
        self.kernel = 'rbf'
        self.probability = False
        self.intercept_scaling = 1
        self.loss = 'squared_hinge'
        self.verbose = 0
        self.random_state = 0

    def load_conf(self):
        self.access_token = self.config.get('TW_CREDENTIALS',                   'access_token')
        self.access_token_secret = self.config.get('TW_CREDENTIALS',            'access_token_secret')
        self.consumer_key = self.config.get('TW_CREDENTIALS',                   'consumer_key')
        self.consumer_secret = self.config.get('TW_CREDENTIALS',                'consumer_secret')

        try:
            if '..' in self.config.get('FILE_PATH', 'stopwords_file'):
                self.stopwords_file = os.path.join(dir_path, self.config.get('FILE_PATH', 'stopwords_file'))
            else:
                self.stopwords_file = self.config.get('FILE_PATH', 'stopwords_file')

            if '..' in self.config.get('FILE_PATH', 'spell_file'):
                self.spell_file = os.path.join(dir_path, self.config.get('FILE_PATH', 'spell_file'))
            else:
                self.spell_file = self.config.get('FILE_PATH', 'spell_file')

            if '..' in self.config.get('FILE_PATH', 'model_mnb_file'):
                self.model_mnb_file = os.path.join(dir_path, self.config.get('FILE_PATH', 'model_mnb_file'))
            else:
                self.model_mnb_file = self.config.get('FILE_PATH', 'model_mnb_file')

            if '..' in self.config.get('FILE_PATH', 'model_ml_file'):
                self.model_ml_file = os.path.join(dir_path, self.config.get('FILE_PATH', 'model_ml_file'))
            else:
                self.model_ml_file = self.config.get('FILE_PATH', 'model_ml_file')

            if '..' in self.config.get('FILE_PATH', 'model_sgd_file'):
                self.model_sgd_file = os.path.join(dir_path, self.config.get('FILE_PATH', 'model_sgd_file'))
            else:
                self.model_sgd_file = self.config.get('FILE_PATH', 'model_sgd_file')

            if '..' in self.config.get('FILE_PATH', 'model_bow_transformer_file'):
                self.model_bow_transformer_file = os.path.join(dir_path, self.config.get('FILE_PATH',
                                                                                         'model_bow_transformer_file'))
            else:
                self.model_bow_transformer_file = self.config.get('FILE_PATH', 'model_bow_transformer_file')

            if '..' in self.config.get('FILE_PATH', 'model_tfidf_transformer_file'):
                self.model_tfidf_transformer_file = os.path.join(dir_path, self.config.get('FILE_PATH',
                                                                                           'model_tfidf_transformer_file'))
            else:
                self.model_tfidf_transformer_file = self.config.get('FILE_PATH', 'model_tfidf_transformer_file')

            if '..' in self.config.get('FILE_PATH', 'train_data_file'):
                self.train_data_file = os.path.join(dir_path, self.config.get('FILE_PATH', 'train_data_file'))
            else:
                self.train_data_file = self.config.get('FILE_PATH', 'train_data_file')

            if '..' in self.config.get('FILE_PATH', 'annotated_file'):
                self.annotated_file = os.path.join(dir_path, self.config.get('FILE_PATH', 'annotated_file'))
            else:
                self.annotated_file = self.config.get('FILE_PATH', 'annotated_file')

            if '..' in self.config.get('FILE_PATH', 'tagged_sentences'):
                self.tagged_sentences = os.path.join(dir_path, self.config.get('FILE_PATH', 'tagged_sentences'))
            else:
                self.tagged_sentences = self.config.get('FILE_PATH', 'tagged_sentences')

            if '..' in self.config.get('FILE_PATH', 'model_crf_file'):
                self.model_crf_file = os.path.join(dir_path, self.config.get('FILE_PATH', 'model_crf_file'))
            else:
                self.model_crf_file = self.config.get('FILE_PATH', 'model_crf_file')

            if '..' in self.config.get('FILE_PATH', 'location_ilceler'):
                self.location_ilceler = os.path.join(dir_path, self.config.get('FILE_PATH', 'location_ilceler'))
            else:
                self.location_ilceler = self.config.get('FILE_PATH', 'location_ilceler')

            if '..' in self.config.get('FILE_PATH', 'location_zarflar'):
                self.location_zarflar = os.path.join(dir_path, self.config.get('FILE_PATH', 'location_zarflar'))
            else:
                self.location_zarflar = self.config.get('FILE_PATH', 'location_zarflar')

        except (NoOptionError, KeyError) as err:
            print(err)

        self.ngram = self.config.get('PARAMETERS', 'ngram')
        self.min_df = self.config.getfloat('PARAMETERS', 'min_df')
        self.max_df = self.config.getfloat('PARAMETERS', 'max_df')
        self.use_idf = self.config.getboolean('PARAMETERS', 'use_idf')
        self.sublinear_tf = self.config.getboolean('PARAMETERS', 'sublinear_tf')
        self.multiclass = self.config.get('PARAMETERS', 'multiclass')
        self.C = self.config.getfloat('PARAMETERS', 'C')
        self.penalty = self.config.get('PARAMETERS', 'penalty')
        self.coef0 = self.config.getfloat('PARAMETERS', 'coef0')
        self.epsilon = self.config.getfloat('PARAMETERS', 'epsilon')
        self.degree = self.config.getint('PARAMETERS', 'degree')
        self.decision_function_shape = self.config.get('PARAMETERS', 'decision_function_shape')
        self.tol = self.config.getfloat('PARAMETERS', 'tol')
        self.max_iter = self.config.getint('PARAMETERS', 'max_iter')
        self.fit_intercept = self.config.get('PARAMETERS', 'fit_intercept')
        self.nu = self.config.getfloat('PARAMETERS', 'nu')
        self.cache_size = self.config.getint('PARAMETERS', 'cache_size')
        self.class_weight = self.config.get('PARAMETERS', 'class_weight')
        self.shrinking = self.config.getboolean('PARAMETERS', 'shrinking')
        self.gamma = self.config.get('PARAMETERS', 'gamma')
        self.dual = self.config.getboolean('PARAMETERS', 'dual')
        self.kernel = self.config.get('PARAMETERS', 'kernel')
        self.probability = self.config.getboolean('PARAMETERS', 'probability')
        self.intercept_scaling = self.config.get('PARAMETERS', 'intercept_scaling')
        self.loss = self.config.get('PARAMETERS', 'loss')
        self.verbose = self.config.get('PARAMETERS', 'verbose')
        self.random_state = self.config.get('PARAMETERS', 'random_state')

        self.EVENT_COUNT = self.config.getint('EVENT_COEFFS', 'event_count')
        self.EVENT_1_COEFF = self.config.getfloat('EVENT_COEFFS', 'event1coeff')
        self.EVENT_2_COEFF = self.config.getfloat('EVENT_COEFFS', 'event2coeff')
        self.EVENT_3_COEFF = self.config.getfloat('EVENT_COEFFS', 'event3coeff')
        self.EVENT_4_COEFF = self.config.getfloat('EVENT_COEFFS', 'event4coeff')
        self.EVENT_5_COEFF = self.config.getfloat('EVENT_COEFFS', 'event5coeff')

    def save_paths(self):
        self.config.set('TW_CREDENTIALS', 'access_token', self.access_token)
        self.config.set('TW_CREDENTIALS', 'access_token_secret', self.access_token_secret)
        self.config.set('TW_CREDENTIALS', 'consumer_key', self.consumer_key)
        self.config.set('TW_CREDENTIALS', 'consumer_secret', self.consumer_secret)

        self.config.set('FILE_PATH', 'stopwords_file', self.stopwords_file)
        self.config.set('FILE_PATH', 'spell_file', self.spell_file)
        self.config.set('FILE_PATH', 'model_mnb_file', self.model_mnb_file)
        self.config.set('FILE_PATH', 'model_ml_file', self.model_ml_file)
        self.config.set('FILE_PATH', 'model_sgd_file', self.model_sgd_file)
        self.config.set('FILE_PATH', 'model_bow_transformer_file', self.model_bow_transformer_file)
        self.config.set('FILE_PATH', 'model_tfidf_transformer_file', self.model_tfidf_transformer_file)
        self.config.set('FILE_PATH', 'train_data_file', self.train_data_file)
        self.config.set('FILE_PATH', 'annotated_file', self.annotated_file)
        self.config.set('FILE_PATH', 'tagged_sentences', self.tagged_sentences)
        self.config.set('FILE_PATH', 'location_ilceler', self.location_ilceler)
        self.config.set('FILE_PATH', 'model_crf', self.model_crf_file)
        self.config.set('FILE_PATH', 'location_zarflar', self.location_zarflar)

        with open(self.conf_file, 'w') as configfile:
            self.config.write(configfile)

    def save_conf(self):
        if not self.config.has_section("TW_CREDENTIALS"):
            self.config.add_section("TW_CREDENTIALS")
        if not self.config.has_section("FILE_PATH"):
            self.config.add_section("FILE_PATH")
        if not self.config.has_section("PARAMETERS"):
            self.config.add_section("PARAMETERS")
        if not self.config.has_section("EVENT_COEFFS"):
            self.config.add_section("EVENT_COEFFS")

        self.config.set('TW_CREDENTIALS', 'access_token',           self.access_token)
        self.config.set('TW_CREDENTIALS', 'access_token_secret',    self.access_token_secret)
        self.config.set('TW_CREDENTIALS', 'consumer_key',           self.consumer_key)
        self.config.set('TW_CREDENTIALS', 'consumer_secret',        self.consumer_secret)

        self.config.set('FILE_PATH', 'stopwords_file',              self.stopwords_file)
        self.config.set('FILE_PATH', 'spell_file',                  self.spell_file)
        self.config.set('FILE_PATH', 'model_mnb_file',              self.model_mnb_file)
        self.config.set('FILE_PATH', 'model_ml_file',               self.model_ml_file)
        self.config.set('FILE_PATH', 'model_sgd_file',              self.model_sgd_file)
        self.config.set('FILE_PATH', 'model_bow_transformer_file',  self.model_bow_transformer_file)
        self.config.set('FILE_PATH', 'model_tfidf_transformer_file',self.model_tfidf_transformer_file)
        self.config.set('FILE_PATH', 'train_data_file',             self.train_data_file)
        self.config.set('FILE_PATH', 'annotated_file',              self.annotated_file)
        self.config.set('FILE_PATH', 'tagged_sentences',            self.tagged_sentences)
        self.config.set('FILE_PATH', 'location_ilceler',            self.location_ilceler)
        self.config.set('FILE_PATH', 'model_crf',                   self.model_crf_file)
        self.config.set('FILE_PATH', 'location_zarflar',            self.location_zarflar)

        self.config.set('EVENT_COEFFS', 'event_count', 5)
        self.config.set('EVENT_COEFFS', 'event1coeff', self.EVENT_1_COEFF)
        self.config.set('EVENT_COEFFS', 'event2coeff', self.EVENT_2_COEFF)
        self.config.set('EVENT_COEFFS', 'event3coeff', self.EVENT_3_COEFF)
        self.config.set('EVENT_COEFFS', 'event4coeff', self.EVENT_4_COEFF)
        self.config.set('EVENT_COEFFS', 'event5coeff', self.EVENT_5_COEFF)

        self.config.set('PARAMETERS', 'ngram', self.ngram)
        self.config.set('PARAMETERS', 'min_df', self.min_df)
        self.config.set('PARAMETERS', 'max_df', self.max_df)
        self.config.set('PARAMETERS', 'use_idf', self.use_idf)
        self.config.set('PARAMETERS', 'sublinear_tf', self.sublinear_tf)
        self.config.set('PARAMETERS', 'multiclass', self.multiclass)
        self.config.set('PARAMETERS', 'C', self.C)
        self.config.set('PARAMETERS', 'penalty', self.penalty)
        self.config.set('PARAMETERS', 'coef0', self.coef0)
        self.config.set('PARAMETERS', 'epsilon', self.epsilon)
        self.config.set('PARAMETERS', 'degree', self.degree)
        self.config.set('PARAMETERS', 'decision_function_shape', self.decision_function_shape)
        self.config.set('PARAMETERS', 'tol', self.tol)
        self.config.set('PARAMETERS', 'max_iter', self.max_iter)
        self.config.set('PARAMETERS', 'fit_intercept', self.fit_intercept)
        self.config.set('PARAMETERS', 'nu', self.nu)
        self.config.set('PARAMETERS', 'cache_size', self.cache_size)
        self.config.set('PARAMETERS', 'class_weight', self.class_weight)
        self.config.set('PARAMETERS', 'shrinking', self.shrinking)
        self.config.set('PARAMETERS', 'gamma', self.gamma)
        self.config.set('PARAMETERS', 'dual', self.dual)
        self.config.set('PARAMETERS', 'kernel', self.kernel)
        self.config.set('PARAMETERS', 'probability', self.probability)
        self.config.set('PARAMETERS', 'intercept_scaling', self.intercept_scaling)
        self.config.set('PARAMETERS', 'loss', self.loss)
        self.config.set('PARAMETERS', 'verbose', self.verbose)
        self.config.set('PARAMETERS', 'random_state', self.random_state)

        with open(self.conf_file, 'w') as configfile:
            self.config.write(configfile)

if __name__ == '__main__':
    confman = ConfManager()
    print(confman.window_confs.cb_mnb.isChecked())
    # confman.save_conf()

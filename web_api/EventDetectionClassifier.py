from sklearn.externals import joblib


class EventDetectionClassifier(object):

  def __init__(self):
    with open(self.conf.model_mnb_file, 'rb') as fid:
      self.multinomial_classifier = joblib.load(fid)
    with open(self.conf.model_ml_file, 'rb') as fid:
      self.multilabel_classifier = joblib.load(fid)
    with open(self.conf.model_sgd_file, 'rb') as fid:
      self.sgd_classifier = joblib.load(fid)
    with open(self.conf.model_bow_transformer_file, 'rb') as fid:
      self.bow_transformer = joblib.load(fid)
    with open(self.conf.model_tfidf_transformer_file, 'rb') as fid:
      self.tfidf_transformer = joblib.load(fid)
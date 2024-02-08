import twitter_auth
import tweepy
import json
import os
import codecs
from nltk.tag import CRFTagger
from nltk.tag import StanfordNERTagger
from LocationDetection import get_district_list
from nltk.tag.util import untag
from nltk.metrics import precision
from ConfManager import ConfManager

def get_train_data(path):
  sentences = []
  with codecs.open(path, encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
      sentence = []
      for named_entity in json.loads(line):
        sentence.append(tuple(named_entity))
      sentences.append(sentence)
  return sentences

def get_train_data_from_annotated(path=ConfManager.annotated_file):
  sentences = []
  with codecs.open(path, encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
      sentence = []
      for named_entity in json.loads(line)['annotated']:
        sentence.append(tuple(named_entity))
      sentences.append(sentence)
  return sentences

def get_crf_tagger():
  dir_path = os.path.dirname(os.path.realpath(__file__))
  tagged_sentences = get_train_data(os.path.join(dir_path, ConfManager.tagged_sentences))
  ct = CRFTagger()
  ct.train(tagged_sentences, ConfManager.model_crf_file)
  return ct

class CRF_extended(CRFTagger):
  def cross_validate(self, data, k=3):
    total = len(data)
    step = total//k
    from random import shuffle
    shuffle(data)
    scores = []
    predicted = []
    actual = []
    districts = [[(d, 'LOCATION')] for d in get_district_list()]
    for i in range(0, k):
      train_data = data[0:i*step] + data[(i+1)*step:]
      test_data = data[i*step:i*step + step]
      print(i*step, i*step + step)
      self.train(train_data+districts, 'cross-validate.crf')
      tagged = self.tag_sents(untag(sent) for sent in test_data)
      predicted += [i[1] for sent in tagged for i in sent]
      actual += [i[1] for sent in test_data for i in sent]
      scores.append(self.evaluate(test_data))
      self.get_confusion_matrix(actual, predicted)
    return scores

  def get_confusion_matrix(self, actual, predicted):
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(actual, predicted, self._tagger.labels())
    print(self._tagger.labels())
    print(cm)

if __name__ == "__main__":
  import re
  dir_path = os.path.dirname(os.path.realpath(__file__))
  tagged_sentences = get_train_data_from_annotated(os.path.join(dir_path, '../resources/annotated.json'))
  test_data = get_train_data_from_annotated(os.path.join(dir_path, '../resources/radyotrafik_annotated.json'))
  train2_data = get_train_data_from_annotated(os.path.join(dir_path, '../resources/annotated_abbtrafik.json'))
  district_list = get_district_list()
  gazetteer = [[(d, 'LOCATION')] for d in district_list]



  ct = CRF_extended()
  # print(ct.cross_validate(tagged_sentences, k=10))
  ct.train(tagged_sentences+test_data+train2_data+gazetteer, "model.crf")
  ct.cross_validate(tagged_sentences+test_data+train2_data, k=5)

  # tagged = ct.tag_sents(untag(sent) for sent in train2_data)
  # predicted = []
  # actual = []
  # predicted += [i[1] for sent in tagged for i in sent]
  # actual += [i[1] for sent in train2_data for i in sent]
  # ct.get_confusion_matrix(actual, predicted)


  tagged = ct.tag_sents([re.split(' ', '''Besiktas Belestepe'deki saldiri ile Ortaköy Reina baglantili mi?''')])
  print(tagged)

  tagged = ct.tag_sents([re.split(' ', '''Elmadağ Hasanoğlan Caddesi ile Akyurt Bağlantı Yolunda karla mücadele çalışmalarımız devam ediyor''')])
  print(tagged)

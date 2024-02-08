import json, csv
import os
import codecs
from nltk.tag import CRFTagger
from nltk.tag import StanfordNERTagger
from nltk.tag.util import untag
from nltk.metrics import precision


def get_district_list(path='../../resources/location_rules/ilceler.txt'):
  district_list = []
  with codecs.open(path, 'r', encoding='utf8') as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
      district_list.append(row[0])
    
  return district_list


def get_from_text_file(path='../../resources/ner_rules/isim_listesi.txt'):
  name_list = []
  with codecs.open(path, 'r', encoding='utf8') as f:
    lines = f.readlines()
    name_list = [n.strip() for n in lines]
  return name_list


def get_location_sequences(tagged):
  sequences = []
  for idx, (token, tag) in enumerate(tagged):
    if tag == 'LOCATION':
      if idx > 0 and tagged[idx-1][1] == 'LOCATION':
        sequences[-1] += ' ' + token
      else:
        sequences.append(token)
  return sequences


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


def get_train_data_from_annotated(path='../../resources/annotated.json'):
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
  tagged_sentences = get_train_data_from_annotated(os.path.join(dir_path, '../../resources/annotated.json'))
  radyo_trafik = get_train_data_from_annotated(os.path.join(dir_path, '../../resources/radyotrafik_annotated.json'))
  abb_trafik = get_train_data_from_annotated(os.path.join(dir_path, '../../resources/annotated_abbtrafik.json'))
  district_list = get_district_list()
  name_list = get_from_text_file(path='../../resources/ner_rules/isim_listesi.txt')
  surname_list = get_from_text_file(path='../../resources/ner_rules/soyisim_listesi.txt')
  tansel_keywords = get_from_text_file(path='../../resources/location_rules/tansel_hoca_keywords.txt')
  stop_words = get_from_text_file(path='../../resources/stopwords-tr.txt')
  prepositions = get_from_text_file(path="../../resources/location_rules/zarflar.txt")

  name_gazetteer = [[(n, 'PERSON')] for n in (surname_list+name_list)]
  gazetteer = [[(d, 'LOCATION')] for d in (district_list+tansel_keywords)]
  preposition_gazetteer = [[(p, 'PREPOSITION') for p in prepositions]]
  other_gazetteer = [[(o, 'OTHER') for o in stop_words]]

  gazetteers = gazetteer + name_gazetteer + preposition_gazetteer + other_gazetteer
  ct = CRF_extended()
  ct.train(tagged_sentences + gazetteers, "model.crf")
  return ct


class CRF_extended(CRFTagger):
  
  def __init__(self):
    super().__init__(feature_func=self.get_features)

  def get_features(self, tokens, idx):
    features = super(CRF_extended, self)._get_features(tokens, idx)
    token = tokens[idx]
    
    if token.isupper():
      features.append('UPPERCASE')
    if "'" in token:
      features.append('QUOTE')
    
    return features

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


  ct = get_crf_tagger()
  # ct.cross_validate(tagged_sentences+test_data+train2_data, k=5)

  # tagged = ct.tag_sents(untag(sent) for sent in train2_data)
  # predicted = []
  # actual = []
  # predicted += [i[1] for sent in tagged for i in sent]
  # actual += [i[1] for sent in train2_data for i in sent]
  # ct.get_confusion_matrix(actual, predicted)


  # tagged = ct.tag_sents([re.split(' ', '''Besiktas belestepedeki saldiri ile Ortaköy Reina baglantili mi?''')])
  tagged = ct.tag('Besiktas belestepedeki saldiri ile Ortaköy Reina baglantili mi?'.split(' '))
  print(tagged)


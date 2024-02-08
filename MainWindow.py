import sys
from PyQt5 import QtWidgets, uic
import icons_rc
import ConfManager
from ModelRunner import ModelRunner
from StreamRunner import StreamRunner


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        self.conf = ConfManager.ConfManager()
        self.streamRunner = StreamRunner(conf=self.conf)
        self.actionTrain.triggered.connect(self.train_action_triggered)
        self.actionSave.triggered.connect(self.action_save_conf)
        self.actionTweets.triggered.connect(self.action_fetch_tweets)
        self.modelRunner = ModelRunner(self.conf)

        self.btn_browse_mnb_2.clicked.connect(self.browse_mnb_file)
        self.btn_browse_ml_2.clicked.connect(self.browse_ml_file)
        self.btn_browse_sgd_2.clicked.connect(self.browse_sgd_file)
        self.btn_browse_spell_2.clicked.connect(self.browse_spell_file)
        self.btn_browse_stopwords_2.clicked.connect(self.browse_sw_file)
        self.btn_ner_file.clicked.connect(self.browse_ner_file)
        self.btn_save_paths.clicked.connect(self.save_paths)

        # FILE & FOLDER PATHS
        self.btn_browse_mnb.clicked.connect(self.set_mnb_file)
        self.btn_browse_ml.clicked.connect(self.set_ml_file)
        self.btn_browse_sgd.clicked.connect(self.set_sgd_file)
        self.btn_browse_spell.clicked.connect(self.set_spell_file)
        self.btn_browse_stopwords.clicked.connect(self.set_stopwords_file)
        self.btn_browse_train_file.clicked.connect(self.set_train_file)
        self.btn_browse_ner.clicked.connect(self.set_ner_file)
        self.btn_browse_annotated_file.clicked.connect(self.set_annotated_file)
        self.txt_event1coeff.setValue(self.conf.EVENT_1_COEFF)
        self.txt_event2coeff.setValue(self.conf.EVENT_2_COEFF)
        self.txt_event3coeff.setValue(self.conf.EVENT_3_COEFF)
        self.txt_event4coeff.setValue(self.conf.EVENT_4_COEFF)
        self.txt_event5coeff.setValue(self.conf.EVENT_5_COEFF)

        self.load_paths()

        self.conf.window_confs = self

    # TRAIN PREFERENCES ------------------------------------------------------------

    def load_paths(self):
        self.txt_mnb_file.setText(self.conf.model_mnb_file)
        self.txt_ml_file.setText(self.conf.model_ml_file)
        self.txt_sgd_file.setText(self.conf.model_sgd_file)
        self.txt_train_file.setText(self.conf.train_data_file)
        self.txt_spell_file.setText(self.conf.spell_file)
        self.txt_loc_keywords_file.setText(self.conf.location_zarflar)
        self.txt_stopwords_file.setText(self.conf.stopwords_file)
        self.txt_annotated_file.setText(self.conf.annotated_file)
        self.txt_ner_file.setText(self.conf.tagged_sentences)
        self.txt_model_crf_file.setText(self.conf.model_crf_file)
        self.txt_bow_transform_file.setText(self.conf.model_bow_transformer_file)
        self.txt_tfidf_transform_file.setText(self.conf.model_tfidf_transformer_file)
        self.txt_access_token.setText(self.conf.access_token)
        self.txt_access_token_secret.setText(self.conf.access_token_secret)
        self.txt_consumer_key.setText(self.conf.consumer_key)
        self.txt_consumer_secret.setText(self.conf.consumer_secret)

        # self.txt_ner_file.setText(self.conf.model_ner_file)

    def save_paths(self):
        self.conf.model_mnb_file = self.txt_mnb_file.text()
        self.conf.model_ml_file = self.txt_ml_file.text()
        self.conf.model_sgd_file = self.txt_sgd_file.text()
        self.conf.train_data_file = self.txt_train_file.text()
        self.conf.spell_file = self.txt_spell_file.text()
        self.conf.location_zarflar = self.txt_loc_keywords_file.text()
        self.conf.stopwords_file = self.txt_stopwords_file.text()
        self.conf.model_crf_file = self.txt_model_crf_file.text()
        self.conf.annotated_file = self.txt_annotated_file.text()
        self.conf.tagged_sentences = self.txt_ner_file.text()
        self.conf.model_bow_transformer_file = self.txt_bow_transform_file.text()
        self.conf.model_tfidf_transformer_file = self.txt_tfidf_transform_file.text()
        self.conf.access_token = self.txt_access_token.text()
        self.conf.access_token_secret = self.txt_access_token_secret.text()
        self.conf.consumer_key = self.txt_consumer_key.text()
        self.conf.consumer_secret = self.txt_consumer_secret.text()
        self.conf.save_paths()

    # def load_models(self):
    #     if self.modelRunner.modelTrainer.bow_transformer == None:
    #         self.modelRunner.modelTrainer.bow_transformer =

    def browse_mnb_file(self):
        directory = QtWidgets.QFileDialog.getOpenFileName(self, "Pick a file")
        if directory:
            self.conf.model_mnb_file = directory

    def browse_ml_file(self):
        directory = QtWidgets.QFileDialog.getOpenFileName(self, "Pick a file")
        if directory:
            self.conf.model_ml_file = directory

    def browse_sgd_file(self):
        directory = QtWidgets.QFileDialog.getOpenFileName(self, "Pick a file")
        if directory:
            self.conf.model_sgd_file = directory

    def browse_spell_file(self):
        directory = QtWidgets.QFileDialog.getOpenFileName(self, "Pick a file")
        if directory:
            self.conf.spell_file = directory

    def browse_sw_file(self):
        directory = QtWidgets.QFileDialog.getOpenFileName(self, "Pick a file")
        if directory:
            self.conf.stopwords_file = directory

    def browse_ner_file(self):
        directory = QtWidgets.QFileDialog.getOpenFileName(self, "Pick a file")
        if directory:
            self.txt_mnb_file.setText(directory)

    def browse_folder(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Pick a folder")
        if directory:
            self.conf.stopwords_file = directory
            self.conf.spell_file = directory
            self.conf.model_mnb_file = directory
            self.conf.model_ml_file = directory
            self.conf.model_sgd_file = directory

    def classifier_selected(self):
        pass

    def vectorizer_selected(self):
        pass

    def transformer_selected(self):
        pass

    def action_fetch_tweets(self, checked):
        self.streamRunner.streamCatcher.event_detector.create_emitter()
        self.streamRunner.streamCatcher.event_detector.analyse_event_data()
        self.modelRunner.modelTrainer.load_from_files()
        self.streamRunner.streamCatcher.set_model(self.modelRunner.modelTrainer)
        self.streamRunner.streamCatcher.event_detector.emitter.update_event_progress.connect(self.update_event_rates)
        if checked:
            self.streamRunner.start()
        else:
            self.streamRunner.terminate()

    def update_event_rates(self, events):
        self.progress_terror.setValue(events[0])
        self.progress_traffic.setValue(events[1])
        self.progress_flood.setValue(events[2])
        self.progress_eq.setValue(events[3])
        self.progress_fire.setValue(events[4])

    def action_save_conf(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)

        msg.setText("Configuration file will be overwritten, Continue?")
        msg.setWindowTitle("Save Configuration")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

        retval = msg.exec_()
        if retval == 'OK':
            self.conf.save_conf()
            # self.conf.load_conf()

    def train_action_triggered(self, checked):
        self.conf.ngram = tuple(map(int, str(self.cv_ngram.currentText()).split(sep='-')))
        self.conf.min_df = self.min_df.value()
        self.conf.max_df = self.max_df.value()
        self.conf.use_idf = self.cb_useidf.isChecked()
        self.conf.sublinear_tf = self.cb_sublineartf.isChecked()
        self.conf.recalc = not self.cb_recalc.isChecked()

        self.conf.multiclass = self.multi_class.currentText()
        self.conf.C = self.c.value()
        self.conf.penalty = self.penalty.currentText()
        self.conf.coef0 = self.coef0.value()
        self.conf.epsilon = self.epsilon.value()
        self.conf.degree = self.degree.value()
        self.conf.decision_function_shape = None if self.decision_function_shape.currentText() == 'None' else \
                                                    self.decision_function_shape.currentText()
        self.conf.tol = self.tol.value()
        self.conf.max_iter = self.max_iter.value()
        self.conf.fit_intercept = self.fit_intercept.isChecked()
        self.conf.nu = self.nu.value()
        self.conf.cache_size = self.cache_size.value()
        self.conf.class_weight = self.class_weight.currentText()
        self.conf.shrinking = self.shrinking.isChecked()
        self.conf.gamma = self.gamma.currentText()
        self.conf.dual = self.dual.isChecked()
        self.conf.kernel = self.kernel.currentText()
        self.conf.probability = self.probability.isChecked()
        self.conf.intercept_scaling = self.intercept_scaling.value()
        self.conf.loss = self.loss.currentText()
        self.conf.verbose = self.verbose.isChecked()
        self.conf.random_state = self.random_state.currentText()

        self.conf.cb_remlinks = self.cb_remlinks.isChecked()
        self.conf.cb_remchars = self.cb_remchars.isChecked()
        self.conf.cb_remnonwords = self.cb_remnonwords.isChecked()
        self.conf.cb_rempunctuation = self.cb_rempunctuation.isChecked()
        self.conf.cb_spellcheck = self.cb_spellcheck.isChecked()
        self.conf.cb_stopwords = self.cb_stopwords.isChecked()

        self.tabWidget.setCurrentIndex(3)
        self.modelRunner.modelTrainer.create_emitter()
        self.modelRunner.modelTrainer.emitter.update_progress.connect(self.update_train_progress)
        self.modelRunner.modelTrainer.emitter.uptade_train_text.connect(self.update_train_step)
        if checked:
            self.modelRunner.start()
        else:
            self.modelRunner.terminate()

    # FOLDER & FILE PATHS

    def set_mnb_file(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Pick a folder")
        if directory:
            self.txt_mnb_file.setText(directory+'/model_mnb.pkl')
            self.conf.model_mnb_file = directory

    def set_ml_file(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Pick a folder")
        if directory:
            self.txt_ml_file.setText(directory+'/model_ml.pkl')
            self.conf.model_ml_file = directory

    def set_sgd_file(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Pick a folder")
        if directory:
            self.txt_sgd_file.setText(directory+'/model_sgd.pkl')
            self.conf.model_sgd_file = directory

    def set_ner_file(self):
        directory = QtWidgets.QFileDialog.getOpenFileName(self, "Pick a folder")
        if directory:
            self.txt_ner_file.setText(directory)
            self.conf.ner_file = directory

    def set_train_file(self):
        directory = QtWidgets.QFileDialog.getOpenFileName(self, "Pick a folder")
        if directory:
            self.txt_train_file.setText(directory)
            self.conf.train_data_file = directory

    def set_spell_file(self):
        directory = QtWidgets.QFileDialog.getOpenFileName(self, "Pick a folder")
        if directory:
            self.txt_spell_file.setText(directory)
            self.conf.spell_file = directory

    def set_stopwords_file(self):
        directory = QtWidgets.QFileDialog.getOpenFileName(self, "Pick a folder")
        if directory:
            self.txt_stopwords_file.setText(directory)
            self.conf.stopwords_file = directory

    def set_loc_file(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Pick a folder")
        if directory:
            self.txt_loc_file.setText(directory)
            self.txt_mnb_file.setText(directory)

    def set_annotated_file(self):
        directory = QtWidgets.QFileDialog.getOpenFileName(self, "Pick a folder")
        if directory:
            self.txt_annotated_file.setText(directory)
            self.conf.annotated_file = directory

    def update_train_progress(self, val):
        self.train_progress_bar.setValue(val)
        if val >= 100:
            self.modelRunner.terminate()
            self.actionTrain.setChecked(False)
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)

            msg.setText("Train process finished")
            msg.setWindowTitle("Train finished")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            retval = msg.exec_()
            self.train_progress_bar.setValue(0)

    def update_train_step(self, text):
        self.txt_progress_step.setText(text)

# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     # app.setStyle(QtWidgets.QStyleFactory.create('windows'))
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

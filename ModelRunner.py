from ModelTrainer import ModelTrainer
from PyQt5.QtCore import QThread, pyqtSignal
import threading


class ModelRunner(QThread):
    update_progress = pyqtSignal(int)

    def __init__(self, conf):
        super(ModelRunner, self).__init__()
        self.modelTrainer = ModelTrainer(conf=conf)

    def setup_model(self):
        self.modelTrainer.setup()

    def run(self):
        # threading._start_new_thread(function=self.setup_model())
        self.modelTrainer.setup()

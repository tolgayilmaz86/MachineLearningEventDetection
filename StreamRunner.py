from StreamCatcher import StreamCatcher
from PyQt5.QtCore import QThread, pyqtSignal
import threading


class StreamRunner(QThread):
    update_progress = pyqtSignal(int)

    def __init__(self, conf):
        super(StreamRunner, self).__init__()
        self.streamCatcher = StreamCatcher(conf=conf)

    def run(self):
        # threading._start_new_thread(function=self.setup_model())
        self.streamCatcher.start()

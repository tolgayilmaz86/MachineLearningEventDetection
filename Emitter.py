from PyQt5.QtCore import QObject, pyqtSignal


class Emitter(QObject):
    update_progress = pyqtSignal(int)
    uptade_train_text = pyqtSignal(str)
    update_event_progress = pyqtSignal(list)

    def __init__(self):
        super(Emitter, self).__init__()

    def emit_progress(self, val):
        self.update_progress.emit(val)

    def emit_train_text(self, text):
        self.uptade_train_text.emit(text)

    def emit_event_rates(self, events):
        self.update_event_progress.emit(events)

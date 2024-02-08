import sys
from MainWindow import MainWindow
from PyQt5 import QtWidgets


def main():
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyle(QtWidgets.QStyleFactory.create('windows'))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QFileDialog
from PyQt4.uic.uiparser import QtCore

__author__ = 'daniel'
import sys
from PyQt4 import QtGui
from ldaplusplus import Ui_LDAPlusPlus
from logic.ldaConfig import LdaConfig
from logic.lda_logic import ldaLogic
from logic.ldaLogicLabelExtraction import ldaLogicLabels
from threadDialog import ThreadManagerDialog
import cProfile
import logging

logging.basicConfig(filename="lsa_eval.txt", format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.DEBUG)

method = "label"
#method = "pattern"

class Editor(QtGui.QMainWindow):

    def __init__(self):
        super(Editor, self).__init__()
        self.ui=Ui_LDAPlusPlus()
        self.ui.setupUi(self)
        self.show()
        self.ui.chooseMainFolder.clicked.connect(self.choose_main_data_folder)
        self.ui.chooseContextFolder.clicked.connect(self.choose_context_data_folder)
        self.ui.startButton.clicked.connect(self.start)

    def choose_main_data_folder(self):
        self.main_folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

    def choose_context_data_folder(self):
        self.context_folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))


    # def start(self):
    #     th = ThreadManagerDialog(self)
    #     th.workerThread = CounterThread(th)
    #     th.run()
    #     th.show()

    def start(self):
        sax_duration = int(self.ui.saxDuration.text())
        alphabet_size = int(self.ui.alphabetSize.text())
        word_length = int(self.ui.wordLength.text())
        distribution_window = int(self.ui.distributionWindow.text())
        document_window = int(self.ui.documentWindow.text())
        training_time = int(self.ui.trainingTime.text())
        thread_dialog = ThreadManagerDialog(self)
        lda_config = LdaConfig(None, training_time=training_time, word_length=word_length, word_duration=sax_duration,
                               windows_size=document_window, distribution_window_size=distribution_window,
                               alphabet_size=alphabet_size, num_topics=15)
        if method is "label":
            thread_dialog.workerThread = ldaLogicLabels(lda_config, self.main_folder, self.context_folder, thread_dialog)
        elif method is "pattern":
            thread_dialog.workerThread = ldaLogic(lda_config, self.main_folder, self.context_folder, thread_dialog)
        else:
            raise Exception("Method %s is not supported!" % method)
        print "Reading in Streams"
        thread_dialog.workerThread.read_in_streams()
        # cProfile.runctx('thread_dialog.workerThread.read_in_streams()', {'thread_dialog': thread_dialog}, {})
        print "Starting lda plus plus"
        thread_dialog.run()
        # cProfile.runctx('thread_dialog.run()', {'thread_dialog': thread_dialog}, {})
        thread_dialog.show()
        # logic.start()
        # self.initialize_config()
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Editor()
    # connect_buttons(ex.ui)
    sys.exit(app.exec_())


# @pyqtSlot()
# def connect_buttons(app):
#     app.pushButton.connect(app.pushButton, QtCore.SIGNAL('clicked()'), choose_file)
    # app.pushButton.clicked(choose_file)
    # app.pushButton_2.clicked(choose_file())


if __name__ == '__main__':
    main()
import os
import sys
import time
import datetime
from datetime import date
from threading import Thread
from pynput.keyboard import Key, Controller

import pandas as pd
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QGridLayout,
                             QGroupBox, QDialog, QVBoxLayout, QTableView, QLineEdit, QTextEdit)
from PyQt5.QtWidgets import QMessageBox


class PandasTable(QAbstractTableModel):
    def __init__(self, df):
        QAbstractTableModel.__init__(self)
        self._df = df

    def rowCount(self, parent=None):
        try:
            return self._df.shape[0]
        except IndexError as e:
            return 1

    def columnCount(self, parent=None):
        try:
            return self._df.shape[1]
        except IndexError as e:
            return 1

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._df.iloc[index.row(), index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._df.columns[col]
        return None

'''Classe finestra inserimento'''
class Window2(QDialog):

    def __init__(self):
        super().__init__()

        today = str(datetime.datetime.today().strftime("%Y-%b-%d"))
        today = "ReportGiornaliero/" + today
        self.mac_daily_folder = os.path.abspath(
            os.path.join(sys.executable + "ReportGiornaliero/", "..", '..', "..", '..', "ReportGiornaliero/"))
        self.mac_daily_path = os.path.abspath(
            os.path.join(sys.executable + today + "_prodotti.csv", "..", '..', '..', '..', '..', today + "_prodotti.csv"))
        self.mac_file_path = os.path.abspath(
            os.path.join(sys.executable + "/prodotti.csv", '..', '..', '..', "..", "..",
                         "prodotti.csv"))
        self.df = None
        self.title = "Inserisci Prodotto"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500

        # variable for safe save confirmation pop up
        self.security = False

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        self.show()

    def load_df(self):
        if not self.df:
            self.df = pd.read_csv(self.mac_file_path)

    def append_to_db(self, s_list):
        df = pd.read_csv(self.mac_file_path)
        if not self.mac_file_path:
            index_list = ["CodiceProdotto", "Nome", "Descrizione", "QtTotale", "QtaMagazzino", "QtaNegozio", "Taglia",
                          "Colore", "Stagione", "Anno", "Data"]
            to_add_series = pd.Series(s_list, index=index_list)
            df.append(to_add_series, ignore_index=True)
            df.to_csv(self.mac_file_path)
            #print("initialization dir:" + self.mac_file_path)

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Inserisci un prodotto")
        layout = QGridLayout()
        layout.setColumnStretch(1, 8)
        layout.setColumnStretch(2, 8)

        layout = QtWidgets.QGridLayout()

        codprod = QtWidgets.QLabel("Codice prodotto")
        layout.addWidget(codprod, 0, 0)
        self.codiceprod = QtWidgets.QTextEdit()
        print(type(self.codiceprod))
        layout.addWidget(self.codiceprod, 0, 1)

        nome = QtWidgets.QLabel("Nome")
        layout.addWidget(nome, 1, 0)
        self.nomeprod = QtWidgets.QLineEdit()
        layout.addWidget(self.nomeprod, 1, 1)

        descrizione = QtWidgets.QLabel("Descrizione")
        layout.addWidget(descrizione, 2, 0)
        self.descprod = QtWidgets.QTextEdit()
        layout.addWidget(self.descprod, 2, 1)

        stagione = QtWidgets.QLabel("Stagione")
        layout.addWidget(stagione, 3, 0)
        self.stagione = QtWidgets.QLineEdit()
        layout.addWidget(self.stagione, 3, 1)

        anno = QtWidgets.QLabel("Anno")
        layout.addWidget(anno, 0, 2)
        self.anno = QtWidgets.QLineEdit()
        layout.addWidget(self.anno, 0, 3)

        qtaneg = QtWidgets.QLabel("QtaNegozio")
        layout.addWidget(qtaneg, 1, 2)
        self.qtanegozio = QtWidgets.QSpinBox()
        layout.addWidget(self.qtanegozio, 1, 3)

        qtamag = QtWidgets.QLabel("QtaMagazzino")
        layout.addWidget(qtamag, 2, 2)
        self.qtamagazzino = QtWidgets.QSpinBox()
        layout.addWidget(self.qtamagazzino, 2, 3)

        messageBox = QtWidgets.QLabel("Box Messaggi")
        layout.addWidget(messageBox, 4, 2)
        self.communication = QtWidgets.QLabel()
        layout.addWidget(self.communication, 4, 3)

        taglia = QtWidgets.QLabel("Taglia")
        layout.addWidget(taglia, 4, 0)
        self.tag = QtWidgets.QLineEdit()
        layout.addWidget(self.tag, 4, 1)

        self.df = self.load_csv()

        colore = QtWidgets.QLabel("Colore")
        layout.addWidget(colore, 3, 2)
        self.col = QtWidgets.QLineEdit()

        layout.addWidget(self.col, 3, 3)

        self.buttonOK = QtWidgets.QPushButton("SALVA", self)
        layout.addWidget(self.buttonOK, 6, 3)

        self.setLayout(layout)
        self.codiceprod.setMinimumSize(80, 20)
        self.codiceprod.setMaximumSize(1020, 20)
        self.descprod.setMinimumSize(80, 20)
        self.descprod.setMaximumSize(1020, 100)
        self.codiceprod.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.buttonOK.clicked.connect(self.buttonOK_clicked)

        # update ad inserimento di ogni char
        # elimina il carattere new line \n e si attiva a stringa completa (secondo input pistola)
        if self.codiceprod is None:
            self.codiceprod.textChanged.connect(lambda what=None: self.setPolishedText(None))
        else:
            self.codiceprod.textChanged.connect(lambda what=self.codiceprod: self.setPolishedText(self.codiceprod.toPlainText()))
            # chiama funzione per mostrare modalita' editing o insert
            self.codiceprod.textChanged.connect(lambda what=self.codiceprod: self.warn_about_change(self.codiceprod.toPlainText()))

    # funzione per segnalare a schermo la MODIFICA di un parametro o l'inserimento di una nuova voce
    def warn_about_change(self, text):
        if self.df.loc[self.df.CodiceProdotto == text].any().any():
            self.communication.setText("ATTENZIONE!!!\nStai per sovrascrivere i valori\ncorrispondenti al codice prodotto\nselezionato")
            self.communication.show()
            print(str(self.df.loc[self.df.CodiceProdotto == text, "Descrizione"]).split(" "))
            self.nomeprod.setText(str(self.df.loc[self.df.CodiceProdotto == text, "Nome"]).split(" ")[4].split("\n")[0])
            self.descprod.setText("\n".join(str(str(self.df.loc[self.df.CodiceProdotto == text, "Descrizione"]).split(" ")[4]).split("\n")[:-1]).replace("\\n", "\n"))
            self.stagione.setText(str(self.df.loc[self.df.CodiceProdotto == text, "Stagione"]).split(" ")[4].split("\n")[0])
            self.anno.setText(str(self.df.loc[self.df.CodiceProdotto == text, "Anno"]).split(" ")[4].split("\n")[0])
            self.tag.setText(str(self.df.loc[self.df.CodiceProdotto == text, "Taglia"]).split(" ")[4].split("\n")[0])
            self.col.setText(str(self.df.loc[self.df.CodiceProdotto == text, "Colore"]).split(" ")[4].split("\n")[0])
            self.qtanegozio.setValue(int(str(self.df.loc[self.df.CodiceProdotto == text, "QtaNegozio"]).split(" ")[4].split("\n")[0]))
            self.qtamagazzino.setValue(int(str(self.df.loc[self.df.CodiceProdotto == text, "QtaMagazzino"]).split(" ")[4].split("\n")[0]))
            self.security = True
        else:
            self.communication.setText(
                "Stai inserendo una\nnuova voce nel database")
            self.communication.show()
            self.nomeprod.setText("")
            self.descprod.setText("")
            self.stagione.setText("")
            self.anno.setText("")
            self.tag.setText("")
            self.col.setText("")
            self.qtanegozio.setValue(0)
            self.qtamagazzino.setValue(0)
            self.security = False

    # metodo per conferma editing (non si attiva con inserimento nuova voce)
    def safe_save(self):
        qm = QMessageBox()
        response = qm.question(self, '', "Vuoi davvero sovrascrivere la voce già presente nel Database_", qm.Yes | qm.No)
        if response == qm.Yes:
            # invoca metodo per salvare contenuti
            self.security = False
            self.buttonOK_clicked
            self.communication.setText("Premi SALVA per convalidare la modifica\nChiudi finestra per annullare")
        else:
            pass


    # funzione connessa al commento precedente
    def setPolishedText(self, codice=None):
        if not codice:
            pass
        elif "\n" in codice:
            self.codiceprod.setText(self.codiceprod.toPlainText().strip("\n").strip())
        else:
            pass

    # funzione update via MODIFICA del database
    # TODO: aggiungere field mancanti, generare output nel message box, chiedere eventualmente conferma per le mods
    def update_list(self, df, text, data):
        pd.set_option('display.max_columns', None)
        #print(df)
        if data[5].isdigit(): # qt Negozio
            df.loc[df.CodiceProdotto == text, 'QtaNegozio'] = int(
                df.loc[df.CodiceProdotto == text, 'QtaNegozio']) * 0 + int(data[5])  # togliere il *0 per trasformare la funzione da funzione di sovrascrittura a funzione di update
            df.loc[df.CodiceProdotto == text, 'QtTotale'] = int(
                df.loc[df.CodiceProdotto == text, 'QtaNegozio']) + int(df.loc[df.CodiceProdotto == text, 'QtaMagazzino'])
        else:
            print("not matching int")

        if data[4].isdigit(): # qta Magazzino
            df.loc[df.CodiceProdotto == text, 'QtaMagazzino'] = int(
                df.loc[df.CodiceProdotto == text, 'QtaMagazzino']) * 0 + int(data[4])
            df.loc[df.CodiceProdotto == text, 'QtTotale'] = int(
                df.loc[df.CodiceProdotto == text, 'QtaNegozio']) + int(
                df.loc[df.CodiceProdotto == text, 'QtaMagazzino'])
        else:
            print("not matching int")

        if data[1]: # nome prodotto
            print(data[1])
            print(df.loc[df.CodiceProdotto == text, 'Nome'])
            df.loc[df.CodiceProdotto == text, 'Nome'] = data[1]
        else:
            print("not matching str")

        if data[2].isalnum(): # descrizione prodotto
            df.loc[df.CodiceProdotto == text, 'Descrizione'] = data[2]
        else:
            print("not matching str")

        if data[6]: # taglia prodotto
            df.loc[df.CodiceProdotto == text, 'Taglia'] = data[6]
        else:
            print("not matching str")

        if data[7]: # colore prodotto
            df.loc[df.CodiceProdotto == text, 'Colore'] = data[7]
        else:
            print("not matching str")

        if data[8]: # stagione prodotto
            df.loc[df.CodiceProdotto == text, 'Stagione'] = data[8]
        else:
            print("not matching str")

        if data[9]: # anno prodotto
            df.loc[df.CodiceProdotto == text, 'Anno'] = data[9]
        else:
            print("not matching str")

        if data[10]: # data inserimento prodotto
            df.loc[df.CodiceProdotto == text, 'Data'] = data[10]
        else:
            print("not matching str")

    def load_csv(self):
        try:
            df = pd.read_csv(self.mac_file_path)
            try:
                daily_df = pd.read_csv(self.mac_daily_path)
            except Exception as e:
                print(e)
                daily_df = self.create_daily_db()
            # print(df)
            self.daily_df = daily_df
            return df
        except FileNotFoundError as e:
            df = self.create_db()
            try:
                daily_df = pd.read_csv(self.mac_daily_path)
            except Exception as e:
                print(e)
                daily_df = self.create_daily_db()
            self.daily_df = daily_df
            return df

    def create_daily_db(self):
        data_list = ["#", "initialization row", "no", 0, 0, 0,
                     "N/A",
                     "N/A", "N/A", "N/A", "N/A"]
        index_list = ["CodiceProdotto", "Nome", "Descrizione", "QtTotale", "QtaMagazzino", "QtaNegozio", "Taglia",
                      "Colore", "Stagione", "Anno", "Data"]

        df = pd.DataFrame(columns=index_list)
        a_series = pd.Series(data_list, index=index_list)
        df = df.append(a_series, ignore_index=True)
        try:
            df.to_csv(self.mac_daily_path, index=False)
        except Exception as e:
            print(self.mac_daily_folder)
            if os.path.isdir(self.mac_daily_folder):
                df.to_csv(self.mac_daily_path, index=False)
            else:
                os.mkdir(self.mac_daily_folder, 0o755)
                df.to_csv(self.mac_daily_path, index=False)

    @staticmethod
    def append_my_df(df1, df2):
        return df1.append(df2)

    @QtCore.pyqtSlot()
    def buttonOK_clicked(self):
        if self.security == False:
            # printing the form information

            codiceprodotto = self.codiceprod.toPlainText().strip()
            print("codice prodotto", codiceprodotto)
            nomeprodotto = self.nomeprod.text()
            descprodotto = self.descprod.toPlainText()
            stagione = self.stagione.text()
            qtanegprodotto = self.qtanegozio.text()
            qtamagprodotto = self.qtamagazzino.text()
            tagliaprodotto = self.tag.text()
            coloreprodotto = self.col.text()
            anno = self.anno.text()
            dataprodotto = date.today()
            qtot = str(int(qtanegprodotto) + int(qtanegprodotto))

            data_list = [codiceprodotto, nomeprodotto, descprodotto, qtot, qtamagprodotto, qtanegprodotto,
                         tagliaprodotto,
                         coloreprodotto, stagione, anno, dataprodotto]
            self.append_to_db(data_list)

            try:
                self.df = self.load_csv()
                if self.df.loc[self.df.CodiceProdotto == codiceprodotto].any().any():
                    # self.df = self.update_list(self.df, codiceprodotto, data_list)
                    self.update_list(self.df, codiceprodotto, data_list)
                    # print(self.df)
                else:
                    m_list = []
                    # save the new df
                    index_list = ["CodiceProdotto", "Nome", "Descrizione", "QtTotale", "QtaMagazzino", "QtaNegozio",
                                  "Taglia", "Colore", "Stagione", "Anno", "Data"]
                    a_series = pd.Series(data_list, index=self.df.columns)
                    self.df = self.df.append(a_series, ignore_index=True)
            except Exception as e:
                print(e)

            finally:
                try:
                    self.df.to_csv(self.mac_file_path, index=False)
                    self.close()
                except Exception as e:
                    self.communication.setText("ATTENZIONE:\ninserire dati validi\nprima di convalidare")
                    self.communication.show()
                    print(e)

            # closing the window
            # self.close()
        else:
            self.safe_save()


class WindowDailyReport(QMainWindow):
    def __init__(self):
        super().__init__()

        self.daily_df = None
        today = str(datetime.datetime.today().strftime("%Y-%b-%d"))
        today = "ReportGiornaliero/" + today
        self.mac_daily_folder = os.path.abspath(
            os.path.join(sys.executable + "ReportGiornaliero/", "..", "..", '..', '..', "ReportGiornaliero/"))
        self.mac_daily_path = os.path.abspath(
            os.path.join(sys.executable + today + "_prodotti.csv", "..", "..", '..', '..', '..', today + "_prodotti.csv"))
        print(self.mac_daily_path)

        self.title = "Report Giornaliero " + str(datetime.datetime.today().strftime("%Y-%m-%d"))
        self.top = 200
        self.left = 200
        self.width = 1120
        self.height = 900
        self.df = self.load_daily_csv()

        self.pandas_table = self.create_table()
        self.pandas_table.setGeometry(30, 30, 1020, 850)
        self.pandas_table.setBaseSize(1020, 850)
        self.setWindowTitle("Report Giornaliero " + str(datetime.datetime.today().strftime("%Y-%m-%d")))

        self.wid = QtWidgets.QWidget()
        self.setCentralWidget(self.wid)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.pandas_table)
        self.wid.setLayout(self.layout)

    def load_daily_csv(self):
        try:
            daily_df = pd.read_csv(self.mac_daily_path)
            self.daily_df = daily_df
            return daily_df
        except Exception as e:
            print(e)
            daily_df = self.create_daily_db()
            self.daily_df = daily_df
            return daily_df

    def create_daily_db(self):
        data_list = ["#", "initialization row", "no", 0, 0, 0,
                     "N/A",
                     "N/A", "N/A", "N/A", "N/A"]
        index_list = ["CodiceProdotto", "Nome", "Descrizione", "QtTotale", "QtaMagazzino", "QtaNegozio", "Taglia",
                      "Colore", "Stagione", "Anno", "Data"]

        df = pd.DataFrame(columns=index_list)
        a_series = pd.Series(data_list, index=index_list)
        df = df.append(a_series, ignore_index=True)
        self.daily_df = df

        try:
            df.to_csv(self.mac_daily_path, index=False)
        except Exception as e:
            print(self.mac_daily_folder)
            if os.path.isdir(self.mac_daily_folder):
                df.to_csv(self.mac_daily_path, index=False)
            else:
                os.mkdir(self.mac_daily_folder, 0o755)
                df.to_csv(self.mac_daily_path, index=False)
        return df

    def create_table(self):
        # create the view
        tv = QTableView()

        # set the table model
        tablemodel = PandasTable(self.load_daily_csv())
        tv.setModel(tablemodel)
        tv.setBaseSize(995, 800)
        # hide grid
        tv.setShowGrid(False)

        vh = tv.verticalHeader()
        vh.setVisible(True)

        # set horizontal header properties
        hh = tv.horizontalHeader()
        hh.setStretchLastSection(True)

        # set row height
        tv.resizeRowsToContents()

        # enable sorting
        tv.setSortingEnabled(False)
        return tv


class Window3(QMainWindow):  # <===
    def __init__(self):
        super().__init__()

        self.daily_df = None

        self.mac_file_path = os.path.abspath(
            os.path.join(sys.executable + "/prodotti.csv", "..", '..', '..', '..', '..', "prodotti.csv"))

        today = str(datetime.datetime.today().strftime("%Y-%b-%d"))
        today = "ReportGiornaliero/" + today
        self.mac_daily_folder = os.path.abspath(
            os.path.join(sys.executable + "ReportGiornaliero/", "..", "..", '..', '..', "ReportGiornaliero/"))
        self.mac_daily_path = os.path.abspath(
            os.path.join(sys.executable + today + "_prodotti.csv", "..", "..", '..', '..', '..', today + "_prodotti.csv"))
        print(self.mac_daily_path)

        self.setWindowTitle("Cerca prodotti")
        self.title = "Cerca Prodotto"
        self.top = 200
        self.left = 200
        self.width = 1120
        self.height = 900
        self.df = self.load_csv()

        self.pandas_table = self.create_table()
        self.pandas_table.setGeometry(30, 30, 1020, 850)
        self.pandas_table.setBaseSize(1020, 850)
        self.line_edit = QTextEdit()
        self.line_edit.move(30, 30)
        self.line_edit.resize(1020, 30)
        self.line_edit.adjustSize()
        self.line_edit.setMinimumSize(800, 30)
        self.line_edit.setMaximumSize(1020, 30)
        self.label = QLabel()
        self.label.setText("Inserire un ID valido per modificare i valori NEGOZIO e TOTALE")
        self.label_instructions = QLabel()
        self.label_instructions.setText("- Il valore TOTALE viene calcolato come la somma di NEGOZIO e MAGAZZINO")
        self.wid = QtWidgets.QWidget()
        self.setCentralWidget(self.wid)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.label_instructions)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.pandas_table)
        self.wid.setLayout(self.layout)

        self.line_edit.setFocus()
        self.line_edit.setMinimumSize(800, 30)
        self.line_edit.setMaximumSize(1020, 30)
        self.daily_table = QPushButton("Report Giornaliero", self)

        self.daily_table.setGeometry(950, 10, 150, 30)
        self.daily_table.clicked.connect(self.windowDailyReport)
        Keyboard = Controller()
        Keyboard.press(Key.enter)
        Keyboard.release(Key.enter)

        if self.line_edit is None:
            self.line_edit.textChanged.connect(lambda what=None: self.check_existence(None))
        else:
            print("controllo testo:", self.line_edit.toPlainText())
            self.line_edit.textChanged.connect(lambda what=self.line_edit: self.check_existence(what.toPlainText()))

    def update_widget(self, row=None):
        self.pandas_table = self.create_table(row)
        self.pandas_table.setGeometry(30, 30, 1020, 850)
        self.pandas_table.setBaseSize(1020, 850)
        self.line_edit = QTextEdit()
        self.line_edit.move(30, 30)
        self.line_edit.resize(1020, 30)
        self.line_edit.adjustSize()
        self.line_edit.setMinimumSize(800, 30)
        self.line_edit.setMaximumSize(1020, 30)
        self.label = QLabel()
        self.label.setText("Inserire un ID valido per modificare i valori NEGOZIO e TOTALE")
        self.label_instructions = QLabel()
        self.label_instructions.setText("- Il valore TOTALE viene calcolato come la somma di NEGOZIO e MAGAZZINO")
        self.wid = QtWidgets.QWidget()
        self.setCentralWidget(self.wid)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.label_instructions)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.pandas_table)
        self.wid.setLayout(self.layout)
        self.line_edit.setFocus()
        self.line_edit.setMinimumSize(800, 30)
        self.line_edit.setMaximumSize(1020, 30)

        self.first_run = True

        if self.line_edit is None:
            print("my text no codice 2:", self.line_edit.toPlainText())
            self.line_edit.textChanged.connect(lambda what=None: self.setPolishedText(None))
        else:
            self.line_edit.textChanged.connect(lambda what=self.line_edit: self.setPolishedText(self.line_edit.toPlainText()))

    def setPolishedText(self, codice=None):
        keyboard = Controller()
        if not codice:
            pass
        elif "\n" in codice:

            self.line_edit.textChanged.connect(lambda what=self.line_edit: self.check_existence(what.toPlainText()))
            self.line_edit.setText(self.line_edit.toPlainText().strip("\n").strip())
            if len(self.line_edit.toPlainText()) > 1:
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
        else:
            pass

    def create_table(self, row=None):
        # create the view
        tv = QTableView()

        # set the table model
        if row is None:
            tablemodel = PandasTable(self.load_csv())
        else:
            tablemodel = PandasTable(row)

        tv.setModel(tablemodel)
        tv.setBaseSize(995, 800)

        # hide grid
        tv.setShowGrid(False)

        vh = tv.verticalHeader()
        vh.setVisible(True)

        # set horizontal header properties
        hh = tv.horizontalHeader()
        hh.setStretchLastSection(True)

        # set row height
        tv.resizeRowsToContents()

        # enable sorting
        tv.setSortingEnabled(False)

        return tv

    def check_existence(self, text=None):
        if text is None:
            pass
        else:
            if self.df is None:
                self.load_df()
                self.update_widget()
            else:
                if self.df.loc[self.df.CodiceProdotto == text].any().any():

                    self.df.loc[self.df.CodiceProdotto == text, 'QtaNegozio'] = self.df.loc[self.df.CodiceProdotto == text, 'QtaNegozio'] - 1
                    if int(self.df.loc[self.df.CodiceProdotto == text, 'QtaNegozio']) < 1:
                        self.df.loc[self.df.CodiceProdotto == text, 'QtaNegozio'] = 0
                        '''attivare alert'''
                        QMessageBox.about(self, "ATTENZIONE", "prodotto " + text + " esaurito in negozio")
                        print(self.df.loc[self.df.CodiceProdotto == text, 'QtaNegozio'])

                        # salva riga con alert (e prodotto relativo) in daily report
                        self.update_daily(self.df.loc[self.df.CodiceProdotto == text, 'CodiceProdotto'],
                                          self.df.loc[self.df.CodiceProdotto == text, 'QtaNegozio'],
                                          self.df.loc[self.df.CodiceProdotto == text, 'QtaMagazzino'],
                                          self.df, self.df.index[self.df.CodiceProdotto == text])

                    self.df.loc[self.df.CodiceProdotto == text, 'QtTotale'] = self.df.loc[
                                                                                  self.df.CodiceProdotto == text, 'QtTotale'] - 1
                    if int(self.df.loc[self.df.CodiceProdotto == text, 'QtTotale']) != (
                            int(self.df.loc[self.df.CodiceProdotto == text, 'QtaNegozio']) + int(
                            self.df.loc[self.df.CodiceProdotto == text, 'QtaMagazzino'])):
                        self.df.loc[self.df.CodiceProdotto == text, 'QtTotale'] = int(
                            self.df.loc[self.df.CodiceProdotto == text, 'QtaNegozio']) + int(
                            self.df.loc[self.df.CodiceProdotto == text, 'QtaMagazzino'])

                    pd.set_option('display.max_columns', None)
                    self.df.to_csv(self.mac_file_path, index=False)
                    self.update_widget(row=self.df.loc[self.df.CodiceProdotto == text])
                else:
                    self.update_widget()
                    pass

    def load_csv(self):
        try:
            df = pd.read_csv(self.mac_file_path)
            try:
                daily_df = pd.read_csv(self.mac_daily_path)
            except Exception as e:
                print(e)
                daily_df = self.create_daily_db()
            self.daily_df = daily_df
            return df
        except FileNotFoundError as e:
            df = self.create_db()
            try:
                daily_df = pd.read_csv(self.mac_daily_path)
            except Exception as e:
                print(e)
                daily_df = self.create_daily_db()
            self.daily_df = daily_df
            return df

    def create_daily_db(self):
        data_list = ["#", "initialization row", "no", 0, 0, 0,
                     "N/A",
                     "N/A", "N/A", "N/A", "N/A"]
        index_list = ["CodiceProdotto", "Nome", "Descrizione", "QtTotale", "QtaMagazzino", "QtaNegozio", "Taglia",
                      "Colore", "Stagione", "Anno", "Data"]

        df = pd.DataFrame(columns=index_list)
        a_series = pd.Series(data_list, index=index_list)
        df = df.append(a_series, ignore_index=True)
        self.daily_df = df

        try:
            df.to_csv(self.mac_daily_path, index=False)
        except Exception as e:
            print(self.mac_daily_folder)
            if os.path.isdir(self.mac_daily_folder):
                df.to_csv(self.mac_daily_path, index=False)
            else:
                os.mkdir(self.mac_daily_folder, 0o755)
                df.to_csv(self.mac_daily_path, index=False)

    def update_daily(self, codice_prodotto, qta_negozio, qta_magazzino, df, index):
        zero_series = df.iloc[index].squeeze()
        self.daily_df = self.daily_df.append(zero_series, ignore_index=True)
        self.daily_df.drop_duplicates(subset="CodiceProdotto", inplace=True)
        self.daily_df.to_csv(self.mac_daily_path, index=False)

    def create_db(self):
        if not os.path.isfile(self.mac_file_path):
            data_list = ["#", "initialization row", "no", 0, 0, 0,
                         "N/A",
                         "N/A", "N/A", "N/A", "N/A"]
            index_list = ["CodiceProdotto", "Nome", "Descrizione", "QtTotale", "QtaMagazzino", "QtaNegozio", "Taglia",
                          "Colore", "Stagione", "Anno", "Data"]

            df = pd.DataFrame(columns=index_list)
            a_series = pd.Series(data_list, index=self.df.columns)
            df = df.append(a_series, ignore_index=True)
            df.to_csv(self.mac_file_path, index=False)
            #print("initialization dir:" + self.mac_file_path)
            return df
        else:
            #print("csv exists", self.mac_file_path)
            pass

    def windowDailyReport(self):  # <===
        self.w = WindowDailyReport()
        self.w.setWindowTitle(self.w.title)
        self.w.setGeometry(self.w.top, self.w.left, self.w.width, self.w.height)
        self.w.show()

    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        self.df = self.load_csv()
        # self.loadCsv()

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Home"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500

        self.mac_file_path = os.path.abspath(
            os.path.join(sys.executable + "/prodotti.csv", "..", '..', '..', '..', '..', "prodotti.csv"))

        self.pushButton = QPushButton("Inserisci / modifica", self)
        styles = """background-color: orange;
                    border-style: outset;
                    border-width: 2px;
                    border-radius: 15px;
                    border-color: #777777;
                    padding: 0px;
                    color: #777777;"""
        self.pushButton.setStyleSheet(styles)
        self.pushButton.setMinimumSize(150, 30)
        self.pushButton.move(self.width/2 - 150/2, 200)
        self.pushButton.setToolTip("<h3>Inserisci o modifica</h3>")
        self.pushButton.clicked.connect(self.window2)  # <===
        self.pushButton2 = QPushButton("Cerca", self)
        self.pushButton2.setMinimumSize(100, 30)
        self.pushButton2.move(self.width/2 - 100/2, 250)
        self.pushButton2.setStyleSheet(styles)
        self.pushButton2.setToolTip("<h3>Cerca</h3>")

        self.pushButton2.clicked.connect(self.window3)  # <===

        self.create_db()
        self.main_window()

    def create_db(self):
        if not os.path.isfile(self.mac_file_path):
            data_list = ["#", "initialization row", "no", 0, 0, 0,
                         "N/A",
                         "N/A", "N/A", "N/A", "N/A"]
            index_list = ["CodiceProdotto", "Nome", "Descrizione", "QtTotale", "QtaMagazzino", "QtaNegozio", "Taglia",
                          "Colore", "Stagione", "Anno", "Data"]

            df = pd.DataFrame(columns=index_list)
            a_series = pd.Series(data_list, index=df.columns)
            df = df.append(a_series, ignore_index=True)
            df.to_csv(self.mac_file_path, index=False)
            #print("initialization dir:" + self.mac_file_path)
        else:
            #print("csv exists", self.mac_file_path)
            pass

    def main_window(self):
        self.setWindowTitle(self.title)
        self.image_path = os.path.abspath(
            os.path.join(sys.executable + "/barneys.jpeg", '..', '..', "barneys.jpeg"))
        self.setStyleSheet("background-image: url(" + self.image_path + ");")

        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def window2(self):  # <===
        self.w = Window2()
        self.w.setWindowTitle(self.w.title)
        self.w.setGeometry(self.w.top, self.w.left, self.w.width, self.w.height)
        self.w.show()

    def window3(self):  # <===
        self.w = Window3()
        self.w.setWindowTitle(self.w.title)
        self.w.setGeometry(self.w.top, self.w.left, self.w.width, self.w.height)
        self.w.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
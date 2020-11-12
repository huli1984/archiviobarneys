import csv
import os
import sys
from datetime import date

import pandas as pd
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QGridLayout,
                             QGroupBox, QDialog, QVBoxLayout, QTableView, QLineEdit, QTextEdit)
from PyQt5.QtWidgets import QMessageBox


class PandasTable(QAbstractTableModel):
    def __init__(self, df):
        QAbstractTableModel.__init__(self)
        self._df = df

    def rowCount(self, parent=None):
        return self._df.shape[0]

    def columnCount(self, parent=None):
        return self._df.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._df.iloc[index.row(), index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._df.columns[col]
        return None


class Window2(QDialog):

    def __init__(self):
        super().__init__()

        self.mac_file_path = os.path.abspath(
            os.path.join(sys.executable + "/prodotti.csv", '..', "..", "..",
                         "prodotti.csv"))
        #print(self.mac_file_path)
        self.df = None
        self.title = "Inserisci Prodotto"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
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
                          "Colore", "Hex", "Data"]
            to_add_series = pd.Series(s_list, index=index_list)
            df.append(to_add_series, ignore_index=True)
            df.to_csv(self.mac_file_path)
            #print("initialization dir:" + self.mac_file_path)

    def check_existence(self, text=None):
        pass

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Inserisci un prodotto")
        layout = QGridLayout()
        layout.setColumnStretch(1, 8)
        layout.setColumnStretch(2, 8)

        layout = QtWidgets.QGridLayout()
        codprod = QtWidgets.QLabel("Codice prodotto")
        layout.addWidget(codprod, 0, 0)
        self.codiceprod = QtWidgets.QTextEdit()
        layout.addWidget(self.codiceprod, 0, 1)
        nome = QtWidgets.QLabel("Nome")
        layout.addWidget(nome, 1, 0)

        self.nomeprod = QtWidgets.QLineEdit()
        layout.addWidget(self.nomeprod, 1, 1)
        descrizione = QtWidgets.QLabel("Descrizione")
        layout.addWidget(descrizione, 2, 0)
        self.descprod = QtWidgets.QTextEdit()
        layout.addWidget(self.descprod, 2, 1)
        qtatot = QtWidgets.QLabel("QtaTotale")
        layout.addWidget(qtatot, 3, 0)
        self.qtatotale = QtWidgets.QSpinBox()
        layout.addWidget(self.qtatotale, 3, 1)
        qtaneg = QtWidgets.QLabel("QtaNegozio")
        layout.addWidget(qtaneg, 3, 2)
        self.qtanegozio = QtWidgets.QSpinBox()
        layout.addWidget(self.qtanegozio, 3, 3)
        qtamag = QtWidgets.QLabel("QtaMagazzino")
        layout.addWidget(qtamag, 3, 4)
        self.qtamagazzino = QtWidgets.QSpinBox()
        layout.addWidget(self.qtamagazzino, 3, 5)
        taglia = QtWidgets.QLabel("Taglia")
        layout.addWidget(taglia, 4, 0)
        self.tag = QtWidgets.QComboBox()
        self.tag.addItem("XS")
        self.tag.addItem("S")
        self.tag.addItem("M")
        self.tag.addItem("L")
        self.tag.addItem("XL")
        self.tag.addItem("XXL")

        self.df = self.load_csv()

        layout.addWidget(self.tag, 4, 1)

        colore = QtWidgets.QLabel("Colore")
        layout.addWidget(colore, 4, 2)
        self.col = QtWidgets.QComboBox()
        self.col.addItem("Bianco", "#ffffff")
        self.col.addItem("Rosso", "#ff0000")
        self.col.addItem("Verde", "#00ff00")
        self.col.addItem("Blu", "#0000ff")

        layout.addWidget(self.col, 4, 3)

        self.buttonOK = QtWidgets.QPushButton("SALVA", self)
        layout.addWidget(self.buttonOK, 5, 2)

        self.setLayout(layout)
        self.codiceprod.setMinimumSize(80, 20)
        self.codiceprod.setMaximumSize(1020, 20)
        self.codiceprod.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.buttonOK.clicked.connect(self.buttonOK_clicked)

    def update_list(self, df, text, data):
        pd.set_option('display.max_columns', None)
        #print(df)
        if data[5].isdigit():
            df.loc[df.CodiceProdotto == text, 'QtaNegozio'] = int(df.loc[df.CodiceProdotto == text, 'QtaNegozio']) + int(data[5])
        else:
            #print("not matching int")
            pass
        if data[4].isdigit():
            df.loc[df.CodiceProdotto == text, 'QtaMagazzino'] = int(df.loc[df.CodiceProdotto == text, 'QtaMagazzino']) + int(data[4])
        else:
            #print("not matching int")
            pass
        #print(df)
        return df

    def load_csv(self):
        try:
            df = pd.read_csv(self.mac_file_path)
            return df
        except FileNotFoundError as e:
            df = self.create_db()
            return df

    @staticmethod
    def append_my_df(df1, df2):
        return df1.append(df2)

    @QtCore.pyqtSlot()
    def buttonOK_clicked(self):
        # printing the form information
        codiceprodotto = self.codiceprod.toPlainText()
        nomeprodotto = self.nomeprod.text()
        descprodotto = self.descprod.toPlainText()
        qtatotprodotto = self.qtatotale.text()
        qtanegprodotto = self.qtanegozio.text()
        qtamagprodotto = self.qtamagazzino.text()
        tagliaprodotto = self.tag.currentText()
        coloreprodotto = self.col.currentText()
        hexprodotto = self.col.currentData()
        dataprodotto = date.today()

        data_list = [codiceprodotto, nomeprodotto, descprodotto, qtatotprodotto, qtamagprodotto, qtanegprodotto,
                     tagliaprodotto,
                     coloreprodotto, hexprodotto, dataprodotto]
        self.append_to_db(data_list)
        #print(hexprodotto)
        try:
            self.df = self.load_csv()
            if self.df.loc[self.df.CodiceProdotto == codiceprodotto].any().any():
                self.df = self.update_list(self.df, codiceprodotto, data_list)
                #print(self.df)
            else:
                m_list = []
                '''save the new df'''
                index_list = ["CodiceProdotto", "Nome", "Descrizione", "QtTotale", "QtaMagazzino", "QtaNegozio",
                              "Taglia",
                              "Colore", "Hex", "Data"]
                a_series = pd.Series(data_list, index=self.df.columns)
                self.df = self.df.append(a_series, ignore_index=True)
        except Exception as e:
            #print("errore:", e)
            #print("contattare l'amministratore")
            pass

        finally:
            self.df.to_csv(self.mac_file_path, index=False)

        # closing the window
        self.close()


class Window3(QMainWindow):  # <===
    def __init__(self):
        super().__init__()
        self.mac_file_path = os.path.abspath(
            os.path.join(sys.executable + "/prodotti.csv", "..", '..', '..', "prodotti.csv"))

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
        self.line_edit.setMinimumSize(800, 30)
        self.line_edit.setMaximumSize(1020, 30)

        if self.line_edit is None:
            self.line_edit.textChanged.connect(lambda what=None: self.check_existence(None))
        else:
            self.line_edit.textChanged.connect(lambda what=self.line_edit: self.check_existence(what.toPlainText()))

    def update_widget(self):
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

        # in update
        if self.line_edit is None:
            self.line_edit.textChanged.connect(lambda what=None: self.check_existence(None))
        else:
            self.line_edit.textChanged.connect(lambda what=self.line_edit: self.check_existence(what.toPlainText()))

    def create_table(self):
        # create the view
        tv = QTableView()

        # set the table model
        tablemodel = PandasTable(self.load_csv())
        tv.setModel(tablemodel)
        tv.setBaseSize(995, 800)
        # hide grid
        tv.setShowGrid(False)

        vh = tv.verticalHeader()
        vh.setVisible(True)

        # set horizontal header properties
        hh = tv.horizontalHeader()
        hh.setStretchLastSection(True)

        # set column width to fit contents
        # tv.resizeColumnsToContents()

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
                    self.df.loc[self.df.CodiceProdotto == text, 'QtaNegozio'] = self.df.loc[
                                                                                    self.df.CodiceProdotto == text, 'QtaNegozio'] - 1
                    if int(self.df.loc[self.df.CodiceProdotto == text, 'QtaNegozio']) <= 0:
                        self.df.loc[self.df.CodiceProdotto == text, 'QtaNegozio'] = 0
                        '''attivare alert'''
                        QMessageBox.about(self, "ATTENZIONE", "prodotto " + text + " esaurito in negozio")

                    self.df.loc[self.df.CodiceProdotto == text, 'QtTotale'] = self.df.loc[
                                                                                  self.df.CodiceProdotto == text, 'QtTotale'] - 1
                    if int(self.df.loc[self.df.CodiceProdotto == text, 'QtTotale']) != (
                            int(self.df.loc[self.df.CodiceProdotto == text, 'QtaNegozio']) + int(
                            self.df.loc[self.df.CodiceProdotto == text, 'QtaMagazzino'])):
                        self.df.loc[self.df.CodiceProdotto == text, 'QtTotale'] = int(
                            self.df.loc[self.df.CodiceProdotto == text, 'QtaNegozio']) + int(
                            self.df.loc[self.df.CodiceProdotto == text, 'QtaMagazzino'])

                    pd.set_option('display.max_columns', None)
                    # #print(self.df)
                    self.df.to_csv(self.mac_file_path, index=False)
                    self.update_widget()
                else:
                    #print("codice prodotto da cambiare:", text)
                    pass

    def load_csv(self):
        try:
            df = pd.read_csv(self.mac_file_path)
            #print(df)
            return df
        except FileNotFoundError as e:
            df = self.create_db()
            return df

    def create_db(self):
        if not os.path.isfile(self.mac_file_path):
            index_list = ["CodiceProdotto", "Nome", "Descrizione", "QtTotale", "QtaMagazzino", "QtaNegozio", "Taglia",
                          "Colore", "Hex", "Data"]
            df = pd.DataFrame(columns=index_list)
            df.to_csv(self.mac_file_path, index=False)
            #print("initialization dir:" + self.mac_file_path)
            return df
        else:
            #print("csv exists", self.mac_file_path)
            pass

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
            os.path.join(sys.executable + "/prodotti.csv", "..", '..', '..', "prodotti.csv"))

        self.pushButton = QPushButton("Inserisci", self)
        styles = """background-color: orange;
border-style: outset;
border-width: 2px;
border-radius: 15px;
border-color: #777777;
padding: 4px;
color: #777777;"""
        self.pushButton.setStyleSheet(styles)
        self.pushButton.move(160, 200)
        self.pushButton.setToolTip("<h3>Inserisci</h3>")
        self.pushButton.clicked.connect(self.window2)  # <===
        self.pushButton2 = QPushButton("Cerca", self)
        self.pushButton2.move(425, 200)
        self.pushButton2.setStyleSheet(styles)
        self.pushButton2.setToolTip("<h3>Cerca</h3>")

        self.pushButton2.clicked.connect(self.window3)  # <===

        self.create_db()
        self.main_window()

    def create_db(self):
        if not os.path.isfile(self.mac_file_path):
            index_list = ["CodiceProdotto", "Nome", "Descrizione", "QtTotale", "QtaMagazzino", "QtaNegozio", "Taglia",
                          "Colore", "Hex", "Data"]
            df = pd.DataFrame(columns=index_list)
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
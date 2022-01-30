import sqlite3
import sys
import os
sys.path.append(os.path.abspath(".."))
sys.path.append(f'{os.path.abspath("..")}\\venv')
sys.path.append(f'{os.path.abspath("..")}\\venv\\Scripts')
sys.path.append(f'{os.path.abspath("..")}\\venv\\Lib\\site-packages')


from PyQt6 import QtWidgets
import pandas as pd
import sys
from PyQt6 import QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import re

from moduls.position import Position
from src.moduls.sqlite import Sqlite
from src.moduls import tools

STYLE = """
                    QPushButton {font: bold 12px;}
                    QLabel {background-color: #ffffff;
                            border-radius: 5px;
                            font: bold 12px;}
                    QListWidget {font: bold 12px;}"""

class SetUpWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint| 
                            Qt.WindowType.WindowMinimizeButtonHint|
                            Qt.WindowType.WindowCloseButtonHint)

        self.db_log = 'sqlite.db'

        self.setStyleSheet(STYLE)



class Window(SetUpWindow):
    
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Przelicznik Wagowy')
        
        self.ui()
    
    def ui(self):

        # START layout_main
        self.layout_main = QVBoxLayout()
        self.layout_main.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout_main)

        self.tab = QTabWidget()
        # self.tab.setTabPosition(2)
        self.layout_main.addWidget(self.tab)

        self.widget_page_1 = QWidget()
        self.layout_page_1 = QVBoxLayout()
        self.layout_page_1.setContentsMargins(1,1,1,1)
        self.widget_page_1.setLayout(self.layout_page_1)
        self.tab.addTab(self.widget_page_1, 'Waga')
        ## START layout_up 
        self.layout_up = QHBoxLayout()
        self.layout_page_1.addLayout(self.layout_up)
        ### START layout_norm 
        self.layout_norm = QVBoxLayout()
        self.label_norm = QLabel('Norma') 
        self.label_norm.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_norm.addWidget(self.label_norm)
        self.list_w_norm = QListWidget()
        self.update_list_w_norm()
        self.list_w_norm.itemClicked.connect(self.update_list_w_size_1)
        self.list_w_norm.setMaximumSize(QSize(140,100))
        self.list_w_norm.setMinimumSize(QSize(140,100))
        self.layout_norm.addWidget(self.list_w_norm)
        self.layout_up.addLayout(self.layout_norm)
        ### END layout_norm
        ### START layout_size1 
        self.layout_size1 = QVBoxLayout()
        self.label_size_1 = QLabel('Wymiar 1')
        self.label_size_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_size1.addWidget(self.label_size_1)
        self.list_w_size1 = QListWidget()
        self.list_w_size1.itemClicked.connect(self.update_list_w_size_2)
        self.list_w_size1.setMaximumSize(QSize(80,100))
        self.list_w_size1.setMinimumSize(QSize(80,100))
        self.layout_size1.addWidget(self.list_w_size1)
        self.layout_up.addLayout(self.layout_size1)
        ### END layout_size1
        ### START layout_size1 
        self.layout_size2 = QVBoxLayout()
        self.label_size_2 = QLabel('Wymiar 2')
        self.label_size_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_size2.addWidget(self.label_size_2)
        self.list_w_size2 = QListWidget()
        self.list_w_size2.itemClicked.connect(
            lambda: self.update_info_item(
                size2=self.list_w_size2.currentItem().text()))
        self.list_w_size2.setMaximumSize(QSize(80,100))
        self.list_w_size2.setMinimumSize(QSize(80,100))
        self.layout_size2.addWidget(self.list_w_size2)
        self.layout_up.addLayout(self.layout_size2)
        ### END layout_size1
        ## END layout_up
        ## START layout_down
        self.layout_down = QVBoxLayout()
        self.layout_page_1.addLayout(self.layout_down)
        ### START layout_quick_calc
        self.layout_quick_calc = QHBoxLayout()
        self.layout_down.addLayout(self.layout_quick_calc)
        self.layout_quick_calc.addWidget(QLabel('Waga 1000szt:'),Qt.AlignmentFlag.AlignCenter)
        self.line_w_quick_calc = QLineEdit()
        self.line_w_quick_calc.setMaximumWidth(100)
        self.layout_quick_calc.addWidget(self.line_w_quick_calc)
        self.btn_quik_calc = QPushButton('Szybki przelicznik')
        self.btn_quik_calc.clicked.connect(lambda:\
            self.update_info_from_quick_calc(\
                self.line_w_quick_calc.text()))
        self.layout_quick_calc.addWidget(self.btn_quik_calc)
        ### END layout_quick_calc
        ### START layout_info
        self.layout_info = QGridLayout()
        self.label_info_name = QLabel('')
        self.label_info_weight = QLabel('')
        self.label_info_100szt_to_kg = QLabel('')
        self.btn_info_100szt_to_kg = QPushButton('Kopiuj')
        self.btn_info_100szt_to_kg.setEnabled(False)
        self.btn_info_100szt_to_kg.clicked.connect(
            lambda: QApplication.clipboard().setText(
                self.label_info_100szt_to_kg.text().replace('.', ',')
            )
        )
        self.label_info_kg_to_100szt = QLabel('')
        self.btn_info_kg_to_100szt = QPushButton('Kopiuj')
        self.btn_info_kg_to_100szt.setEnabled(False)
        self.btn_info_kg_to_100szt.clicked.connect(
            lambda: QApplication.clipboard().setText(
                self.label_info_kg_to_100szt.text().replace('.', ',')
            )
        )
        self.layout_down.addLayout(self.layout_info)
        self.label_info_name_0 = QLabel('Pozycja: ')
        self.label_info_name_0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_info.addWidget(self.label_info_name_0, 0, 0)
        self.layout_info.addWidget(self.label_info_name, 0, 1, 1, 2)
        self.label_info_weight_0 = QLabel('Waga 1000szt: ')
        self.label_info_weight_0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_info.addWidget(self.label_info_weight_0, 1, 0)
        self.layout_info.addWidget(self.label_info_weight, 1, 1, 1, 2)
        self.label_info_100szt_to_kg_0 = QLabel('100szt -> kg: ')
        self.label_info_100szt_to_kg_0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_info.addWidget(self.label_info_100szt_to_kg_0, 2, 0)
        self.layout_info.addWidget(self.label_info_100szt_to_kg, 2, 1)
        self.layout_info.addWidget(self.btn_info_100szt_to_kg, 2, 2)
        self.label_info_kg_to_100szt_0 = QLabel('kg -> 100szt: ')
        self.label_info_kg_to_100szt_0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_info.addWidget(self.label_info_kg_to_100szt_0, 3, 0)
        self.layout_info.addWidget(self.label_info_kg_to_100szt, 3, 1)
        self.layout_info.addWidget(self.btn_info_kg_to_100szt, 3, 2)
        ### END layout_info
        ### START layout_conversion
        self.layout_converion = QGridLayout()
        self.layout_converion.setHorizontalSpacing(0)
        self.layout_converion.setContentsMargins(0,0,0,0)
        self.layout_down.addLayout(self.layout_converion)
        self.line_edit_100szt_kg_weight = QLineEdit()
        self.line_edit_100szt_kg_weight.setEnabled(False)
        self.line_edit_100szt_kg_weight.textEdited\
            .connect(lambda: self.weight_converter(
                'to_szt',
                self.line_edit_100szt_kg_weight.text()))
        self.line_edit_kg_100szt_weight = QLineEdit()
        self.line_edit_kg_100szt_weight.setEnabled(False)
        self.line_edit_kg_100szt_weight.textEdited\
            .connect(lambda: self.weight_converter(
                'to_kg',
                self.line_edit_kg_100szt_weight.text()))
        self.line_edit_100szt_kg_price = QLineEdit()
        self.line_edit_100szt_kg_price.textEdited\
            .connect(lambda: self.price_converter(
                'to_szt',
                self.line_edit_100szt_kg_price.text()))
        self.line_edit_100szt_kg_price.setEnabled(False)
        self.line_edit_kg_100szt_price = QLineEdit()
        self.line_edit_kg_100szt_price.textEdited\
            .connect(lambda: self.price_converter(
                'to_kg',
                self.line_edit_kg_100szt_price.text()))
        self.line_edit_kg_100szt_price.setEnabled(False)
        self.layout_converion.addWidget(self.line_edit_100szt_kg_weight, 0, 0)
        self.layout_converion.addWidget(QLabel(' kg '), 0, 1)
        self.layout_converion.addWidget(QLabel(' = '), 0, 2)
        self.layout_converion.addWidget(self.line_edit_kg_100szt_weight, 0, 3)
        self.layout_converion.addWidget(QLabel(' sztuk '), 0, 4)
        self.layout_converion.addWidget(self.line_edit_100szt_kg_price, 1, 0)
        self.layout_converion.addWidget(QLabel(' zł/kg '), 1, 1)
        self.layout_converion.addWidget(QLabel(' = '), 1, 2)
        self.layout_converion.addWidget(self.line_edit_kg_100szt_price, 1, 3)
        self.layout_converion.addWidget(QLabel(' zł/100szt '), 1, 4)
        ### END layout_conversion
        ### START layout_buttons


        # self.layout_buttons = QHBoxLayout()
        # self.layout_down.addLayout(self.layout_buttons)
        # self.btn_add_new_position = QPushButton('Dodaj pozycje')
        # self.btn_update_position = QPushButton('Popraw pozycje')
        # self.btn_update_position.setDisabled(True)
        # self.btn_delete_position = QPushButton('Usuń pozycje')
        # self.layout_buttons.addWidget(self.btn_add_new_position)
        # self.layout_buttons.addWidget(self.btn_update_position)
        # self.layout_buttons.addWidget(self.btn_delete_position)
        # self.btn_add_new_position.clicked.connect(self.btn_add_new_position_func)
        # self.btn_update_position.clicked.connect(self.btn_update_position_func)
        # self.btn_delete_position.clicked.connect(self.btn_delete_position_func)


        ### END layout_buttons
        ## END layout_down
        # END layout_main

        self.widget_page_3 = QWidget()
        self.layout_page_3 = QVBoxLayout()
        self.widget_page_3.setLayout(self.layout_page_3)
        self.tab.addTab(self.widget_page_3, 'DIN/ISO/PN')

        self.show()
        # turn off resizing
        self.setMaximumSize(self.width(), self.height())
        self.setMinimumSize(self.width(), self.height())

    def update_list_w_norm(self):
        with Sqlite() as sql:
            result = sql.query_to_list(
                    """
                    SELECT DISTINCT waga_Norma
                    FROM waga
                    """)
        result = tools.quick_sort(result, type='str')
        self.list_w_norm.clear()
        self.list_w_norm.addItems([item for item in result])
        

    def update_list_w_size_1(self):
        self.actual = Position(norm=self.list_w_norm.currentItem().text())
        with Sqlite() as sql:
            result = sql.query_to_list(
                    f"""
                    SELECT DISTINCT waga_Rozmiar1
                    FROM waga
                    WHERE waga_Norma = '{self.actual.norm}'
                    """)
        result = tools.quick_sort(result, type='number')
        self.list_w_size1.clear()
        self.list_w_size2.clear()
        self.list_w_size1.addItems([str(item) for item in result])

    def update_list_w_size_2(self):
        self.actual.size1 = self.list_w_size1.currentItem().text()
        with Sqlite() as sql:
            results = sql.query_to_list(
                f"""SELECT DISTINCT waga_Rozmiar2
                    FROM waga
                    WHERE
                        waga_Norma = '{self.list_w_norm.currentItem().text()}'
                        AND waga_Rozmiar1 = {self.actual.size1}
                """)
        self.list_w_size2.clear()
        results = tools.quick_sort(results, type='number')
        results = [str(item) for item in results]
        if results[0] == 'None' and len(results) == 1: 
            self.update_info_item()
        elif results[0] == 'None' and len(results) > 1:
            del results[0]
            self.list_w_size2.addItems(results)
            self.update_info_item(size2='')
        else:
            self.list_w_size2.addItems(results)
            
    def update_info_item(self, size2=None):
        self.line_w_quick_calc.clear()
        if size2 is not None:
            self.actual.size2 = size2
        self.label_info_name.setText(self.actual.full_name)
        self.actual.weight = self.weight_query()
        self.label_info_weight.setText(self.actual.weight_kg_per_1000szt)
        self.label_info_100szt_to_kg.setText(f'{self.actual.calc_100szt_to_kg:.3f}')
        self.label_info_kg_to_100szt.setText(f'{self.actual.calc_kg_to_100szt:.3f}')
        self.enable_info()

    def enable_info(self):
        # self.btn_update_position.setEnabled(True)
        self.line_edit_100szt_kg_weight.setEnabled(True)
        self.line_edit_kg_100szt_weight.setEnabled(True)
        self.line_edit_100szt_kg_price.setEnabled(True)
        self.line_edit_kg_100szt_price.setEnabled(True)
        self.btn_info_100szt_to_kg.setEnabled(True)
        self.btn_info_kg_to_100szt.setEnabled(True)
        self.line_edit_100szt_kg_weight.clear()
        self.line_edit_kg_100szt_weight.clear()
        self.line_edit_100szt_kg_price.clear()
        self.line_edit_kg_100szt_price.clear()

    def update_info_from_quick_calc(self, string):
        try:
            self.list_w_size2.clear()
            self.list_w_size1.clear()
            convert = tools.str_to_number(string)
            self.actual = Position(weight=convert)
            self.enable_info()
            self.label_info_name.setText(self.actual.full_name)
            self.label_info_weight.setText(self.actual.weight_kg_per_1000szt)
            self.label_info_100szt_to_kg.setText(f'{self.actual.calc_100szt_to_kg:.3f}')
            self.label_info_kg_to_100szt.setText(f'{self.actual.calc_kg_to_100szt:.3f}')
        except Exception as e:
            print(e)

    def weight_converter(self, widget: str, string: str):
        try:
            convert = tools.str_to_number(string)
            if widget == 'to_kg':
                self.line_edit_100szt_kg_weight.setText(
                    str(f'{(convert / self.actual.calc_100szt_to_kg / 100):.3f}')
                )
            if widget == 'to_szt':
                self.line_edit_kg_100szt_weight.setText(
                    str(f'{int(convert / self.actual.calc_kg_to_100szt * 100)}')
                )
        except Exception as e:
            print(e)
        
    def price_converter(self, widget: str, string: str):
        try:
            convert = tools.str_to_number(string)
            if widget == 'to_kg':
                self.line_edit_100szt_kg_price.setText(
                    str(f'{(convert * self.actual.calc_100szt_to_kg):.2f}')
                )   
            if widget == 'to_szt':
                self.line_edit_kg_100szt_price.setText(
                    str(f'{(convert * self.actual.calc_kg_to_100szt):.2f}')
                )
        except Exception as e:
            print(e)


    def weight_query(self) -> float:
        with Sqlite() as sql:
            if self.actual.size2 == '':
                size2 = 'is NULL'
            else:
                size2 = f" = {self.actual.size2}"
            results = sql.query_to_list(
                    f"""SELECT waga_Waga1000szt
                        FROM waga
                        WHERE
                            waga_Norma = '{self.actual.norm}'
                            AND waga_Rozmiar1 = {self.actual.size1}
                            AND waga_Rozmiar2 {size2}
                    """)
        return results[0]





    # def btn_add_new_position_func(self):
    #    self.add_window = WindowAddPosition()
    
    # def btn_update_position_func(self):
    #     self.update_window = WindowUpdatePosition(self.actual)

    # def btn_delete_position_func(self):
    #     text = (
    #         f"norma:\t {self.actual.norm}\n"
    #         f"rozmiar_1:\t {self.actual.size1}\n"
    #         f"rozmiar_2:\t {self.actual.size2}\n"
    #         f"waga1000szt:\t {self.actual.weight:.2f}")
    #     box  = MyMessageInfoBox('Informacja','Czy usunąć podaną pozycję?',text)
    #     results = box.exec()
    #     if results == QMessageBox.StandardButton.Yes:
    #         if self.actual.size2 == '':
    #             size2 = 'is NULL'
    #         else:
    #             size2 = f" = {self.actual.size2}"
    #         with Sqlite() as sql:
    #             # napisać Select gdy znajdzie jedno to wtedy po id usuwamt to jedno
    #             if sql.delete( f"""DELETE FROM waga 
    #                             WHERE
    #                                 waga_Norma = '{self.actual.norm}',
    #                                 AND waga_Rozmiar1 = '{self.actual.size1}',
    #                                 AND waga_Rozmiar2 {size2}""") is True:
    #                                 print('YYYYYYYE')

# class MyMessageInfoBox(QMessageBox):
    
#     def __init__(self, title, question, message):
#         super().__init__()
#         self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
#         self.setStyleSheet(STYLE)
#         self.setWindowTitle(title)
#         self.setText(question)
#         self.setInformativeText(message)
#         self.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
#         self.setDefaultButton(QMessageBox.StandardButton.Yes)
#         self.button(QMessageBox.StandardButton.Yes).setText('Tak')
#         self.button(QMessageBox.StandardButton.No).setText('Nie')

# class WindowPosition(SetUpWindow):

    
#     def __init__(self) -> None:
#         super().__init__()

#         self.ui()
#         self.show()


#     def ui(self):
#         self.layout_main = QFormLayout()
#         self.layout_main.setRowWrapPolicy(QFormLayout.RowWrapPolicy.DontWrapRows)
#         self.layout_main.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

#         self.btn_manual = QPushButton('Otwórz poradnik')
#         self.btn_manual.clicked.connect(self.btn_manual_func)
#         self.label_norm = QLabel('Norma/Nazwa')
#         self.line_edit_norm = QLineEdit()
#         self.line_edit_norm.setPlaceholderText('DIN933')
#         self.label_size1 = QLabel('Rozmiar 1')
#         self.line_edit_size1 = QLineEdit()
#         self.line_edit_size1.setPlaceholderText('10')
#         self.label_size2 = QLabel('Rozmiar 2')
#         self.line_edit_size2 = QLineEdit()
#         # self.line_edit_size2.setPlaceholderText('')
#         self.label_weight = QLabel('Waga 1000szt.')
#         self.line_edit_weight = QLineEdit()
#         self.line_edit_weight.setPlaceholderText('4573')
#         self.btn_accept = QPushButton('')
#         self.btn_accept.clicked.connect(self.btn_accept_func)
#         self.layout_main.addRow(self.btn_manual)
#         self.layout_main.addRow(self.label_norm, self.line_edit_norm)
#         self.layout_main.addRow(self.label_size1, self.line_edit_size1)
#         self.layout_main.addRow(self.label_size2, self.line_edit_size2)
#         self.layout_main.addRow(self.label_weight, self.line_edit_weight)
#         self.layout_main.addRow(self.btn_accept)
#         self.setLayout(self.layout_main)


#     def btn_manual_func(self):
#         pass

#     def btn_accept_func(self):
#         pass

#     def check_norm(self) -> bool:
#         norm = self.line_edit_norm.text()
#         if (norm != '') and (' ' not in norm):
#             return True
#         else:
#             return False

#     def check_size1(self) -> bool:
#         size1 = self.line_edit_size1.text()
#         if (size1 != '') and (re.search('[0-9,.]', size1)) and (' ' not in size1):
#             return True
#         else:
#             return False

#     def check_size2(self) -> bool:
#         size2 = self.line_edit_size2.text()
#         if size2 == '':
#             return True
#         elif (size2 != '') and (re.search('[0-9]', size2)) and (' ' not in size2):
#             return True
#         else:
#             return False

#     def check_weight(self) -> bool:
#         weight = self.line_edit_weight.text()
#         if (weight != '') and (re.search('[0-9,.]', weight)) and (' ' not in weight):
#             return True
#         else:
#             return False

#     def check_all(self):
#         if (self.check_norm() is True) and (self.check_size1() is True) and (self.check_size2() is True) and (self.check_weight() is True):
#             return True
#         else:
#             return False

# class WindowAddPosition(WindowPosition):
#     def __init__(self) -> None:
#         super().__init__()
#         self.btn_accept.setText('Dodaj')

#         # self.position = Position()

#     def btn_accept_func(self):
#         if self.check_all() is True:
#             # if self.line_edit_size2.text() != '':
#             position = Position(norm=self.line_edit_norm.text(),
#                                 size1=self.line_edit_size1.text(),
#                                 size2=self.line_edit_size2.text(),
#                                 weight=self.line_edit_weight.text())
#             if self.line_edit_size2.text() == '':
#                 position.size2 = 'NULL'    
#                 # position = Position(norm=self.line_edit_norm.text(),
#                 #                     size1=self.line_edit_size1.text(),
#                 #                     size2='NULL',
#                 #                     weight=self.line_edit_weight.text())

#             with Sqlite(self.db_log) as sql:
#                 if sql.insert(f"""
#                     INSERT INTO waga (waga_Norma, waga_Rozmiar1, waga_Rozmiar2, waga_Waga1000szt)
#                     VALUES ('{position.norm}', {position.size1}, {position.size2}, {position.weight})
#                     """) is True:
#                     message = QMessageBox.information(self, 'Wynik operacji', 'udało się dodać pozycje')
#             print(position)

# class WindowUpdatePosition(WindowPosition):
#     def __init__(self, position) -> None:
#         super().__init__()
#         self.position = position
#         print(self.position)
#         self.btn_accept.setText('Popraw')
#         print(self.position.norm)
#         self.line_edit_norm.setText(self.position.norm)
#         print(self.line_edit_norm.text())
#         self.line_edit_size1.setText(self.position.size1)
#         self.line_edit_size2.setText(self.position.size2)
#         self.line_edit_weight.setText(str(self.position.weight))

#     def btn_accept_func(self):
#         if self.check_all() is True:
#             self.position.norm = self.line_edit_norm.text(),
#             self.position.size1 = self.line_edit_size1.text(),
#             self.position.size2 = self.line_edit_size2.text(),
#             self.position.weight = self.line_edit_weight.text()
#             if self.line_edit_size2.text() == '':
#                 self.position.size2 = 'NULL'    
#         print(self.position)

# class Position:

#     def __init__(self, norm: str='', size1: str='', size2: str='', weight: float=0) -> None:
#         self.norm = norm
#         self.size1 = size1
#         self.size2 = size2
#         self.weight = weight
    
#     @property
#     def norm(self):
#         return self.__norm

#     @norm.setter
#     def norm(self, norm):
#         if isinstance(norm, tuple):
#             norm = norm[0]
#         self.__norm = norm

#     @norm.deleter
#     def norm(self):
#         self.norm = ''

#     @property
#     def size1(self):
#         return self.__size1
    
#     @size1.setter
#     def size1(self, size1):
#         if isinstance(size1, tuple):
#             size1 = size1[0]
#         self.__size1 = size1

#     @size1.deleter
#     def size1(self):
#         self.size1 = ''

#     @property
#     def size2(self):
#         return self.__size2
    
#     @size2.setter
#     def size2(self, size2):
#         if isinstance(size2, tuple):
#             size2 = size2[0]
#         # if size2 == '':
#         #     self.__size2 = 'NULL'
#         self.__size2 = size2

#     @size2.deleter
#     def size2(self):
#         self.size2 = ''

#     @property
#     def weight(self):
#         return self.__weight
    
#     @weight.setter
#     def weight(self, weight):
#         # if ',' in weight:
#         #     weight = weight.replace(',', '.')
#         weight  = float(weight)
#         if weight > 0:
#             self.__weight = weight
#         else:
#             self.__weight = 0

#     @property
#     def full_name(self):
#         if self.__size2 == '':
#             return f'{self.__norm}  {self.__size1}'
#         else:
#             return f'{self.__norm}  {self.__size1}x{self.__size2}'
    
#     @property
#     def calc_kg_to_100szt(self):
#         val = self.__weight * (100/1000)
#         return val

#     @property
#     def calc_100szt_to_kg(self):
#         val = (1000/100) * (1/self.__weight)
#         return val
    
#     @property
#     def weight_kg_per_1000szt(self):
#         return str(self.__weight) + ' kg/1000szt.'

#     def __repr__(self) -> str:
#         str_repl =  f"""norm: {self.norm}
#                         size 1: {self.size1}
#                         size 2: {self.size2}
#                         weight: {self.weight}
#                         kg_to_100szt: {self.calc_kg_to_100szt}
#                         100szt_to_kg: {self.calc_100szt_to_kg}"""
#         return str_repl

            

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Window()
    sys.exit(app.exec())

if __name__ == '__main__':
        main()
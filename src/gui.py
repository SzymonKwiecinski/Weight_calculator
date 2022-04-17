from asyncio.windows_events import NULL
import sys
import os
import re
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QTabWidget
from PyQt6.QtWidgets import QLabel, QPushButton, QListWidget, QLineEdit, QGridLayout, QComboBox, QFormLayout
from PyQt6.QtCore import Qt, QSize
from src.position import Position
from src.sqlite import Sqlite
# from src.norm import Norm
from src import tools

STYLE = """
    QPushButton {font: bold 12px;}
    QLabel {background-color: #e0e0e0;
            border-radius: 5px;
            font: bold 12px;}
    QListWidget {font: bold 12px;}"""


class SetUpWindow(QWidget):
    """Class parent for all my windows.

    Set style configuration in order to
    contain the same layout everywhere.
    """

    def __init__(self) -> None:
        super().__init__()

        self.setWindowFlags(Qt.WindowType.WindowMinimizeButtonHint
                            | Qt.WindowType.WindowCloseButtonHint)

        self.db_log = 'sqlite.db'

        self.setStyleSheet(STYLE)


class Window(SetUpWindow):
    """Main gui widnows class."""
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Przelicznik Wagowy')
        # self.files_norm = Norm()
        self.ui()

    def ui(self):
        self.layout_main = QVBoxLayout()
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout_main)
        # START button activate always top
        self.btn_stay_on_top = QPushButton('Zatrzymaj zawsze widoczny')
        self.layout_main.addWidget(self.btn_stay_on_top)
        self.btn_stay_on_top.clicked.connect(self.change_state_of_window)
        # END button activate always top
        self.tab = QTabWidget()
        self.layout_main.addWidget(self.tab)
        # START page1
        self.widget_page_1 = QWidget()
        self.layout_page_1 = QVBoxLayout()
        self.layout_page_1.setContentsMargins(1, 1, 1, 1)
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
        self.list_w_norm.setMaximumSize(QSize(140, 100))
        self.list_w_norm.setMinimumSize(QSize(140, 100))
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
        self.list_w_size1.setMaximumSize(QSize(80, 100))
        self.list_w_size1.setMinimumSize(QSize(80, 100))
        self.layout_size1.addWidget(self.list_w_size1)
        self.layout_up.addLayout(self.layout_size1)
        ### END layout_size1
        ### START layout_size2
        self.layout_size2 = QVBoxLayout()
        self.label_size_2 = QLabel('Wymiar 2')
        self.label_size_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_size2.addWidget(self.label_size_2)
        self.list_w_size2 = QListWidget()
        self.list_w_size2.itemClicked.connect(
            lambda: self.update_info_item(
                size2=self.list_w_size2.currentItem().text()))
        self.list_w_size2.setMaximumSize(QSize(80, 100))
        self.list_w_size2.setMinimumSize(QSize(80, 100))
        self.layout_size2.addWidget(self.list_w_size2)
        self.layout_up.addLayout(self.layout_size2)
        ### END layout_size2
        ## END layout_up
        ## START layout_down
        self.layout_down = QVBoxLayout()
        self.layout_page_1.addLayout(self.layout_down)
        ### START layout_quick_calc
        self.layout_quick_calc = QHBoxLayout()
        self.layout_down.addLayout(self.layout_quick_calc)
        self.layout_quick_calc.addWidget(
            QLabel('Waga 1000szt:', alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        )
        self.line_w_quick_calc = QLineEdit()
        self.line_w_quick_calc.setMaximumWidth(100)
        self.layout_quick_calc.addWidget(self.line_w_quick_calc)
        self.btn_quik_calc = QPushButton('Szybki przelicznik')
        self.btn_quik_calc.clicked.connect(
            lambda: self.update_info_from_quick_calc(
                self.line_w_quick_calc.text()
            )
        )
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
        self.label_info_name_0.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        self.layout_info.addWidget(self.label_info_name_0, 0, 0)
        self.layout_info.addWidget(self.label_info_name, 0, 1, 1, 2)
        self.label_info_weight_0 = QLabel('Waga 1000szt: ')
        self.label_info_weight_0.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        self.layout_info.addWidget(self.label_info_weight_0, 1, 0)
        self.layout_info.addWidget(self.label_info_weight, 1, 1, 1, 2)
        self.label_info_100szt_to_kg_0 = QLabel('100szt -> kg: ')
        self.label_info_100szt_to_kg_0.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        self.layout_info.addWidget(self.label_info_100szt_to_kg_0, 2, 0)
        self.layout_info.addWidget(self.label_info_100szt_to_kg, 2, 1)
        self.layout_info.addWidget(self.btn_info_100szt_to_kg, 2, 2)
        self.label_info_kg_to_100szt_0 = QLabel('kg -> 100szt: ')
        self.label_info_kg_to_100szt_0.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        self.layout_info.addWidget(self.label_info_kg_to_100szt_0, 3, 0)
        self.layout_info.addWidget(self.label_info_kg_to_100szt, 3, 1)
        self.layout_info.addWidget(self.btn_info_kg_to_100szt, 3, 2)
        ### END layout_info
        ### START layout_conversion
        self.layout_converion = QGridLayout()
        self.layout_converion.setHorizontalSpacing(0)
        self.layout_converion.setContentsMargins(0, 0, 0, 0)
        self.layout_down.addLayout(self.layout_converion)
        self.line_edit_kg_weight = QLineEdit()
        self.line_edit_kg_weight.setEnabled(False)
        self.line_edit_kg_weight.textEdited\
            .connect(lambda: self.weight_converter(
                'to_szt',
                self.line_edit_kg_weight.text()))
        self.line_edit_szt_weight = QLineEdit()
        self.line_edit_szt_weight.setEnabled(False)
        self.line_edit_szt_weight.textEdited\
            .connect(lambda: self.weight_converter(
                'to_kg',
                self.line_edit_szt_weight.text()))
        self.line_edit_kg_price = QLineEdit()
        self.line_edit_kg_price.textEdited\
            .connect(lambda: self.price_converter(
                'to_szt',
                self.line_edit_kg_price.text()))
        self.line_edit_kg_price.setEnabled(False)
        self.line_edit_100szt_price = QLineEdit()
        self.line_edit_100szt_price.textEdited\
            .connect(lambda: self.price_converter(
                'to_kg',
                self.line_edit_100szt_price.text()))
        self.line_edit_100szt_price.setEnabled(False)
        self.layout_converion.addWidget(self.line_edit_kg_weight, 0, 0)
        self.layout_converion.addWidget(QLabel(' kg '), 0, 1)
        self.layout_converion.addWidget(QLabel(' = '), 0, 2)
        self.layout_converion.addWidget(self.line_edit_szt_weight, 0, 3)
        self.layout_converion.addWidget(QLabel(' sztuk '), 0, 4)
        self.layout_converion.addWidget(self.line_edit_kg_price, 1, 0)
        self.layout_converion.addWidget(QLabel(' zł/kg '), 1, 1)
        self.layout_converion.addWidget(QLabel(' = '), 1, 2)
        self.layout_converion.addWidget(self.line_edit_100szt_price, 1, 3)
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
        # END page1

        # START page2
        self.widget_page_2 = QWidget()
        self.layout_page_2 = QFormLayout()
        self.widget_page_2.setLayout(self.layout_page_2)
        self.tab.addTab(self.widget_page_2, 'DIN/ISO/PN')
        self.label_1_p2 = QLabel('Nazwa długa normy')
        self.label_1_p2.setWordWrap(True)
        self.label_din_p2 = QLabel('DIN ')
        self.label_pn_p2 = QLabel('PN  ')
        self.label_iso_p2 = QLabel('ISO ')
        self.label_other_p2 = QLabel('INNE')
        self.combo_box_din_p2 = QComboBox()
        self.combo_box_din_p2.textActivated.connect(self.combo_box_func_p2)
        self.combo_box_iso_p2 = QComboBox()
        self.combo_box_iso_p2.textActivated.connect(self.combo_box_func_p2)
        self.combo_box_pn_p2 = QComboBox()
        self.combo_box_pn_p2.textActivated.connect(self.combo_box_func_p2)
        self.combo_box_other_p2 = QComboBox()
        self.combo_box_other_p2.textActivated.connect(self.combo_box_func_p2)
        
        self.btn_norma_p2 = QPushButton('Otwórz katalog/normę')
        self.btn_norma_p2.clicked.connect(self.open_norm_file_p2)
        self.btn_norma_p2.setDisabled(True)
        self.populate_norm_list()

        self.layout_page_2.addRow(self.label_1_p2)
        self.layout_page_2.addRow(self.label_din_p2, self.combo_box_din_p2)
        self.layout_page_2.addRow(self.label_iso_p2, self.combo_box_iso_p2)
        self.layout_page_2.addRow(self.label_pn_p2, self.combo_box_pn_p2)
        self.layout_page_2.addRow(self.label_other_p2, self.combo_box_other_p2)
        self.layout_page_2.addRow(self.btn_norma_p2)

        # END page2

        self.show()
        # turn off resizing
        self.setMaximumSize(self.width(), self.height())
        self.setMinimumSize(self.width(), self.height())

    def update_list_w_norm(self) -> None:
        """Fills first WidgetList.

        Execute query with products norm.
        e.g DIN123 ..."""

        with Sqlite() as sql:
            result = sql.query_to_list(
                """
                SELECT DISTINCT waga_Norma
                FROM waga
                """)
        result = tools.quick_sort(result, type='str')
        self.list_w_norm.clear()
        self.list_w_norm.addItems([item for item in result])

    def update_list_w_size_1(self) -> None:
        """Fills second ListWidgets."""
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

    def update_list_w_size_2(self) -> None:
        """Fills third WidgetList.

        If positions have only one size then
        fill info about it and allows."""

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

    def update_info_item(self, size2=None) -> None:
        """Manages display info about a position."""
        self.line_w_quick_calc.clear()
        if size2 is not None:
            self.actual.size2 = size2
        self.label_info_name.setText(self.actual.full_name)
        self.actual.weight = self.weight_query()
        self.label_info_weight.setText(self.actual.weight_kg_per_1000szt)
        self.label_info_100szt_to_kg.setText(f'{self.actual.calc_100szt_to_kg:.3f}')
        self.label_info_kg_to_100szt.setText(f'{self.actual.calc_kg_to_100szt:.3f}')
        self.enable_info()

    def enable_info(self) -> None:
        """Activates calculation options for a position."""
        # self.btn_update_position.setEnabled(True)
        self.line_edit_kg_weight.setEnabled(True)
        self.line_edit_szt_weight.setEnabled(True)
        self.line_edit_kg_price.setEnabled(True)
        self.line_edit_100szt_price.setEnabled(True)
        self.btn_info_100szt_to_kg.setEnabled(True)
        self.btn_info_kg_to_100szt.setEnabled(True)
        self.line_edit_kg_weight.clear()
        self.line_edit_szt_weight.clear()
        self.line_edit_kg_price.clear()
        self.line_edit_100szt_price.clear()

    def update_info_from_quick_calc(self, string: str) -> None:
        """Manages behavior for quick_calc option."""
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

    def weight_converter(self, widget: str, string: str) -> None:
        """Handle event for weight conversion.

        Args:
            widget: indicate direction of convertion
                allows(to_kg, to_szt)
            string: value to confert in string format

        Raises:
            TypeError: If wrong widget variable

        """

        if widget not in ['to_kg', 'to_szt']:
            raise TypeError
        try:
            convert = tools.str_to_number(string)
            if widget == 'to_kg':
                self.line_edit_kg_weight.setText(
                    self.actual.convert_weight_from_szt_to_kg(szt=convert)
                )
            if widget == 'to_szt':
                self.line_edit_szt_weight.setText(
                    self.actual.convert_weight_from_kg_to_szt(kg=convert)
                )
        except Exception as e:
            print(e)

    def price_converter(self, widget: str, string: str):
        """Handle event for price conversion.

        Args:
            widget: indicate direction of convertion
                allows(to_kg, to_szt)
            string: value to confert in string format

        Raises:
            TypeError: If wrong widget variable

        """

        if widget not in ['to_kg', 'to_szt']:
            raise TypeError
        try:
            convert = tools.str_to_number(string)
            if widget == 'to_kg':
                self.line_edit_kg_price.setText(
                    self.actual.convert_price_from_100szt_to_kg(szt100=convert)
                )
            if widget == 'to_szt':
                self.line_edit_100szt_price.setText(
                    self.actual.convert_price_from_kg_to_100szt(kg=convert)
                )
        except Exception as e:
            print(e)

    def weight_query(self) -> float:
        """Quary database about weight of the position."""
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

    def change_state_of_window(self) -> None:
        """Changes visibility of window.

        Allows either set window to be always on top or not
        """

        if self.btn_stay_on_top.text() == 'Schowaj kalkulator':
            self.btn_stay_on_top.setText('Zatrzymaj zawsze widoczny')
            self.setWindowFlags(
                Qt.WindowType.WindowCloseButtonHint
                | Qt.WindowType.WindowMinimizeButtonHint
                | Qt.WindowType.WindowSystemMenuHint
                | Qt.WindowType.WindowTitleHint
                | Qt.WindowType.Window
            )
            self.show()
        elif self.btn_stay_on_top.text() == 'Zatrzymaj zawsze widoczny':
            self.btn_stay_on_top.setText('Schowaj kalkulator')
            self.setWindowFlags(
                Qt.WindowType.WindowCloseButtonHint
                | Qt.WindowType.WindowStaysOnTopHint
                | Qt.WindowType.WindowMinimizeButtonHint
                | Qt.WindowType.WindowSystemMenuHint
                | Qt.WindowType.WindowTitleHint
                | Qt.WindowType.Window
            )
            self.show()

    def populate_norm_list(self):
        """Populate all norm fields"""
        norms = {
            'din': ['normy_Din', self.combo_box_din_p2],
            'pn': ['normy_Pn', self.combo_box_pn_p2],
            'iso': ['normy_Iso', self.combo_box_iso_p2]
            # 'other': ['', self.combo_box_other_p2]
        }
        with Sqlite() as sql:
            for norm in norms.values():
                results = sql.query_to_list(
                    f"""SELECT
                            DISTINCT {norm[0]}
                        FROM normy
                        WHERE
                            {norm[0]} is not NULL
                            AND {norm[0]} <> ''
                    """
                )
                results = tools.quick_sort(results, type='str')
                norm[1].addItem('')
                norm[1].addItems(results)

            results = sql.query_to_list(
                    f"""SELECT
                            DISTINCT normy_Nazwa
                        FROM normy
                        WHERE
                            (normy_Din is NULL OR normy_Din = '')
                            AND (normy_Iso is NULL OR normy_Iso = '')
                            AND (normy_Pn is NULL OR normy_Pn = '')
                    """
            )
            self.combo_box_other_p2.addItem('')
            self.combo_box_other_p2.addItems(results)

        

    def combo_box_func_p2(self, selected):
        if selected != '':
            if re.search('DIN', selected, re.RegexFlag.I):
                results = self.select_one_row(selected, 'Din')
                self.combo_box_iso_p2.setCurrentText(results[0][2])
                self.combo_box_pn_p2.setCurrentText(results[0][3])
                self.combo_box_other_p2.setCurrentText('')
                self.label_1_p2.setText(results[0][0])
                self.manage_norm_button_p2(results[0][4])
            elif re.search('PN', selected, re.RegexFlag.I):
                results = self.select_one_row(selected, 'Pn')
                self.combo_box_iso_p2.setCurrentText(results[0][2])
                self.combo_box_din_p2.setCurrentText(results[0][1])
                self.combo_box_other_p2.setCurrentText('')
                self.label_1_p2.setText(results[0][0])
                self.manage_norm_button_p2(results[0][4])
            elif re.search('ISO', selected, re.RegexFlag.I):
                results = self.select_one_row(selected, 'Iso')
                self.combo_box_din_p2.setCurrentText(results[0][1])
                self.combo_box_pn_p2.setCurrentText(results[0][3])
                self.combo_box_other_p2.setCurrentText('')
                self.label_1_p2.setText(results[0][0])
                self.manage_norm_button_p2(results[0][4])
            else:
                results = self.select_one_row(selected, 'Nazwa')
                self.combo_box_din_p2.setCurrentText('')
                self.combo_box_iso_p2.setCurrentText('')
                self.combo_box_pn_p2.setCurrentText('')
                self.label_1_p2.setText(results[0][0])
                self.manage_norm_button_p2(results[0][4])

    def manage_norm_button_p2(self, selected):
        if selected is not None and selected != '':
            self.file_norm_p2 = selected
            self.btn_norma_p2.setEnabled(True)
            self.btn_norma_p2.setText(selected)
        else:
            self.btn_norma_p2.setText('Brak rysunku w bazie danych')
            self.btn_norma_p2.setDisabled(True)

    def open_norm_file_p2(self):
        os.startfile(f'normy\{self.file_norm_p2}')

    def select_one_row(self, selected, column):
        with Sqlite() as sql:
            query = sql.query_all(
                f"""SELECT
                        normy_Nazwa,
                        normy_Din,
                        normy_Iso,
                        normy_Pn,
                        normy_Plik
                    FROM normy
                    WHERE normy_{column} = '{selected}'
                """
            )
        return query
    
    # def find_norm_file(self, ):
    #     pass

    # def btn_add_new_position_func(self):
    #    self.add_window = WindowAddPosition()
    #
    # def btn_update_position_func(self):
    #     self.update_window = WindowUpdatePosition(self.actual)
    #
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
#
# class MyMessageInfoBox(QMessageBox):
#
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
#
# class WindowPosition(SetUpWindow):
#
#
#     def __init__(self) -> None:
#         super().__init__()
#
#         self.ui()
#         self.show()
#
#
#     def ui(self):
#         self.layout_main = QFormLayout()
#         self.layout_main.setRowWrapPolicy(QFormLayout.RowWrapPolicy.DontWrapRows)
#         self.layout_main.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
#
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
#
#
#     def btn_manual_func(self):
#         pass
#
#     def btn_accept_func(self):
#         pass
#
#     def check_norm(self) -> bool:
#         norm = self.line_edit_norm.text()
#         if (norm != '') and (' ' not in norm):
#             return True
#         else:
#             return False
#
#     def check_size1(self) -> bool:
#         size1 = self.line_edit_size1.text()
#         if (size1 != '') and (re.search('[0-9,.]', size1)) and (' ' not in size1):
#             return True
#         else:
#             return False
#
#     def check_size2(self) -> bool:
#         size2 = self.line_edit_size2.text()
#         if size2 == '':
#             return True
#         elif (size2 != '') and (re.search('[0-9]', size2)) and (' ' not in size2):
#             return True
#         else:
#             return False
#
#     def check_weight(self) -> bool:
#         weight = self.line_edit_weight.text()
#         if (weight != '') and (re.search('[0-9,.]', weight)) and (' ' not in weight):
#             return True
#         else:
#             return False
#
#     def check_all(self):
#         if (self.check_norm() is True) and (self.check_size1() is True)
#            and (self.check_size2() is True) and (self.check_weight() is True):
#             return True
#         else:
#             return False
#
# class WindowAddPosition(WindowPosition):
#     def __init__(self) -> None:
#         super().__init__()
#         self.btn_accept.setText('Dodaj')
#
#         # self.position = Position()
#
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
#
#             with Sqlite(self.db_log) as sql:
#                 if sql.insert(f"""
#                     INSERT INTO waga (waga_Norma, waga_Rozmiar1, waga_Rozmiar2, waga_Waga1000szt)
#                     VALUES ('{position.norm}', {position.size1}, {position.size2}, {position.weight})
#                     """) is True:
#                     message = QMessageBox.information(self, 'Wynik operacji', 'udało się dodać pozycje')
#             print(position)
#
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
#
#     def btn_accept_func(self):
#         if self.check_all() is True:
#             self.position.norm = self.line_edit_norm.text(),
#             self.position.size1 = self.line_edit_size1.text(),
#             self.position.size2 = self.line_edit_size2.text(),
#             self.position.weight = self.line_edit_weight.text()
#             if self.line_edit_size2.text() == '':
#                 self.position.size2 = 'NULL'
#         print(self.position)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    Window()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

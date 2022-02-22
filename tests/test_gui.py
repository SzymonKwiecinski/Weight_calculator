from src.gui import *
from pytest import mark


@mark.gui
def test_gui():
    try:
        app = QApplication(sys.argv)
        Window()
        assert True
    except Exception as e:
        assert False, e

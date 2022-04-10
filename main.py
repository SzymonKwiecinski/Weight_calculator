import os
import sys
sys.path.insert(0, os.path.abspath("."))
sys.path.insert(1, f'{os.path.abspath(".")}\\venv')
sys.path.insert(2, f'{os.path.abspath(".")}\\venv\\Scripts')
sys.path.insert(3, f'{os.path.abspath(".")}\\venv\\Lib\\site-packages')
from src.gui import main

if __name__ == '__main__':
    main()

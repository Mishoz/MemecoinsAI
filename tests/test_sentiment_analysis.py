import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from sentiment_analysis import main

def test_main():
    main()

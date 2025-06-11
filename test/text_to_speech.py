# add /Users/azakaria/Code/fluent/app.py to python path
import sys
sys.path.append('/Users/azakaria/Code/fluent')

from app import text_to_speech

text_to_speech("Hello, how are you?", "en")
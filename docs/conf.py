import os
import sys
import django

sys.path.insert(0, os.path.abspath('../'))  # or adjust path to your project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takealot.settings')
django.setup()

project = 'Take_alot_new'
author = 'Simphiwe Nhlabati'
release = '0.1'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]
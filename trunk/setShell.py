import sys
import os

sys.path.append("c:\\projekti")
sys.path.append("c:\\projekti\\prviDjango")
sys.path.append("d:\\projekti")
sys.path.append("d:\\projekti\\prviDjango")

os.environ['DJANGO_SETTINGS_MODULE']='prviDjango.settings'

import django
import prviDjango
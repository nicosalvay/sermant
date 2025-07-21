import os
import sys
path = '/var/www/ascensores'
if path not in sys.path:
    sys.path.append(path)
os.environ["DJANGO_SETTINGS_MODULE"]="ascensores.settings"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


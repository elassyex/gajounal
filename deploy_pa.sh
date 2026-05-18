#!/bin/bash
set -e

cd ~
echo "=== 1/8: Clone repo ==="
git clone https://github.com/elassyex/gajounal.git

echo "=== 2/8: Create virtualenv ==="
python3.12 -m venv /home/asy123/.virtualenvs/gajounal

echo "=== 3/8: Install dependencies ==="
source /home/asy123/.virtualenvs/gajounal/bin/activate
cd ~/gajounal
pip install -r requirements.txt

echo "=== 3.5/8: Create .env for PA ==="
cat > ~/gajounal/mysite/settings/.env << 'ENVEOF'
CSRF_TRUSTED_ORIGINS=https://asy123.pythonanywhere.com
ENVEOF

echo "=== 4/8: Write WSGI file ==="
cat > /var/www/asy123_pythonanywhere_com_wsgi.py << 'EOF'
import os
import sys
path = '/home/asy123/gajounal'
if path not in sys.path:
    sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings.dev'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
EOF

echo "=== 5/8: Migrate ==="
python manage.py migrate

echo "=== 6/8: Load demo data ==="
python manage.py loaddata database.json

echo "=== 7/8: Collect static ==="
python manage.py collectstatic --noinput

echo "=== Almost done! ==="
echo ""
echo "One last step - go to the Web tab:"
echo "  https://www.pythonanywhere.com/user/asy123/webapps/asy123.pythonanywhere.com/"
echo "and set:"
echo "  Virtualenv: /home/asy123/.virtualenvs/gajounal"
echo "Then click Reload."
echo ""
echo "Site: https://asy123.pythonanywhere.com"
echo "Admin: https://asy123.pythonanywhere.com/admin/ (user: admin, pass: admin)"

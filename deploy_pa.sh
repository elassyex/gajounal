#!/bin/bash
set -e

cd ~
echo "=== 1/8: Clone repo ==="
git clone https://github.com/elassyex/gajounal.git

echo "=== 2/8: Create virtualenv ==="
mkvirtualenv gajounal --python=python3.12

echo "=== 3/8: Install dependencies ==="
cd ~/gajounal
pip install -r requirements.txt

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

echo "=== 8/8: Set virtualenv & reload ==="
cd ~/gajounal
pa webapp set-webapp asy123.pythonanywhere.com virtualenv /home/asy123/.virtualenvs/gajounal
pa webapp reload asy123.pythonanywhere.com

echo "=== Done! ==="
echo "Site: https://asy123.pythonanywhere.com"
echo "Admin: https://asy123.pythonanywhere.com/admin/ (user: admin, pass: admin)"

#!/usr/bin/env bash
PUBLIC=${1?Error: No Public IP given}

cd ..
git pull 
path_to_settings="Django-Books/Login/settings.py"
PUBLIC_="['${PUBLIC}']" 
False=False

sed -i "s/\("DEBUG" *= *\).*/\1$False/" $path_to_settings
sed -i "s/\("ALLOWED_HOSTS" *= *\).*/\1$PUBLIC_/" $path_to_settings
echo "STATIC_ROOT = os.path.join(BASE_DIR, 'static/')" >> $path_to_settings

sudo source venv/bin/activate
sudo python3 Django-Books/manage.py migrate
sudo python3 Django-Books/manage.py collectstatic --noinput
sudo systemctl daemon-reload
sudo systemctl enable nginx
sudo service nginx restart
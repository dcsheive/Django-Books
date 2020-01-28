#!/usr/bin/env bash
PUBLIC=${1?Error: No Public IP given}
echo ${PUBLIC}

cd ..

sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get --assume-yes install nginx
sudo apt-get --assume-yes install python3
sudo apt-get --assume-yes install -y python3-pip
sudo apt-get --assume-yes install python3-venv

path_to_settings="Django-Books/Login/settings.py"
PUBLIC_="['${PUBLIC}']" 
False=False

sed -i "s/\("DEBUG" *= *\).*/\1$False/" $path_to_settings
sed -i "s/\("ALLOWED_HOSTS" *= *\).*/\1$PUBLIC_/" $path_to_settings
echo "STATIC_ROOT = os.path.join(BASE_DIR, 'static/')" >> $path_to_settings

sudo python3 -m venv venv
source ./venv/bin/activate
pip3 install -r Django-Books/requirements.txt
pip3 install gunicorn
python3 Django-Books/manage.py migrate
python3 Django-Books/manage.py collectstatic

echo "[Unit]
Description=gunicorn daemon
After=network.target
[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/Django-Books
ExecStart=/home/ubuntu/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/Django-Books/Login.sock Login.wsgi:application
[Install]
WantedBy=multi-user.target" > /etc/systemd/system/gunicorn.service

sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

sudo rm -rf /etc/nginx/sites-available/default
sudo rm -rf /etc/nginx/sites-enabled/default

echo "server {
  listen 80;
  server_name ${PUBLIC};
  location = /favicon.ico { access_log off; log_not_found off; }
  location /static/ {
      root /home/ubuntu/Django-Books;
  }
  location /media/ {
      root /home/ubuntu/Django-Books;
  }
  location / {
      include proxy_params;
      proxy_pass http://unix:/home/ubuntu/Django-Books/Login.sock;
  }
}" > /etc/nginx/sites-available/Login

sudo ln -s /etc/nginx/sites-available/Login /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl daemon-reload
sudo systemctl enable nginx
sudo service nginx restart

sudo rm -rf Django-Books/db.sqlite3
python3 Django-Books/manage.py migrate
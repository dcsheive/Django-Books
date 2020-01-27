#!/usr/bin/env bash
PUBLIC=${1?Error: No Public IP given}
PRIVATE=${2?Error: No Private IP given}
echo ${PUBLIC}
echo ${PRIVATE}

eval "apt-get install nginx"
eval "apt-get install python3"
eval "apt-get install -y python3-pip"
eval "apt-get install python3-venv"

path_to_settings = "Django-Books/Login/settings.py"
PUBLIC_="['${PUBLIC}']" 
False=False

sed -i "s/\("DEBUG" *= *\).*/\1$False/" $path_to_settings
sed -i "s/\("ALLOWED_HOSTS" *= *\).*/\1$PUBLIC_/" $path_to_settings
echo "STATIC_ROOT = os.path.join(BASE_DIR, 'static/')" >> $path_to_settings

eval "python3 -m venv venv"
eval "source venv/bin/activate"
eval "pip install -r requirements.txt"
eval "pip install gunicorn"
eval "python Django-Books/manage.py migrate"
eval "python Django-Books/manage.py collectstatic"

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

eval "rm -rf /etc/nginx/sites-available/default"
eval "rm -rf /etc/nginx/sites-enabled/default"

echo "server {
  listen 80;
  server_name ${PRIVATE};
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

eval "ln -s /etc/nginx/sites-available/Login /etc/nginx/sites-enabled/"
eval "nginx -t"
eval "systemctl daemon-reload"
eval "systemctl enable nginx"
eval "service nginx restart"
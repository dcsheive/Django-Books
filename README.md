# The Wall

# AWS EC2 Setup with Ubuntu

First ssh into your EC2 instance:


Run these commands:

git clone https://github.com/dcsheive/Django-Books.git

cd Django-Books


Then execute start.sh with EC2 Public IP:

sudo chmod +x start.sh

sudo ./start.sh <Public-IP>


When finished enter this command:

sudo chown ubuntu db.sqlite3


Update:

sudo chmod +x update.sh

sudo ./update.sh <Public-IP>

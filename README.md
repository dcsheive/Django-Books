# The Wall

ssh into your EC2 instance

Run these commands:

sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install git
git clone https://github.com/dcsheive/Django-Books.git


Then execute start.sh with EC2 Public and Private IPs:

sudo chmod +x start.sh
sudo ./start.sh <Public-IP> <Private-IP>

Update 
sudo chmod +x update.sh
sudo ./update.sh <Public-IP>

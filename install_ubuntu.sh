sudo apt update
git clone https://github.com/Galrin/hello11app.git
cd hello11app
#sudo apt install python3-venv # disable dialog prompt
#python3 -m venv venv
#chmod +x ./venv/bin/activate
sudo apt install -y mariadb-*

mysql -u root -q "SET PASSWORD FOR `root`@`localhost` = PASSWORD('1AaBbCc#')"

export DATABASE_PASSWORD="1ABbCc#"

python3 create_database.py



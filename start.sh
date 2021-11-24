echo "Cloning Repo, Please Wait..."
git clone https://github.com/creatorPavan/RadioBaba.git /RadioBaba
echo "Installing Requirements..."
cd /RadioBaba
pip3 install -U -r requirements.txt
echo "Starting Bot, Please Wait..."
python3 main.py

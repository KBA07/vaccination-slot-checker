A Simple python program which checks for the vaccine slots available periodically given age
If vaccine slot is available it prints the available vaccination centres details on the Std Out

make sure python 3.8 is installed with virtualenv, pip
Clone this repo

virtualenv ENV
source ENV/bin/activate
pip install -r requirements.txt

Usage
python main.py 360 18 03-04-2021   # retry-after(sec), age, date (dd-mm-yyyy) # a prompt will be generate asking for search details
python main.py 900 21 03-04-2021 560078 # retry-after(sec), age, date (dd-mm-yyyy), pincode
python main.py 1200 45 03-04-2021 Karnataka BBMP # retry-after(sec), age, date (dd-mm-yyyy), state name, district name

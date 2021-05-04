# Vaccine Slot Checker
## A Simple python program which checks for the vaccine slots availability periodically for a given age.

If vaccine slots are available, then it prints the available vaccination centres details on the StdOut.

Make sure python 3.8 is installed with virtualenv and pip

#### Clone this repo
```
virtualenv ENV
source ENV/bin/activate
pip install -r requirements.txt
```

#### Usage
```
python main.py 900 18 03-05-2021   # retry-after(sec), age, date (dd-mm-yyyy) # a prompt will be generated asking for search details
python main.py 900 21 03-05-2021 560078 # retry-after(sec), age, date (dd-mm-yyyy), pincode
python main.py 1200 45 03-05-2021 Karnataka BBMP # retry-after(sec), age, date (dd-mm-yyyy), state name, district name
```

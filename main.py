import sys
import json
import time

from api_fetcher import APIFetcher
from logger import LOG

def run_main(retry_after, age, date, pincode=None, state_name=None, district_name=None):
    apiObj = APIFetcher(age, date, pincode, state_name, district_name)

    while True:
        centres = apiObj.get_centres_after_age_filter()
        if centres:
            LOG.info(f"Got {len(centres)} centres for vaccination")
            LOG.info(json.dumps(centres, indent=4))
            sys.exit(0)
        LOG.info(f"Didn't find any centres for vaccination")
        time.sleep(retry_after)


if __name__ == "__main__":

    # retry-after(sec), age, date (dd-mm-yyyy)
    # retry-after(sec), age, date (dd-mm-yyyy), pincode
    # retry-after(sec), age, date (dd-mm-yyyy), state name, district name
    
    argument_length = len(sys.argv)

    if argument_length == 4:
        retry_after, age, date = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
        run_main(retry_after, age, date)
    elif argument_length == 5:
        retry_after, age, date, pincode = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
        run_main(retry_after, age, date, pincode)
    elif argument_length == 6:
        retry_after, age, date, state_name, district_name = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5]
        run_main(retry_after, age, date, state_name=state_name, district_name=district_name)

    LOG.error("Not enought argument passed")




    

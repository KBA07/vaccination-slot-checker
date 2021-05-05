import sys
import json
import time

from api_fetcher import APIFetcher
from mailer import Mailer
from logger import LOG

def run_main(retry_after, age, date, pincode=None, state_name=None, district_name=None, sender_email=None, sender_password=None, reciever_email=None):
    apiObj = APIFetcher(age, date, pincode, state_name, district_name)

    mailer_obj = None
    if sender_email and sender_password and reciever_email:
        mailer_obj = Mailer(sender_email, sender_password)
    
    while True:
        try:
            centres = apiObj.get_centres_after_age_filter()
            if centres:
                subject = f"Got {len(centres)} centres for vaccination"
                LOG.info(subject)
                body = json.dumps(centres, indent=4)
                LOG.info(body)

                if mailer_obj:
                    mailer_obj.send_mail(subject, reciever_email, body)

                sys.exit(0)
                
            LOG.info(f"Didn't find any centres for vaccination")
            time.sleep(retry_after)
        except Exception:
            LOG.exception("Exception occurred while fetching, Re running the program")


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
    elif argument_length == 9:
        retry_after, age, date, state_name, district_name, sender_email, sender_password, reciever_email = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8]
        run_main(retry_after, age, date, state_name=state_name, district_name=district_name, sender_email=sender_email, sender_password=sender_password, reciever_email=reciever_email)
    LOG.error("Not enought argument passed")




    

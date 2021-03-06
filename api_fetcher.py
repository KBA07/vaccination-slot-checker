import sys
import json

import requests

import copy

from logger import LOG


class APIFetcher(object):
    COWIN_DOMAIN = "cdn-api.co-vin.in"
    COWIN_HOST = f"https://{COWIN_DOMAIN}/"
    CAPACATY_AT_LEAST = 1

    URI_GET_STATES = "api/v2/admin/location/states"
    URI_GET_DISTRICTS = "api/v2/admin/location/districts/{state_id}"
    URI_GET_VACCINE_SLOTS_DISTRICT = "api/v2/appointment/sessions/public/calendarByDistrict" # ?district_id=294&date=02-05-2021
    URI_GET_VACCINE_SLOTS_PINCODE = "api/v2/appointment/sessions/public/calendarByPin"   # ?pincode=560078&date=02-05-2021"


    def __init__(self, age, date, pincode=None, state=None, district=None):
        # API automatically returns x+7 days slot
        self.age = age
        self.date = date
        self.pincode = pincode
        self.state = state
        self.district = district
        self.district_id = None

        self.input_provided = False
        if self.pincode or (self.state and self.district):
            self.input_provided = True

    def get_vaccine_by_pin(self):
        return self._fetch_api(APIFetcher.URI_GET_VACCINE_SLOTS_PINCODE, params={'pincode':self.pincode, 'date':self.date}).get("centers", [])

    def get_vaccine_by_district(self):
        return self._fetch_api(APIFetcher.URI_GET_VACCINE_SLOTS_DISTRICT, params={'district_id':self.district_id, 'date':self.date}).get("centers", [])
    
    @staticmethod
    def _fetch_api(uri, params=None):
        url = APIFetcher.COWIN_HOST + uri
        headers = {
            'Host': APIFetcher.COWIN_DOMAIN, # Hack faking to be sent over website
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' # Hack, faking it to be a browsers request
        }
        LOG.info(f"Headers are {headers}")
        resp = requests.get(url, params=params, headers=headers)
        if resp.status_code == 200:
            try:
                return json.loads(resp.content)
            except Exception:
                LOG.exception(f"Exception occurred while fetching the API {uri}")
                sys.exit(1)
        LOG.error("Error occurred while fetching the API")
        LOG.info(f"Request headers are {resp.request.headers}")
        LOG.info(f"Resp status code are {resp.status_code}")
        LOG.info(f"Resp headers are {resp.headers}")
        LOG.info(f"Resp content are {resp.content}")
        sys.exit(1)

    def get_centres_after_age_filter(self):
        centres = self.get_slots()
        # LOG.debug(centres)
        if not centres:
            return centres

        age_centres = []
        for centre in centres:

            age_sessions = []
            for session in centre["sessions"]:
                if session['min_age_limit'] <= self.age and session['available_capacity'] >= APIFetcher.CAPACATY_AT_LEAST:
                    age_sessions.append(copy.deepcopy(session))
        
            if age_sessions:
                centre["session"] = age_sessions
                age_centres.append(copy.deepcopy(centre))
        
        return age_centres


    def get_slots(self):
        if not self.input_provided:
            search_by_pincode = input("Do you want to search by Pincode (y/n)")

            print(search_by_pincode)
            if search_by_pincode.lower() == "y":
                pincode = input("Please enter the pincode for slot:")
                self.pincode = pincode
                self.input_provided = True

                return self.get_vaccine_by_pin()

            resp = self._fetch_api(APIFetcher.URI_GET_STATES)

            disp_string = ""
            for state in resp["states"]:
                disp_string += f"{state['state_id']}\t{state['state_name']}\n"

            stateid = input(f"Specify the state id for the state which you want the slots for \nID\tState Name\n{disp_string}")

            resp = self._fetch_api(APIFetcher.URI_GET_DISTRICTS.format(state_id=stateid))

            disp_string = ""
            for district in resp["districts"]:
                disp_string += f"{district['district_id']}\t{district['district_name']}\n"

            district_id = input(f"Specify the district id for the district which you want the slots for \nID\tDistrict Name\n{disp_string}")
            self.district_id = district_id
            self.input_provided = True

            return self.get_vaccine_by_district()


        if self.pincode:
            return self.get_vaccine_by_pin()
        

        if self.district_id:
            return self.get_vaccine_by_district()

        # State name and District Name Given
        resp = self._fetch_api(APIFetcher.URI_GET_STATES)

        state_id = None
        disp_string = ""
        for state in resp["states"]:
            if state["state_name"] == self.state:
                state_id = state["state_id"]
                break
            disp_string += state["state_name"] + '\n'
        
        if not state_id:
            LOG.error(f"Incorrect State name provided in the script try again with the correct state name \n {disp_string}")
            sys.exit(1)

        resp = self._fetch_api(APIFetcher.URI_GET_DISTRICTS.format(state_id=state_id))
        district_id = None
        disp_string = ""
        for district in resp["districts"]:
            if district["district_name"] == self.district:
                district_id = district["district_id"]
                break
            disp_string += district['district_name'] + '\n'

        if not state_id:
            LOG.error(f"Incorrect disctrict name provided in the script try again with the correct disctrict name \n {disp_string}")
            sys.exit(1)

        self.district_id = district_id
        return self.get_vaccine_by_district()


if __name__ == "__main__":
    APIFetch = APIFetcher(45, "02-05-2021")

    print(APIFetch.get_centres_after_age_filter())
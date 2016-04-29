# RFIDTest.py
# Alexander Gotsis + agotsis + EE
# Tests andrewID lookup!

import urllib.request, json #used to fetch andrewID's from service, parse JSON

def lookupAndrewID(RFIDid):
        RFIDid = RFIDid.upper()
        url = "http://merichar-dev.eberly.cmu.edu:81/cgi-bin/card-lookup3?\
card_id=%s" % RFIDid
        try:
            response = urllib.request.urlopen(url) #fetch from cardservice port
        except urllib.error.HTTPError:
            print("Check the IP allow list!")
            return
        data = json.loads(response.read().decode('utf-8')) #convert to string
        print(data["andrewid"]) #dictionary lookup in the JSON object!

lookupAndrewID('49c8b374') #This is my card serial number. Should print agotsis
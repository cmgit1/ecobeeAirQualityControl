import io
import time
from datetime import datetime, timedelta
import requests as reqs
import json

import AirQualityReader

ecobee_base_url = "https://api.ecobee.com/"
api_versioni_url = "1/"
thermostat_request_url = "thermostat"
tokenFileName = "tokens.json"

def readJsonDataFromFile(filename):
    with open(filename, 'r') as token_file:
        data = json.load(token_file)
        return data

def writeTokenFile(tokens, filename):
    with open(filename, 'w') as token_file:
        json.dump(tokens, token_file, sort_keys=True, indent=4)

def refreshTokenRequest(tokens):
    req_data = {'grant_type': 'refresh_token', \
       'refresh_token': tokens['REFRESH_TOKEN'], \
       'client_id': tokens['API_KEY']}
    t = datetime.utcnow()
    access_token_expire = t + timedelta(0,0,0,0,0,1,0)
    refresh_token_expire = t + timedelta(365)
    r = reqs.post(ecobee_base_url + 'token', req_data)
    if r.status_code != 200:
        return False
    rj = r.json()
    tokens['REFRESH_TOKEN'] = rj['refresh_token']
    tokens['ACCESS_TOKEN'] = rj['access_token']
    tokens['ACCESS_EXPIRE'] = str(access_token_expire.timestamp())
    tokens['REFRESH_EXPIRE'] = str(refresh_token_expire.timestamp())
    return True

def updateAccessToken(tokens):
    access_token_expire = datetime.fromtimestamp(float(tokens['ACCESS_EXPIRE']))
    if datetime.utcnow() > access_token_expire:
        if refreshTokenRequest(tokens):
            writeTokenFile(tokens, tokenFileName)
            return True
        return False
    return True

def controlThermostat(tokens, controlJsonFileName):
    full_url = ecobee_base_url + api_versioni_url + thermostat_request_url
    auth_headers = {'Content-Type': 'application/json;charset=UTF-8', 'Authorization': 'Bearer ' + tokens['ACCESS_TOKEN']}
    req_data = readJsonDataFromFile(controlJsonFileName)
    r = reqs.post(full_url, headers = auth_headers, json=req_data)
    if r.status_code != 200:
        return False
    return True

def ecobeeControl(iaq: float, iaq_accuracy: int):
    print(f'IAQ {iaq:.0f}, IAQ Accuracy {iaq_accuracy:d}')


myTokens = readJsonDataFromFile(tokenFileName)
while (updateAccessToken(myTokens) == False):
    time.sleep(5)
while (controlThermostat(myTokens, "setHoldFanOn.json") == False):
    time.sleep(5)
time.sleep(60)
while (controlThermostat(myTokens, "resumeProgram.json") == False):
    time.sleep(5)

AirQualityReader.run(ecobeeControl)

import sys 
import pyotp
import os
import requests
import json

command = sys.argv[1]
elapsed = sys.argv[2]
exit_code = sys.argv[3]
otp_key = os.getenv('OTP_KEY')
url = os.getenv('TERM_NOTIFIER_URL')
coder = pyotp.TOTP(otp_key)

data = {
    "message": "{} elapsed={}secs, exit={}".format(command, elapsed, exit_code),
    "code":coder.now()
}

r = requests.post(url, json=data)
print(r)



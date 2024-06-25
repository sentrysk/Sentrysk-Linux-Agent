#!/usr/bin/env python3

# Libraries
##############################################################################
import subprocess
import re
from datetime import datetime
import pytz
##############################################################################

# Global Values
##############################################################################
TIME_REGEX = r'\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun) (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2} \d{2}:\d{2}:\d{2} \d{4}\b'
# Compile the pattern
TM_RE = re.compile(TIME_REGEX)

# Unix Date Format
NIX_DF = '%a %b %d %H:%M:%S %Y'

# Send Date Format
SND_DF = "%Y-%m-%d %H:%M:%S"
##############################################################################

# Functions
##############################################################################
def get_last_logons():
    last_logons = []

    for line in subprocess.check_output(["last", "-F"]).decode("utf-8").splitlines():
        fields = line.split()
        if len(fields) >= 7:
            user = fields[0]
            # Skip reboot
            if user.lower() == "reboot" or user.lower() == "shutdown":
                continue
            
            # Check if Time Regex matches
            match = re.search(TM_RE, line)
            if match:
                last_logon = match.group(0)
                # Convert date string to date format
                last_logon = datetime.strptime(last_logon, NIX_DF)
                # Convert date to UTC timezone
                last_logon = last_logon.astimezone(pytz.utc) 
                
                last_logons.append({
                    "username": user,
                    "last_logon": last_logon.strftime(SND_DF)
                })

    return last_logons
##############################################################################
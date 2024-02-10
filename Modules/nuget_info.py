#!/usr/bin/env python3

# Libraries
##############################################################################
import subprocess
import json
import logging
##############################################################################

# Functions
##############################################################################
def list_installed_packages():
    try:
        result = subprocess.run(["nuget", "list", "-AllVersions", "-Prerelease", "-Source", "https://api.nuget.org/v3/index.json", "--outputformat", "json"], capture_output=True, text=True, check=True)
        packages_data = json.loads(result.stdout)
        return packages_data
    except Exception as e:
        # Log the error
        logging.error(e)
        return {
            "running": "false"
        }
##############################################################################
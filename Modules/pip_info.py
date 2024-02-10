#!/usr/bin/env python3

# Libraries
##############################################################################
import pkg_resources
import logging
##############################################################################

# Functions
##############################################################################
def get_pip_packages():
    try:
        # Get a list of all installed packages using pkg_resources
        installed_packages = [
            {
                'name': package.project_name,
                'version': package.version
            }
            for package in pkg_resources.working_set
        ]
        pip_info = {
            "installed":True,
            "packages":installed_packages
        }
        return pip_info
    except Exception as e:
        pip_info = {
            "installed":False
        }
        # Log the error
        logging.error(e)
        return pip_info
##############################################################################
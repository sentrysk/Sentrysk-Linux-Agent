#!/usr/bin/env python3

# Libraries
##############################################################################
import subprocess
import logging
##############################################################################

# Functions
##############################################################################
def is_systemd():
    """Check if the system is using systemd as the init system."""
    try:
        # Check if systemd is running by executing the command
        subprocess.check_call(["pidof", "systemd"])
        return True
    except subprocess.CalledProcessError:
        return False

def get_service_info():
    """Collect information about services on a Linux system."""
    if not is_systemd():
        print("Error: This system does not use systemd as the init system.")
        return None

    try:
        # Run the systemctl command to get the list of all services
        cmd = "systemctl list-units --type=service --all --plain --no-legend"
        result = subprocess.check_output(cmd, shell=True, text=True)
        # Process the output and split it into lines
        lines = result.strip().split('\n')

        # Create a list to store the service information
        services_info = []

        # Skip the header line (UNIT LOAD ACTIVE SUB DESCRIPTION)
        for line in lines[1:]:
            # Split each line into columns
            columns = line.split(maxsplit=4)

            # Extract relevant information
            service_name = columns[0]
            #service_load = columns[1]
            #service_active = columns[2]
            service_status = columns[3]
            service_description = columns[4]

            # Append service information to the list
            services_info.append({
            	'display_name': service_name,
                'service_name': service_name,
                'status': service_status,
                'description': service_description
            })

        return services_info

    except subprocess.CalledProcessError as e:
        # Log the error
        logging.error(e)
        return []
##############################################################################
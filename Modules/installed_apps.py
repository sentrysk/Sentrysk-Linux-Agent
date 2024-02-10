#!/usr/bin/env python3

# Libraries
##############################################################################
import subprocess
import json
##############################################################################

# Functions
##############################################################################

def get_installed_programs():
    # Define the package managers and their respective handlers
    package_managers = {
        "apt": get_installed_programs_apt,          # APT package manager
        "dnf": get_installed_programs_dnf,          # DNF package manager
        "yum": get_installed_programs_yum,          # YUM package manager
        "pacman": get_installed_programs_pacman,    # Pacman package manager
        "snap": get_installed_programs_snap         # Snap package manager
    }

    installed_programs = []

    # Iterate over each package manager and retrieve the installed programs
    for package_manager, handler in package_managers.items():
        if is_command_available(package_manager):
            programs = handler()
            installed_programs.extend(programs)

    # Return the installed_programs
    return installed_programs


def is_command_available(command):
    # Check if the command is available
    try:
        subprocess.check_output(['which', command])
        return True
    except subprocess.CalledProcessError:
        return False


def get_installed_programs_apt():
    # Get installed programs using APT package manager
    command = "dpkg-query -Wf '${Package} ${Version}\n'"
    output = subprocess.check_output(command, shell=True, text=True)
    return [{"name": line.split(' ', 1)[0],    # Extract program name
             "version": line.split(' ', 1)[1],    # Extract program version
             "installed_by": "apt"} for line in output.split('\n') if line]


def get_installed_programs_dnf():
    # Get installed programs using DNF package manager
    command = "dnf list installed --quiet --installed"
    output = subprocess.check_output(command, shell=True, text=True)
    return [{"name": line.split()[0],    # Extract program name
             "version": line.split()[1],    # Extract program version
             "installed_by": "dnf"} for line in output.split('\n')[1:-1] if line]


def get_installed_programs_yum():
    # Get installed programs using YUM package manager
    command = "yum list installed"
    output = subprocess.check_output(command, shell=True, text=True)
    return [{"name": line.split()[0],    # Extract program name
             "version": line.split()[1],    # Extract program version
             "installed_by": "yum"} for line in output.split('\n')[1:-1] if line]


def get_installed_programs_pacman():
    # Get installed programs using Pacman package manager
    command = "pacman -Q"
    output = subprocess.check_output(command, shell=True, text=True)
    return [{"name": line.split()[0],    # Extract program name
             "version": line.split()[1],    # Extract program version
             "installed_by": "pacman"} for line in output.split('\n') if line]


def get_installed_programs_snap():
    # Get installed programs using Snap package manager
    command = "snap list"
    output = subprocess.check_output(command, shell=True, text=True)
    lines = output.split('\n')[1:-1]
    return [{"name": line.split()[0],    # Extract program name
             "version": line.split()[1],    # Extract program version
             "installed_by": "snap"} for line in lines if line]

##############################################################################

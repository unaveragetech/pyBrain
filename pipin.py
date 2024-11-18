"""
pipin.py: Automated Dependency Installer with Logging and Missing Library Detection

This script offers an automated solution for managing Python project dependencies by reading the 'requirements.txt' file, installing listed packages, logging the process, and identifying missing third-party libraries that should be added. With robust logging and flexible configuration, this tool ensures transparent and consistent dependency management across different environments.

Features:
---------
1. **Automated Dependency Installation**:
   - Reads the 'requirements.txt' file and installs packages using 'pip'.
   - Ensures that all required dependencies are installed without manual intervention.
   
2. **Progress Logging**:
   - Logs the installation process in detail to a file called 'install_log.txt'.
   - Includes timestamps for when installation starts and ends.
   - Logs successful installations and any encountered errors.
   
3. **Error Handling**:
   - Captures package-specific issues (e.g., version conflicts) as well as critical failures (e.g., subprocess errors).
   - Continues installing remaining packages even after an error occurs, logging all events for easy troubleshooting.

4. **Missing Library Detection**:
   - Scans all Python files in the project directory for third-party imports.
   - Identifies any libraries that are imported but not listed in 'requirements.txt' and appends them.
   
5. **Customizable**:
   - Users can omit certain libraries from installation by passing a list of libraries to the `install_requirements()` function.
   - The installation process can also be entirely disabled using a flag, allowing flexibility in different environments.

6. **Transparency and Traceability**:
   - All installation steps are logged, making it easy to trace which packages were installed and which failed.
   - The generated log file provides clear diagnostics for faster issue resolution.

7. **Efficient CI/CD and Team Collaboration**:
   - Ensures that all team members and automated environments (such as CI/CD pipelines) are working with the same set of dependencies, preventing version discrepancies.
   - The logging system makes it easy to audit installations and resolve issues across distributed teams.

Why Use This Script in Production?
-----------------------------------
1. **Automated Dependency Management**:
   - Automates the installation of required packages to avoid human error and ensure a consistent environment setup.

2. **Error Logging and Diagnostics**:
   - Logs all encountered errors, making it easy to troubleshoot failed installations.

3. **Missing Library Detection**:
   - Automatically identifies and adds missing third-party libraries to the 'requirements.txt' file, ensuring no dependencies are overlooked.

4. **Transparency and Accountability**:
   - Creates a log file ('install_log.txt') with a detailed audit trail of successful and failed installations.

5. **CI/CD Pipeline Integration**:
   - Ideal for integrating into continuous integration/continuous deployment (CI/CD) pipelines, automating dependency installation and ensuring consistency across different environments.

Usage:
------
1. Include this script in your project directory.
2. Ensure you have a 'requirements.txt' file listing the necessary Python packages.
3. Call the `install_requirements()` function at the beginning of your script to automatically install dependencies.

Example:
--------
    from pipin import install_requirements
    install_requirements()

    # Continue with the rest of your script here...

Log File Example:
-----------------
The 'install_log.txt' file will look like this:

===== Installation started at 2024-10-16 10:00:00 =====

===== Successful Installation =====
Successfully installed package1
Successfully installed package2

===== Installation Errors =====
Error installing package3: version conflict

===== Installation ended at 2024-10-16 10:05:00 =====

Conclusion:
-----------
This script ensures all project dependencies are consistently installed and updated, with full logging for transparency and troubleshooting. It also identifies and adds missing libraries to 'requirements.txt', making it an essential tool for production environments where automation, stability, and transparency are crucial.
"""

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import subprocess
import sys

def ensure_tqdm_installed():
    """
    Ensures that 'tqdm' is installed. If not, it installs the package.
    This function is used to add the tqdm progress bar library as a dependency.
    """
    try:
        # Try importing tqdm
        import tqdm
    except ImportError:
        # If tqdm is not installed, install it via pip
        print("tqdm not found. Installing it now...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tqdm'])
        print("tqdm successfully installed.")

# Call the function at the top to ensure tqdm is available
ensure_tqdm_installed()

# from pipin import install_requirements
import os
from datetime import datetime
import shutil
import time
from tqdm import tqdm  # Loading bar library
import pkgutil
import importlib


def install_requirements(omit_libraries=None, disable_installation=False):
    """
    Installs Python packages listed in 'requirements.txt', with additional options:
    
    - Omits specified libraries if needed.
    - Handles cases where 'pip' is not installed.
    - Optionally disable installation via a function argument.
    
    Args:
        omit_libraries (list, optional): A list of libraries to omit from installation.
        disable_installation (bool, optional): If set to True, skips the installation process.
    """
    log_file = 'install_log.txt'

    # If disable_installation is set to True, skip the entire installation process
    if disable_installation:
        with open(log_file, 'a') as log:
            log.write(f"===== Installation disabled by user at {datetime.now()} =====\n")
        print("Installation is disabled. Skipping the installation process.")
        return

    # Check if pip is installed
    if shutil.which('pip') is None:
        with open(log_file, 'a') as log:
            log.write(f"===== Critical Error: 'pip' is missing! at {datetime.now()} =====\n")
        print("Error: 'pip' is not installed. Please install 'pip' to proceed.")
        return

    # Read the requirements.txt file
    try:
        with open('requirements.txt', 'r') as req_file:
            requirements = req_file.readlines()
    except FileNotFoundError:
        with open(log_file, 'a') as log:
            log.write(f"===== Critical Error: 'requirements.txt' not found at {datetime.now()} =====\n")
        print("Error: 'requirements.txt' not found. Ensure the file exists in the project directory.")
        return

    # Filter out any libraries the user wants to omit
    if omit_libraries:
        requirements = [req for req in requirements if not any(omit in req for omit in omit_libraries)]

    with open(log_file, 'a') as log:
        log.write(f"\n\n===== Installation started at {datetime.now()} =====\n")

    # Install packages with a progress bar
    try:
        # Install the filtered list of requirements
        if requirements:
            # Create a temporary requirements file excluding omitted libraries
            temp_req_file = 'temp_requirements.txt'
            with open(temp_req_file, 'w') as temp_file:
                temp_file.writelines(requirements)

            # Loading bar for installation progress
            with tqdm(total=len(requirements), desc="Installing Packages") as pbar:
                result = subprocess.run(['pip', 'install', '-r', temp_req_file], capture_output=True, text=True)
                pbar.update(len(requirements))  # Update the loading bar once installation is complete

            # Log success messages
            with open(log_file, 'a') as log:
                log.write("===== Successful Installation =====\n")
                log.write(result.stdout)

            # Check for errors
            if result.returncode != 0:
                with open(log_file, 'a') as log:
                    log.write("===== Installation Errors =====\n")
                    log.write(result.stderr)
                print("Failed to install some packages. Check 'install_log.txt' for details.")
            else:
                print("All packages installed successfully.")

            # Clean up the temporary requirements file
            os.remove(temp_req_file)
        else:
            print("No packages to install. All requested libraries were omitted.")

    except subprocess.CalledProcessError as e:
        # Log critical errors (if subprocess itself fails)
        with open(log_file, 'a') as log:
            log.write(f"===== Critical Error: {e} =====\n")
        print(f"Installation failed. Error: {e}")

    # Finalizing log
    with open(log_file, 'a') as log:
        log.write(f"===== Installation ended at {datetime.now()} =====\n")

    # Check and add missing libraries to requirements.txt
    add_missing_libraries_to_requirements()


def is_standard_lib(module_name):
    """
    Checks if a module is part of the Python standard library.
    """
    return module_name in sys.builtin_module_names or pkgutil.find_loader(module_name) is None


def add_missing_libraries_to_requirements():
    """
    Scans all .py files in the current directory for third-party imports and adds any missing libraries to requirements.txt.
    """
    all_imports = set()
    py_files = [f for f in os.listdir('.') if f.endswith('.py')]

    for file in py_files:
        with open(file, 'r') as f:
            lines = f.readlines()

        for line in lines:
            if line.startswith('import ') or line.startswith('from '):
                parts = line.replace('import', '').replace('from', '').strip().split()
                if parts:
                    module = parts[0].split('.')[0]
                    if not is_standard_lib(module):
                        all_imports.add(module)

    # Update requirements.txt with missing third-party libraries
    try:
        with open('requirements.txt', 'r') as req_file:
            existing_requirements = req_file.readlines()
            existing_requirements = [r.strip() for r in existing_requirements]
    except FileNotFoundError:
        existing_requirements = []

    missing_libs = [lib for lib in all_imports if lib not in existing_requirements]

    if missing_libs:
        with open('requirements.txt', 'a') as req_file:
            req_file.writelines([lib + '\n' for lib in missing_libs])
        print(f"Added missing libraries to requirements.txt: {missing_libs}")
    else:
        print("No new libraries to add to requirements.txt.")


# Ensure that the script runs when install_requirements() is called
if __name__ == "__main__":
    install_requirements()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
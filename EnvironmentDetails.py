
import tkinter as tk
import os
import subprocess
import tempfile

class EnvironmentDetails:
    def __init__(self , main):
        self.root = main.root
        self.main = main
        self.details_frame = tk.Frame(self.root)

    def show_env_details(self, env_name):
        # Display environment details in the details frame
        details_label = tk.Label(self.main.main_frame, text=f"Environment Name: {env_name}", font=("Helvetica", 20))
        details_label.grid(row=0, column=1, padx=10, pady=5)

        # Get the list of installed packages and their versions
        packages = self.get_installed_packages(env_name)

        # Display the list of packages and versions
        if packages:
            for package in packages:
                package_label = tk.Label(self.details_frame, text=package, font=("Helvetica", 14))
                package_label.pack(pady=5)
        else:
            no_packages_label = tk.Label(self.details_frame, text="No packages installed in this environment", font=("Helvetica", 14))
            no_packages_label.pack(pady=5)

    def get_installed_packages(self, env_name):
        try:

            open_terminal_cmd = [
                "osascript",
                "-e",
                f'tell application "Terminal" to do script "cd ~/Desktop/python_env/ && source {env_name}/bin/activate && pip list"',
            ]

            # Run the command to open a new terminal window and execute the commands
            #result = subprocess.run(open_terminal_cmd, check=False , capture_output=True, text=True)

            result = subprocess.check_output(open_terminal_cmd, text=True)
            print(result)
            # Wait for the terminal to finish and close
            subprocess.run(f"sleep 5 && killall Terminal", shell=True, check=True)


            packages = []#result.strip().split('\n')[2:]  # Exclude header rows
            return packages
        except subprocess.CalledProcessError:
            print("error parsing")
            return []

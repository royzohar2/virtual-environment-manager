
import tkinter as tk
import os
import subprocess
import tempfile
from tkinter import messagebox


class EnvironmentDetails:
    def __init__(self , main):
        self.root = main.root
        self.main = main

    def show_env_details(self, env_name):
        # Display environment details in the details frame
        details_label = tk.Label(self.main.main_frame, text=f"Environment Name: {env_name}", font=("Helvetica", 20))
        details_label.grid(row=0, column=1, padx=10, pady=5)

        # Get the list of installed packages and their versions
        packages = self.get_installed_packages(env_name)
        i = 0 
        # Display the list of packages and versions
        if packages:
            for i, package in enumerate(packages):
                row_num = i // 3 + 1
                col_num = i % 3
                package_label = tk.Label(self.main.main_frame, text=package, font=("Helvetica", 14))
                package_label.grid(row=row_num, column=col_num, padx=10, pady=5)

        else:
            no_packages_label = tk.Label(self.main.main_frame, text="No packages installed in this environment", font=("Helvetica", 14))
            no_packages_label.grid(row=1, column=0, padx=10, pady=5)


         # Row number for command input and submit button
        buttons_row = len(packages) // 3 + 4 if packages else 2

        # Create a button to close the environment details frame
        close_button = tk.Button(self.main.main_frame, text="Close env", command=self.close_env_details)
        close_button.grid(row=buttons_row, column=0, padx=10, pady=5)

        # Open terminal
        open_terminal_button = tk.Button(self.main.main_frame, text="Open Terminal", command=lambda: self.open_terminal(env_name))
        open_terminal_button.grid(row=buttons_row, column=1, padx=10, pady=5)

        # Create a button to delete the environment
        delete_button = tk.Button(self.main.main_frame, text="Delete env", command=lambda: self.delete_env(env_name))
        delete_button.grid(row=buttons_row, column=2, padx=10, pady=5)

    def get_installed_packages(self , env_name):
        try:
            # Create a temporary file to capture the output
            with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
                temp_file_name = temp_file.name

            # Define the commands to execute in the new Terminal window
            commands = [
                f'cd ~/Desktop/python_env/',
                f'source {env_name}/bin/activate',
                f'pip list > {temp_file_name}',  # Redirect output to the temporary file
            ]

            # Create an AppleScript command to open a new terminal window and run the commands
            applescript = f'''
            tell application "Terminal"
                do script "{'; '.join(commands)}"
            end tell
            '''

            # Run the AppleScript command
            subprocess.run(['osascript', '-e', applescript])
            subprocess.run("sleep 2 && killall Terminal", shell=True, check=True)

                    # Read the output from the temporary file
            with open(temp_file_name, "r") as file:
                packages = file.readlines()

            # Delete the temporary file
            os.remove(temp_file_name)
            packages = [line.strip().replace("\n" , "") for line in packages[2:]]

            return packages
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Error parsing")
            return []


    def close_env_details(self):
        self.main.show_env_list()

    def delete_env(self, env_name):
        try:
            # Construct the command to delete the virtual environment
            command = f"rm -r ~/Desktop/python_env/{env_name}"

            # Run the command using subprocess
            subprocess.run(command, shell=True, check=True)

            print(f"Environment '{env_name}' deleted successfully.")

            # Refresh the environment list or perform any other necessary actions
            self.main.show_env_list()

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error deleting environment '{env_name}': {e}")


    
    def open_terminal(self, env_name):
        try:
            commands = [
                f'cd ~/Desktop/python_env/',
                f'source {env_name}/bin/activate',
            ]
            # Create an AppleScript command to open a new terminal window and run the commands
            applescript = f'''
            tell application "Terminal"
                do script "{'; '.join(commands)}"
            end tell
            '''

            # Run the AppleScript command
            subprocess.run(['osascript', '-e', applescript])

        except Exception as e:
            messagebox.showerror("Error", f"Error opening terminal: {e}")
      

   
import tkinter as tk
import os
from tkinter import messagebox
import subprocess
import json
class NewEnvironment():
    def __init__(self , main):
        self.root = main.root
        self.main = main
        with open("python_libraries.json", "r") as json_file:
            self.library_data = json.load(json_file)

    def new_env(self):
        details_label = tk.Label(self.main.main_frame, text="create new env", font=("Helvetica", 20))
        details_label.grid(row=0, column=1, padx=10, pady=5)

        env_name_label = tk.Label(self.main.main_frame, text="new env name:", font=("Helvetica", 20))
        env_name_label.grid(row=1, column=0, padx=10, pady=5)

        self.env_name_entry = tk.Entry(self.main.main_frame, width=40)
        self.env_name_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5)
        # Create and display checkboxes for each library
        self.library_vars = {}
        for i, library in enumerate(self.library_data.keys()):
            row_num = i // 3 +2
            col_num = i % 3
            var = tk.IntVar()
            self.library_vars[library] = var
            checkbox = tk.Checkbutton(self.main.main_frame, text=library, variable=var)
            checkbox.grid(row=row_num, column=col_num, padx=10, pady=5)
        
        close_button = tk.Button(self.main.main_frame, text="back to main", command=self.close_new_env)
        close_button.grid(row=row_num +1, column=0, padx=10, pady=5)

        # Create an Install button
        install_button = tk.Button(self.main.main_frame, text="Create", command=self.install_libraries)
        install_button.grid(row=row_num +1, column=2, padx=10, pady=5)
                

    def close_new_env(self):
        self.main.show_env_list()
        
    def install_libraries(self):
        env_name = self.env_name_entry.get()
        if not env_name:
            messagebox.showerror("Error", "Please enter a valid environment name.")
            return

        selected_libraries = [library for library, var in self.library_vars.items() if var.get() == 1]

        if not selected_libraries:
            messagebox.showerror("Error", "Please select at least one library to install.")
            return


        # Create pip installation commands for selected libraries
        pip_install_commands = [self.library_data[library] for library in selected_libraries]

        # Combine all commands into a single script
        commands = [
            f'cd ~/Desktop/python_env/',
            f"python3 -m venv {env_name}" ,
            f'source {env_name}/bin/activate',
            *pip_install_commands
        ]

        # Create an AppleScript command to open a new terminal window and run the commands
        applescript = f'''
        tell application "Terminal"
            do script "{'; '.join(commands)}"
        end tell
        '''

        print(commands)
        

        # Run the AppleScript command
        subprocess.run(['osascript', '-e', applescript])

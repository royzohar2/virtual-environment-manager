import tkinter as tk
import os
from EnvironmentDetails import EnvironmentDetails
class VirtualEnvManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Environment Manager")
        # Set the default window size
        self.root.geometry("600x700")

        self.main_frame = tk.Frame(root)
        self.main_frame.grid(row=0, column=0, columnspan=3)  # Ensure the frame is properly gridded

        # Get the full path to your desktop folder
        desktop_path = os.path.expanduser("~/Desktop")
        self.env_folder = os.path.join(desktop_path, "python_env")

        # Check if the 'python_env' folder exists
        if not os.path.exists(self.env_folder):
            os.makedirs(self.env_folder)  # Create the folder if it doesn't exist
        self.show_env_list()
        self.environment_details = EnvironmentDetails( self)


    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_env_list(self):
        self.clear_main_frame()


        # Create a headline label with custom style
        headline_label = tk.Label(self.main_frame, text="Virtual Environments", font=("Helvetica", 20))
        headline_label.grid(row=0, column=1, padx=10, pady=5)

        # List virtual environments in the 'python_env' folder
        self.env_names = [d for d in os.listdir(self.env_folder) if os.path.isdir(os.path.join(self.env_folder, d))]

        # Create styled buttons for each environment
        for i, env_name in enumerate(self.env_names):
            row_num = i // 3 + 1
            col_num = i % 3
            button = tk.Button(self.main_frame, text=env_name, command=lambda name=env_name: self.open_env(name), 
                               width=20, height=2, bg="lightblue", relief=tk.RAISED, font=("Helvetica", 12))
            button.grid(row=row_num, column=col_num, padx=10, pady=5)


        # Button to add a new environment
        add_button = tk.Button(self.main_frame, text="Add New Environment", command=self.add_env,
                               width=20, height=2, bg="lightgreen", relief=tk.RAISED, font=("Helvetica", 12))
        add_button.grid(row=row_num +1, column=1, padx=10, pady=5)

    def open_env(self, env_name):
        self.clear_main_frame()
        self.environment_details.show_env_details(env_name)

        # Implement the logic to open an environment here
        # You can launch a new window or perform any actions you need

    def add_env(self):
        self.clear_main_frame()

        pass
        # Implement the logic to add a new environment here
        # You can create a new virtual environment using the `venv` module or any other method




if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualEnvManagerApp(root)
    root.mainloop()

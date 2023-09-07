import tkinter as tk
from tkinter import ttk
import os
from EnvironmentDetails import EnvironmentDetails
from NewEnvironment import NewEnvironment

class VirtualEnvManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Environment Manager")
        # Set the default window size
        self.root.geometry("650x700")
        # Create A Main frame

        main_frame = ttk.Frame(root)

        main_frame.pack(fill=tk.BOTH,expand=1)

        # Create Frame for X Scrollbar

        sec = ttk.Frame(main_frame)

        sec.pack(fill=tk.X,side=tk.BOTTOM)

        my_canvas = tk.Canvas(main_frame)

        my_canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)

        # Add A Scrollbars to Canvas

        x_scrollbar = ttk.Scrollbar(sec,orient=tk.HORIZONTAL,command=my_canvas.xview)

        x_scrollbar.pack(side=tk.BOTTOM,fill=tk.X)

        y_scrollbar = ttk.Scrollbar(main_frame,orient=tk.VERTICAL,command=my_canvas.yview)
        y_scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

        # Configure the canvas

        my_canvas.configure(xscrollcommand=x_scrollbar.set)

        my_canvas.configure(yscrollcommand=y_scrollbar.set)

        my_canvas.bind("<Configure>",lambda e: my_canvas.config(scrollregion= my_canvas.bbox(tk.ALL))) 

        # Create Another Frame INSIDE the Canvas

        self.main_frame = tk.Frame(my_canvas)
        # Add that New Frame a Window In The Canvas

        my_canvas.create_window((0,0),window= self.main_frame, anchor="nw")

        self.custom_style = ttk.Style()
        self.custom_style.configure("Custom.TButton", background="red")


        # Get the full path to your desktop folder
        desktop_path = os.path.expanduser("~/Desktop")
        self.env_folder = os.path.join(desktop_path, "python_env")

        # Check if the 'python_env' folder exists
        if not os.path.exists(self.env_folder):
            os.makedirs(self.env_folder)  # Create the folder if it doesn't exist
        self.show_env_list()
        self.environment_details = EnvironmentDetails( self)
        self.new_env = NewEnvironment(self)
   

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
                               width=20, height=2,  relief=tk.RAISED, font=("Helvetica", 12))
            button.grid(row=row_num, column=col_num, padx=10, pady=5)


        # Button to add a new environment
        add_button = tk.Button(self.main_frame, text="Add New Environment", command=self.add_env,
                               width=20, height=2, relief=tk.RAISED, font=("Helvetica", 12))
        add_button.grid(row=row_num+1 , column=1, padx=10, pady=5)

    def open_env(self, env_name):
        self.clear_main_frame()
        self.environment_details.show_env_details(env_name)


    def add_env(self):
        self.clear_main_frame()
        self.new_env.new_env()
        


if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualEnvManagerApp(root)
    root.mainloop()

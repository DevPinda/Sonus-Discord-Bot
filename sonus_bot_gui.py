# Importing the TKinter library that is utilised to create a python based GUI for
# the Sonus Discord Bot, alongside the subprocess library that is used to create
# a subprocess that can run the main.py when the button is clicked as a subprocess
import tkinter as tk
import tkinter.messagebox as messagebox
import subprocess
import psutil
import os

# Sets permissions for this script, needed to stop the process of the Bot
try:
    os.chmod("sonus_bot_gui.py", 0o777)
except FileNotFoundError:
    print("File not found error")

# Create the root TKinter object
root = tk.Tk()

# Dedicated method used to style the GUI widgets and other utility uses
def gui_config():
    # Changes window title
    root.title('Sonus Bot')
    # Changes background colour
    root.config(bg='#36393F')
    # Sets weight of column and row grids based on the index(left argument)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=0)
    root.grid_rowconfigure(0, weight=1)

    # Two variables below return the size of the screen into width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Utilising the width and height of the screen and using them in order to
    # resize the window's screen with specified constant multipliers such as
    # '0.55', also used to position the window to the center of the screen
    width = int(screen_width * 0.575)
    height = int(screen_height * 0.55)
    x_offset = int((screen_width - width) / 2)
    y_offset = int((screen_height - height) / 2)
    root.geometry(f"{width}x{height}+{x_offset}+{y_offset}")

    # Creates a label and sets the text
    title_label = tk.Label(root, text='Welcome to the Sonus Discord Bot!')
    # Configures the label by styling the background and font styling
    title_label.config(bg='#36393F', font=('Roboto',24,'bold'), fg='#FFFFFF')
    # Sets row and column value of the label on the grid
    title_label.grid(row=0, column=0)

# Calls the function so the gui_config styling runs
gui_config()

process = None
# Declaring the main function
def run_main():
    global process
    # Initialising the process variable by creating a subprocess that runs the
    # 'main.py' file with python and returns the subprocesses's error messages
    process = subprocess.Popen(["python", "main.py"], stderr=subprocess.PIPE)
    # Run the function check_process every 1000ms
    root.after(1000, check_process)

def stop_main():
    if process is not None:
        try:
            # Get the process ID
            pid = process.pid
            # Get the process object
            proc = psutil.Process(pid)
            # Kills the process with the PID acquired
            proc.kill()
            process.kill()
            print("Bot stopped!")
            # Destroys the window as to close the GUI
            root.destroy()
        # Handles exception when the process isn't found
        except psutil.NoSuchProcess:
            messagebox.showerror("Error", "Process not found!")
        # Handles exception when the permission to stop the process is denied
        except psutil.AccessDenied:
            messagebox.showerror("Error", "Invalid Permissions, access denied!")
    # Info message to user to indicate they should start the bot before stopping it
    else:
        messagebox.showinfo("Info", "Please start the Bot before stopping it")
        messagebox.askquestion


# Declare the function check_process that checks the subprocesses's status
def check_process():
    # If nothing has been added to the poll function of the subprocess then the
    # function is called as a recursive call which is executed every 1000ms
    if process.poll() is None:
        root.after(1000, check_process)
    else:
        # If the return code of the subprocess doesn't equal to 0 then the
        # error message is retrieved and displayed in a message box 
        if process.returncode != 0 :
            error_message = process.stderr.read()
            messagebox.showerror("Error", error_message)

# Declares, initialises, configures the styling and sets the grid position of
# the button that is used to call the 'run_main' function defined earlier,
# so the button should run the 'main.py' script once the button is pressed
main_button = tk.Button(root, text="Run the Bot!", command=run_main)
main_button.config(bg="#5865F2",font=("Roboto", 16,"bold"), fg="#11193F")
main_button.grid(row=1, column=0, sticky='ew', ipady=12)

# Declares, initialises, configures the styling and sets the grid position of
# the button that is used to call the 'stop_main' function defined earlier,
# so the button should stop the 'main.py' script once the button is pressed
# and closes the window as well
stop_button = tk.Button(root, text="Stop the Bot and Close the Window!", command=stop_main)
stop_button.config(bg="#b30000",font=("Roboto", 16,"bold"), fg="#11193F")
stop_button.grid(row=2, column=0, sticky='ew', ipady=12)

root.protocol("WM_DELETE_WINDOW", stop_main)
# Call to the mainloop function of the TK library to the root window
root.mainloop()
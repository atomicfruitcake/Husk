"""!
@author atomicfruitcake

@date 2018
"""

from Tkinter import *
from orchestrator import Orchestrator


class HuskApp:
    def __init__(self, master):
        """
        Constructor for the GUI app
        @param master: main window of applicaiton
        """
        self.master = master
        master.title("Ballet SSH Orcherstrator")

        self.label = Label(master, text="Welcome to Ballet").pack()

        self.username_label = Label(master, text="Enter Username").pack()
        self.username = StringVar()
        self.username_field = Entry(master, textvariable=self.username).pack()

        self.hosts_label = Label(master, text="Enter Hosts").pack()
        self.hosts = StringVar()
        self.hosts_field = Entry(master, textvariable=self.hosts).pack()

        self.password_enabled = False
        self.password_button = Button(master, text="Password required?", command=self.enable_password).pack()
        self.password = StringVar()
        self.password_field = Entry(master, textvariable=self.password)
        self.password_field.config(state=DISABLED)
        self.password_field.pack()

        self.disable_known_hosts_button = Checkbutton(master, text="Disable Known Hosts?").pack()

        self.run = Button(master, text="Start", command=self.check_ready_to_start).pack()

        self.close_button = Button(master, text="Close", command=master.quit).pack()

    def enable_password(self):
        """
        Set password field to an ctive state
        """
        if self.password_enabled is False:
            self.password_button.config(state=NORMAL)
        else:
            self.password_button.config(state=DISABLED)
            self.password_enabled = True

    def check_ready_to_start(self):
        """
        Check that all required fields are filled
        """
        print(self.username)
        print(self.password_field.grab_status())


def setup_root():
    root = Tk()
    root.geometry("600x400")
    return root


if __name__ == "__main__":
    root = setup_root()
    my_gui = HuskApp(root)
    root.mainloop()

"""!
@author atomicfruitcake

@date 2018

GUI application for managing multiple parallel SSH sessions
"""
import os
from Tkinter import *
import ttk
import tkFileDialog
import ScrolledText

from orchestrator import Orchestrator


class BalletApp:
    def __init__(self, master):
        """
        Constructor for the GUI app
        @param master: main window of application
        """
        self.master = master

        self.master.configure()
        self.orchestrator = None
        self.master.title("Ballet SSH Orchestrator")
        self.keyfile = ""
        self.domains = []

        self.s = ttk.Style()
        self.s.theme_use("aqua")

        self.label = ttk.Label(master, text="Welcome to Ballet", font="Helvetica 18 bold").grid(row=0, column=0)

        self.username_label = ttk.Label(master, text="Enter Username").grid(row=1, column=0)
        self.username = StringVar()
        self.username_field = ttk.Entry(master, textvariable=self.username).grid(
            row=2, column=0
        )

        self.hosts_label = Label(master, text="Enter Each Host on a new line").grid(
            row=3, column=0
        )

        self.hosts = StringVar()
        self.hosts_field = ScrolledText.ScrolledText(master, bg="beige", height=5, width=40)
        self.hosts_field.delete("1.0", END)
        self.hosts_field.grid(row=4, column=0)

        def get_keyfile():
            """
            Open a file dialog window to allow user to select a keyfile (.pem)
            """
            self.keyfile = tkFileDialog.askopenfilename(
                initialdir="~/",
                title="Select keyfile"
            )
            self.keyfile_label = ttk.Label(
                master, text="Keyfile: {}".format(self.keyfile)
            ).grid(row=5, column=0)

        self.keyfile_select = ttk.Button(
            master,
            text="Choose Keyfile",
            command=get_keyfile
        ).grid(row=6, column=0)

        def enable_password():
            """
            Enable the password field
            """
            self.password_field.configure(state="normal")
            self.password_field.update()

        def disable_password():
            """
            Disable to password field
            """
            self.password_field.configure(state="disabled")
            self.password_field.update()

        password_switch = StringVar()
        self.disable_entry_radio_button = ttk.Radiobutton(
            master,
            text="No Password",
            variable=password_switch,
            value="0",
            command=disable_password,
        )
        self.disable_entry_radio_button.grid(row=7, column=0)
        self.enable_entry_radio_button = ttk.Radiobutton(
            master,
            text="Password",
            variable=password_switch,
            value="1",
            command=enable_password,
        )
        self.enable_entry_radio_button.grid(row=8, column=0)

        self.password = StringVar()
        self.password_field = Entry(
            master, width=80, show="*", textvariable=self.password
        )
        self.password_field.configure(state="disabled", width=20)
        self.password_field.grid(row=9, column=0)

        self.run = ttk.Button(master, text="Start", command=self.boot_sessions).grid(
            row=10, column=0
        )
        self.close_button = ttk.Button(master, text="Close", command=master.quit).grid(
            row=11, column=0
        )

    def error_popup(self, msg):
        """
        Display and error popup to inform user of a problem
        @param msg: message to display to user
        """
        popup = Tk()
        popup.wm_title("Error")
        label = ttk.Label(popup, text=msg, font=("Helvetica", 16))
        label.pack()
        close_button = ttk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack()
        popup.mainloop()

    def check_ready_to_start(self):
        """
        Check that all required fields are filled
        """
        def check_field(field, field_name):
            """
            Check that a field is valid for use
            @param field: value of field
            @param field_name: name of field
            """
            try:
                assert len(field) != 0
            except AssertionError:
                self.error_popup("Error: {} not specified".format(field_name))

        self.domains = self.hosts_field.get("1.0", END).splitlines()
        check_field(self.username.get(), "Username")
        check_field(self.keyfile, "Keyfile")
        check_field(self.domains, "Hosts")
        self.password = None if len(self.password.get()) == 0 else self.password

    def boot_sessions(self):
        """
        Load the session data into the orchestrator
        """
        self.check_ready_to_start()
        self.orchestrator = Orchestrator(
            keyfile=self.keyfile,
            username=self.username.get(),
            domains=self.domains,
            password=self.password.get() if self.password is not None else None,
        )
        self.create_ssh_windows()

    def create_ssh_windows(self):
        num_windows = len(self.domains)
        terminals = []
        for i in range(num_windows):
            terminal = Frame(root, height=400, width=500)
            window = terminal.winfo_id()
            os.system("xterm -into {} -geometry 40x20 -sb &".format(window))
            terminals.append(terminal)
            terminal.grid(row=12, column=i)

def setup_root():
    root = Tk()
    root.geometry("800x500")
    root.focus_set()
    root.bind("<Escape>", lambda e: e.widget.quit())
    root.configure(background="grey")
    return root


if __name__ == "__main__":
    root = setup_root()
    my_gui = BalletApp(root)
    root.mainloop()

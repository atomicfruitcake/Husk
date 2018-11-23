"""!
@author atomicfruitcake

@date 2018
"""

from Tkinter import *
import tkFileDialog
import ScrolledText
from orchestrator import Orchestrator


class BalletApp:
    def __init__(self, master):
        """
        Constructor for the GUI app
        @param master: main window of applicaiton
        """
        self.master = master
        self.orchestrator = None
        master.title("Ballet SSH Orchestrator")
        self.keyfile = ""
        self.domains = []
        self.label = Label(master, text="Welcome to Ballet").grid(row=0, column=0)

        self.username_label = Label(master, text="Enter Username").grid(row=1, column=0)
        self.username = StringVar()
        self.username_field = Entry(master, textvariable=self.username).grid(row=2, column=0)

        self.hosts_label = Label(master, text="Enter Hosts").grid(row=3, column=0)
        self.hosts = StringVar()
        self.hosts_field = ScrolledText.ScrolledText(master, bg='white', height=5)
        self.hosts_field.delete('1.0', END)
        self.hosts_field.grid(row=4, column=0)
        # self.hosts_field = Entry(master, textvariable=self.hosts).grid(row=4, column=0)

        def get_keyfile():
            """
            Open a file dialog window to allow user to select a keyfile (.pem)
            """
            self.keyfile = tkFileDialog.askopenfilename(
                initialdir="~/",
                title="Select keyfile"
            )
            self.keyfile_label = Label(master, text="Keyfile: {}".format(self.keyfile)).grid(row=5, column=0)

        self.keyfile_select = Button(master, text="Choose Keyfile", fg="black", command=get_keyfile).grid(row=6, column=0)

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

        switch = StringVar()
        self.disable_entry_radio_button = Radiobutton(master, text="No Password", variable=switch, value="0", command=disable_password)
        self.disable_entry_radio_button.grid(row=7, column=0)
        self.enable_entry_radio_button = Radiobutton(master, text="Password", variable=switch, value="1", command=enable_password)
        self.enable_entry_radio_button.grid(row=8, column=0)

        self.password = StringVar()
        self.password_field = Entry(master, width=80, show="*", textvariable=self.password)
        self.password_field.configure(state="disabled")
        self.password_field.grid(row=9, column=0)

        self.disable_known_hosts = BooleanVar()
        self.disable_known_hosts_button = Checkbutton(master, text="Disable Known Hosts", variable=self.disable_known_hosts).grid(row=10, column=0)
        self.run = Button(master, text="Start", command=self.boot_sessions).grid(row=11, column=0)
        self.close_button = Button(master, text="Close", command=master.quit).grid(row=12, column=0)

    def check_ready_to_start(self):
        """
        Check that all required fields are filled
        """
        self.domains = self.hosts_field.get('1.0', END).splitlines()
        assert(len(self.username.get()) != 0)
        assert(len(self.domains) != 0)
        assert (len(self.keyfile) != 0)
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
            disable_known_hosts=self.disable_known_hosts.get(),
            password=self.password.get()
        )
        print(self.orchestrator)

def setup_root():
    root = Tk()
    root.geometry("1000x800")
    root.focus_set()
    root.bind("<Escape>", lambda e: e.widget.quit())
    return root


if __name__ == "__main__":
    root = setup_root()
    my_gui = BalletApp(root)
    root.mainloop()

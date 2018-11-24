"""!
@author atomicfruitcake

@date 2018

Orchestrates multiple SSH sessions on multiple hosts with a single object.
"""
from fabric.connection import Connection


class Orchestrator:

    def __init__(
        self, keyfile, username, domains, disable_known_hosts=True, password=None
    ):
        """
        Constructor for the multi SSH login
        @param keyfile: str - path to SSH key required to access the domains
        @param username: str - username to ssh login with
        @param domains: list - list of domains to login to
        @param disable_known_hosts: bool
        @param password: str - password to use if challenged on login
        """
        self.username = username
        self.domains = domains
        self.disable_known_hosts = disable_known_hosts
        self.connect_kwargs = {"key_filename": keyfile}
        if password is not None:
            self.connect_kwargs["password"] = password
        self.connections = self.establish_connections()


    def establish_connections(self, port=22):
        """
        Establish the SSH connections as fabric connection objects
        @param port: int - port to connect on, default ssh port 22
        @return: list - fabric Connection objects
        """
        return [
            Connection(
                host="{user}@{domain}:{port}".format(
                    user=self.username,
                    domain=domain,
                    port=port
                )
            ) for domain in self.domains
        ]

    def open_connections(self):
        """

        @return:
        """
        [connection.open() for connection in self.connections]


    def run_command(self, command):
        """
        Run command on all connections
        @param command: str - command to run over all connections
        """
        print([connection.run(command) for connection in self.connections])


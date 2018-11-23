"""!
@author atomicfruitcake

@date 2018


"""
import multiprocessing
from fabric.api import settings



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
        self.keyfile = keyfile
        self.username = username
        self.domains = domains
        self.disable_known_hosts = disable_known_hosts
        self.password = password
        self.connections = self.__establish_connections()


    def __establish_connections(self):
        """
        Establish fabric SSH connections to all of the domains
        @return: list - fabric ssh connection
        """
        if self.password:
            return [
            settings(
                host_string="{}@{}".format(self.username, domain),
                disable_known_hosts=self.disable_known_hosts,
                key_filename=self.keyfile,
                password=self.password
            )
            for domain in self.domains
        ]
        else:
            return [
                settings(
                    host_string="{}@{}".format(self.username, domain),
                    disable_known_hosts=self.disable_known_hosts,
                    key_filename=self.keyfile,
                )
                for domain in self.domains
            ]

    def mp_connections(self):
        """

        @return:
        """
        return [
            multiprocessing.Process(
                target=connection,
                args=()
            )
            for connection in self.connections
        ]


    def run_command(self, command):
        """
        Run command on all connections
        @param command: str - command to run over all connections
        """
        for connection in self.connections:
            print(connection.run(command))

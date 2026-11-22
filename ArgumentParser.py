import sys
import argparse

class ArgumentParser():
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog='grizzly-cli', description='A tool for usage of grizzlysms.com in CLI, designed for terminal-adept users who want quick information about the service offered by grizzly-sms')
        self.parser.add_argument('-sl','--services-list', action='store_true')
        self.parser.add_argument('-cl', '--countries-list', action='store_true')
        self.parser.add_argument('-b', '--balance', action='store_true')
        self.parser.add_argument('-c', '--country')
        self.parser.add_argument('-s', '--service')
        self.arguments=self.parser.parse_args(sys.argv[1:]) 
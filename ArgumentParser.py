import argparse
import sys


class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog='grizzly-cli', description='A tool for usage of grizzlysms.com in CLI, designed for terminal-adept users who want quick information about the service offered by grizzly-sms')
        self.parser.add_argument('-sl','--services-list', action='store_true')
        self.parser.add_argument('-cl', '--countries-list', action='store_true')
        self.parser.add_argument('-stpw', '--static-tron-payment-wallet', action='store_true')
        self.parser.add_argument('-b', '--balance', action='store_true')
        self.parser.add_argument('-c', '--country')
        self.parser.add_argument('-s', '--service')
        self.parser.add_argument('-sc', '--service-code')
        self.parser.add_argument('-cc', '--country-code',  type=int)
        self.parser.add_argument('-minp', '--min-price', type=float)
        self.parser.add_argument('-minp', '--max-price', type=float)
        self.arguments=self.parser.parse_args(sys.argv[1:])
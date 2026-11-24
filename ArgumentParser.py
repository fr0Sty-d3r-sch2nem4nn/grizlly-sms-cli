import argparse
import sys


class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog='grizzly-cli', description='A tool for usage of grizzlysms.com in CLI, designed for terminal-adept users who want quick information about the service offered by grizzly-sms')
        
        # staric (non-param) methods
        self.parser.add_argument('-sl','--services-list', action='store_true')
        self.parser.add_argument('-cl', '--countries-list', action='store_true')
        self.parser.add_argument('-stpw', '--static-tron-payment-wallet', action='store_true')
        self.parser.add_argument('-b', '--balance', action='store_true')
        self.parser.add_argument('-aa', '--active-activations', action='store_true')
        self.parser.add_argument('-i', '--initialize', action='store_true')
        
        self.parser.add_argument('-c', '--country', type=str)
        self.parser.add_argument('-srv', '--service', type=str)
        self.parser.add_argument('-sc', '--service-code', type=str)
        self.parser.add_argument('-cc', '--country-code',  type=int)
        self.parser.add_argument('-s', '--save', help='This flag allows to store the records of e.g. countries or services list, but also the details on specific services and vendors offers details.')
        
        self.parser.add_argument('-sp', '--service-prices', action='store_true', help='Displays detailed information on the service prices')
        self.parser.add_argument('-rn', '--request-number', action='store_true', help='Is used to request a number for the service you specified in the arguments.')
        
        get_number_group = self.parser.add_argument_group('request-number')
        get_number_group.add_argument('-minP', '--min-price', type=float)
        get_number_group.add_argument('-maxP', '--max-price', type=float)
        get_number_group.add_argument("-aVI", '--allowed-vendors-ids')
        get_number_group.add_argument("-eVI", '--excluded-vendors-ids')
        get_number_group.add_argument('-epp', '--excluded-phone-prefixes')
        
        self.parser.add_argument('-aS', '--activation-status', action='store_true')
        self.parser.add_argument('-cas', '--change-activation-status', help='This flag is used to change the activation status for a cetain service.', action='store_true')
        self.parser.add_argument('-sN', '--status-number', type=int, help="\n-1: Cancel Activation\n1: Number Ready\n3: Request Next Code\n6: Complete Activation\n8: Cancel Activation")
        self.parser.add_argument('-aI', '-pI', '--activation-id', '--purchase-id', type=int)

        self.arguments=self.parser.parse_args(sys.argv[1:])
import argparse
import sys


class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog='grizzly-cli', description='A tool for usage of grizzlysms.com in CLI, designed for terminal-adept users who want quick information about the service offered by grizzly-sms')

        self.parser.add_argument('-sl','--services-list', action='store_true')
        self.parser.add_argument('-cl', '--countries-list', action='store_true')
        self.parser.add_argument('-stpw', '--static-tron-payment-wallet', action='store_true')
        self.parser.add_argument('-b', '--balance', action='store_true')
        self.parser.add_argument('-aa', '--active-activations', action='store_true')

        # get_status_group = self.parser.add_argument_group('-gs')
        self.parser.add_argument('-aI', '-pI', '--activation-id', '--purchase-id', type=int)

        self.parser.add_argument('-c', '--country', type=str)
        self.parser.add_argument('-srv', '--service', type=str)
        self.parser.add_argument('-sc', '--service-code', type=str)
        self.parser.add_argument('-cc', '--country-code',  type=int)

        # get_number_group = self.parser.add_argument_group('-gN', '-pN', '--get-number', '--purchase-number')
        self.parser.add_argument('-minP', '--min-price', type=float)
        self.parser.add_argument('-maxP', '--max-price', type=float)
        self.parser.add_argument("-aVI", '--allowed-vendors-ids')
        self.parser.add_argument("-eVI", '--excluded-vendors-ids')
        self.parser.add_argument('-epp', '--excluded-phone-prefixes')

        self.parser.add_argument('-s', '--save', help='This flag allows to store the records of e.g. countries or services list, but also the details on specific services and vendors offers details.')
        
        # change_activation_status = self.parser.add_argument_group('-cas', '--change-activation-status')
        self.parser.add_argument('-sN', '--status-number', type=int, help="\n -1: Cancel Activation\n1: Number Ready\n3: Request Next Code\n6: Complete Activation\n8: Cancel Activation")


        self.arguments=self.parser.parse_args(sys.argv[1:])
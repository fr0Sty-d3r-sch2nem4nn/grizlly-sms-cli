import argparse
import sys


class ArgsHandler:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog='grizzly-cli', description='A tool for usage of grizzlysms.com in CLI, designed for terminal-adept users who want quick information about the service offered by grizzly-sms')
        self.parser.add_argument('--version', '-v', action='version', version='%(prog)s v0.0.5')
        
        subparsers = self.parser.add_subparsers(dest='command', title=None, description=None, metavar='Available subcommands:', required=True)
        common = argparse.ArgumentParser(add_help=False)
        
        init_cmd = subparsers.add_parser('init', help="Initalizes the .env file or overwrites it once created.", parents=[common])
        
        default_arguments_group = common.add_argument_group('Default Arguments')
        default_arguments_group.add_argument('-c', '--country', help="The name of the phone-number's country you want to get the service for.", type=str)
        default_arguments_group.add_argument('-srv', '--service', help="The name of the service you want to get the numeber for.", type=str)
        default_arguments_group.add_argument('-sc', '--service-code', help="Grizzly-SMS specific code for a service type", type=str)
        default_arguments_group.add_argument('-cc', '--country-code',  type=int, help="Grizzly-SMS specific code for a country.")
        
        status_group = common.add_argument_group('Status Commands Arguments')
        status_group.add_argument('-sN', '--status-number', type=int, help="\n-1: Cancel Activation\n1: Number Ready\n3: Request Next Code\n6: Complete Activation\n8: Cancel Activation")
        status_group.add_argument('-aI', '-pI', '--activation-id', '--purchase-id', type=int)
        
        phone_request_group = common.add_argument_group('Phone Number Request Arguments')
        phone_request_group.add_argument('-minP', '--min-price', type=float, help="Determines the minimal price when request for a phone number is made.")
        phone_request_group.add_argument('-maxP', '--max-price', type=float, help="Determines the maximal price when request for a phone number is made.")
        phone_request_group.add_argument("-aVI", '--allowed-vendors-ids', help='Once making a request for a phone number, solely vendors with those ids will be allowed. Provide in a following format e.g. 434,23,34')
        phone_request_group.add_argument("-eVI", '--excluded-vendors-ids', help='Once making a request for a phone number, the offers from those vendors will be excluded while choosing an offer. Provide in a following format e.g. 434,23,34')
        phone_request_group.add_argument('-epp', '--excluded-phone-prefixes', help='Once making a request for a phone number, the phone-prexifes specified will be excluded while choosing an offer. Provide in a following format e.g. 434,23,34')
        
        common.add_argument('-s', '--save', help='This flag allows to store the records of e.g. countries or services list, but also the details on specific services and vendors offers details.', action='store_true')
        
        # static no 
        static_tron_wallet_parser = subparsers.add_parser('topup-wallet', help="Generates an address which you can use to replenish your Grizzly SMS balance with.", parents=[common])
        balance_parser = subparsers.add_parser('balance', help="Displays user's current balance in USD in GrizzlySMS.", parents=[common])
        services_list_parser = subparsers.add_parser('service-list', help='Displays all available services in GrizzlySMS.', parents=[common])
        country_list_parser = subparsers.add_parser('country-list', help='Displays all available countries in GrizzlySMS which you can get phone number for your services from.', parents=[common])
        active_activations = subparsers.add_parser('active-activations',help='Displays all active phone-number orders.', parents=[common])
        
        service_prices_cmd = subparsers.add_parser('get-service-price', help='Displays detailed information on the service prices', parents=[common])
        service_prices_cmd.add_argument_group(default_arguments_group)
        
        req_cmd = subparsers.add_parser('request-number', help='Request a number', parents=[common])
        req_cmd.add_argument_group(default_arguments_group)
        req_cmd.add_argument_group(phone_request_group)
        
        activation_status_parser = subparsers.add_parser('get-status', help="Display activation status of the phone-number order.", parents=[common])
        change_activation_status_parser = subparsers.add_parser('change-status', help='Sends a request for a phone number for specific service.', parents=[common])

        self.arguments=self.parser.parse_args(sys.argv[1:])
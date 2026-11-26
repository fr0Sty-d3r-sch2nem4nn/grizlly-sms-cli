from argparse import Namespace
import json
from os import environ

from dotenv import load_dotenv
from requests import request, Response

load_dotenv()

grizzly_api_key = environ.get("GRIZZLY_API_KEY")

class ApiHandler:
    def __init__(self):
        self.static_methods = {
            'init': self.provide_api_key,
            'service-list': self.get_available_services,
            'country-list': self.get_available_countries,
            'topup-wallet': self.set_static_usdt_address,
            'active-activations': self.get_active_activations_list,
            'balance': self.get_current_balance
        }
        
        self.dynamic_methods = {
            'get-service-price': self.get_current_service_prices,
            'request-number': self.request_service_number,
            'get-status': self.get_activation_status,
            'change-status': self.alter_activation_status
        }

    def provide_api_key(self):
        try:
            user_input_key = input("Provide your API-key for grizzly-sms: ")
            
            if grizzly_api_key:
                final_decision = input("Are you certain you want to change your already existing API-key ?")

                if final_decision.lower() == "no":
                    print("API-key change Aborted.")
                    return
        
            with open('.env', 'w') as file:
                file.write(f"export GRIZZLY_API_KEY={user_input_key}")
        
            print("The API-key has been successfully saved.")
        except Exception as error:
            print("Error occured while providing api key:", error)
        
    def get_available_countries(self):
        
        request_response = self.__retrieve_country_list()
        
        with open("countries.json", "w") as file:
            json.dump(request_response.json(), file, indent=3)
        
        for key, value in request_response.json().items():
            print(f'Country Name: {value['eng']}, Grizzly-SMS key: {key}\n')

    def get_available_services(self):
        try:
            request_response = self.__retrieve_services_list()
            
            with open("services.json", "w") as file:
                json.dump(request_response.json(), file, indent=3)

            for service in request_response.json()['services']:
                print(f"Service Name: {service['name']}\nGrizzlySMS Service-Code:{service['code']}\n")
            
            print("The list with services has been saved in services.json")
            
            return request_response.json()

        except Exception as err:
            print("available services error:", err)


    def get_current_balance(self):
        try:
            GET_CURRENT_BALANCE = f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={grizzly_api_key}&action=getBalance"

            request_response = request(method="GET", url=GET_CURRENT_BALANCE).text
            
            print(f"Your balance is: {float(request_response.split("ACCESS_BALANCE:")[1])}$")
        
        except Exception as error:
            print("Balance retrieval error: ", error)

    def get_active_activations_list(self):
        try:
            GET_ACTIVE_ACTIVATIONS = f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={grizzly_api_key}&action=getActiveActivations"

            request_response = request(method="GET", url=GET_ACTIVE_ACTIVATIONS)

            jsoned_response = request_response.json()

            if jsoned_response is None:
                print("No activations are active yet !")
                return

            for key, value in jsoned_response.items():
                print(f'{key}: {value}')
        
        except Exception as error:
            print("Error occured while retrieving activation list", error)
    
    def set_static_usdt_address(self):
        try:
            STATIC_WALLET_FOR_TOP_UP = f"https://api.grizzlysms.com/public/crypto/wallet?api_key={grizzly_api_key}&coin=usdt&network=tron"

            request_response = request(method="GET", url=STATIC_WALLET_FOR_TOP_UP)

            print(f"Your address on Tron Blockchain-Network for top-up of your Grizzly-SMS account\n\nAddress:{request_response.json()['wallet_address']}")
        
        except Exception as error:
            print("Static error for TRON occured an error", error)
    # methods requiring parameter
    # private methods for retrieval of information for calling the methods
    def __find_country_code_by_name(self, country_name):
        try:
            for key, value in self.__retrieve_country_list().json().items():
                if value['eng'].lower() == country_name.lower():
                    return int(value['id'])
            
            return None
        except Exception as error:
            print("Met an error while trying to find country code:", error)
    
    def __find_service_code_by_name(self, country_name):
        try:
            for service in self.__retrieve_services_list().json()['services']:
                if service['name'].lower() == country_name.lower():
                    return service['code']
        
            return None
        except Exception as error:
            print("Met an error while trying to find service code:", error)
    
    def __retrieve_country_list(self)->Response:
        try:
            GET_COUNTRIES_ENDPOINT = f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={grizzly_api_key}&action=getCountries"

            request_response = request(method="GET", url=GET_COUNTRIES_ENDPOINT)
        
            return request_response
        except Exception as error:
            print("Met an error while trying to retrieve the country list.")
    
    def __retrieve_services_list(self)->Response:
        try:
            GET_SERVICES_ENDPOINT = f"https://grizzlysms.com/stubs/handler_api.php?api_key={grizzly_api_key}&action=getServicesList"

            request_response = request(method="GET", url=GET_SERVICES_ENDPOINT)
        
            return request_response
        except Exception as error:
            print("Met an error while trying to retrieve the services list.")
    
    def handle_parameter_methods(self, args:Namespace, method_name:str):
        try:
            country_code:int = self.__find_country_code_by_name(args.country) if args.country else args.country_code
            service_code:int = self.__find_service_code_by_name(args.service) if args.service else args.service_code
            
            print("Request sent...")
            
            if method_name == 'request-number':
                self.dynamic_methods[method_name](service_code, country_code, args.max_price, args.min_price, args.excluded_vendors_ids, args.excluded_phone_prefixes, args.allowed_vendors_ids)

            if method_name == 'get-service-price':
                self.dynamic_methods[method_name](service_code, country_code)

            if method_name == 'change-status':
                self.dynamic_methods[method_name](args.status_number, args.activation_id)

            if method_name == 'get-status':
                self.dynamic_methods[method_name](args.activation_id)
        except Exception as error:
            print("Error occured while executing dynamic method: ", error)

    def get_current_service_prices(self, service:int, country:int):
        try:
            if service is None or country is None:
                raise Exception("Cannot perform any action as one of the inputs required is None")

            GET_CURRENT_COUNTRY = (
                f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={grizzly_api_key}&action=getPricesV3&service={service}&country={country}")

            request_response = request(method="GET", url=GET_CURRENT_COUNTRY)
            
            country_name = self.__retrieve_country_list().json()[f'{country}']['eng']
            
            print(f"Offers for numbers from {country_name}")
            
            service_data = request_response.json()[f'{country}'][f'{service}']
            
            print(f"Price: {service_data['price']}$\nAmount of available numbers: {service_data['count']}")
                
            if service_data.get('providers'):
                print(f'\nSpecific Data on providers:\n')
                for provider_id, provider_offer_data in service_data['providers'].items():
                    print(f'Provider Id: {provider_id}')
                    print(f'Amount of available numbers: {provider_offer_data['count']}')
                    print(f"Vendor's Prices for number: {(provider_offer_data['price'])}\n")
            
        except Exception as error:
            print('Error occured while retriving service prices', error)
    ## Phone number request
    def request_service_number(self,
        service,
        country,
        max_price,
        min_price,
        except_provider_ids,
        phone_exception,
        provider_ids):
        try:
            NUMBER_REQUEST_ENDPOINT = f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={grizzly_api_key}&action=getNumberV2&service={service}&country={country}"

            f'maxPrice={max_price}&providerIds={provider_ids}&exceptProviderIds={except_provider_ids}&phoneException={phone_exception}&minPrice={min_price}'

            request_response = request(method="GET", url=NUMBER_REQUEST_ENDPOINT)

            print(request_response.text)
            print(request_response.json())

            return request_response.json()
        
        except Exception as error:
            print("Error occured while requesting service number:", error)

    def alter_activation_status(self, status, _id):
        try:
            ACTIVATION_STATUS_ALTER_ENDPOINT = f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={grizzly_api_key}&action=setStatus&status={status}&id={_id}"

            request_response = request(
                method="POST", url=ACTIVATION_STATUS_ALTER_ENDPOINT
            )

            print(request_response.text)
            print(request_response.json())

            return request_response.json()
        
        except Exception as error:
            print("Error occured while changing activation status: ", error)

    def get_activation_status(self, _id):
        try:
            ACTIVATION_STATUS_RETRIEVE_ENDPOINT = f"https://api.grizzlysms.com/stubs/handler_api.php?{grizzly_api_key}=api_key&action=getStatusV2&id={_id}"

            request_response = request(method="GET", url=ACTIVATION_STATUS_RETRIEVE_ENDPOINT)

            print(request_response.text)
            print(request_response.json())

            return request_response.json()
        except Exception as error:
            print("Error occured while retrieving activation status: ", error)
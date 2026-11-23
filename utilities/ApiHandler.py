import json
from os import environ

from dotenv import load_dotenv
from requests import request

load_dotenv()

grizzly_api_key = environ.get("GRIZZLY_API_KEY")

class ApiHandler:
    def __init__(self):
        self.static_methods = {
            'initialize': self.provide_api_key,
            'services_list': self.get_available_services,
            'countries_list': self.get_available_countries,
            'static_tron_payment_wallet': self.set_static_usdt_address,
            'active_activations': self.get_active_activations_list,
            'balance': self.get_current_balance
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
        GET_COUNTRIES_ENDPOINT = f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={grizzly_api_key}&action=getCountries"

        request_response = request(method="GET", url=GET_COUNTRIES_ENDPOINT)

        with open("countries.json", "w") as file:
            json.dump(file, request_response.json())

        print(request_response.text)
        print(request_response.json())

    def get_available_services(self):
        try:
            GET_SERVICES_ENDPOINT = f"https://grizzlysms.com/stubs/handler_api.php?api_key={grizzly_api_key}&action=getServicesList"

            request_response = request(method="GET", url=GET_SERVICES_ENDPOINT)

            with open("services.json", "w") as file:
                json.dump(request_response.json(), file, indent=3)

            for service in request_response.json()['services']:
                print(f"Service Name: {service['name']}\nGrizzlySMS Service-Code:{service['code']}\n")
            
            print("The list with services has been saved in services.json")

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
        GET_ACTIVE_ACTIVATIONS = f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={grizzly_api_key}&action=getActiveActivations"

        request_response = request(method="GET", url=GET_ACTIVE_ACTIVATIONS)

        jsoned_response = request_response.json()

        if jsoned_response is None:
            print("No activations are active yet !")
            return
        
        print(jsoned_response)

    
    def set_static_usdt_address(self):
        STATIC_WALLET_FOR_TOP_UP = f"https://api.grizzlysms.com/public/crypto/wallet?api_key={grizzly_api_key}&coin=usdt&network=tron"

        request_response = request(method="GET", url=STATIC_WALLET_FOR_TOP_UP)

        print(f"Your address on Tron Blockchain-Network for top-up of your Grizzly-SMS account\n\nAddress:{request_response.json()['wallet_address']}")


    def get_current_prices_country(self, service, country):
        GET_CURRENT_COUNTRY = (
            f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={grizzly_api_key}&action=getPricesV3&service="
            f"{service}&country={country}"
        )

        request_response = request(method="GET", url=GET_CURRENT_COUNTRY)

        print(request_response.json())
        print(request_response.text)
        

        return request_response.json()

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
            print(error)

    def alter_activation_status(self, status, _id):
        ACTIVATION_STATUS_ALTER_ENDPOINT = f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={grizzly_api_key}&action=setStatus&status={status}&id={_id}"

        request_response = request(
            method="POST", url=ACTIVATION_STATUS_ALTER_ENDPOINT
        )

        print(request_response.text)
        print(request_response.json())

        return request_response.json()


    def get_activation_status(self, _id):
        ACTIVATION_STATUS_RETRIEVE_ENDPOINT = f"https://api.grizzlysms.com/stubs/handler_api.php?{grizzly_api_key}=api_key&action=getStatusV2&id={_id}"

        request_response = request(
            method="GET", url=ACTIVATION_STATUS_RETRIEVE_ENDPOINT
        )

        print(request_response.text)
        print(request_response.json())

        return request_response.json()
from os import environ

from dotenv import load_dotenv
from requests import request

load_dotenv()

grizzly_api_key = environ.get("GRIZZLY_API_KEY")

class ApiHandler:
    def __init__(self):
        pass

    def get_available_countries(self):
        GET_COUNTRIES_ENDPOINT = f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={grizzly_api_key}&action=getCountries"

        request_response = request(method="GET", url=GET_COUNTRIES_ENDPOINT).json()

        return request_response

    def get_available_services(self):
        try:
            GET_SERVICES_ENDPOINT = f"https://grizzlysms.com/stubs/handler_api.php?api_key={grizzly_api_key}&action=getServicesList"

            request_response: dict = request(method="GET", url=GET_SERVICES_ENDPOINT).json()

            return request_response
        except Exception as err:
            print("available services error:", err)


    def get_current_balance(self):
        try:
            GET_CURRENT_BALANCE = f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={grizzly_api_key}&action=getBalance"

            request_response = request(method="GET", url=GET_CURRENT_BALANCE).text
            
            return float(request_response.split("ACCESS_BALANCE:")[1])
        
        except Exception as error:
            print("Balance retrieval error: ", error)

    def get_active_activations_list(self):
        GET_ACTIVE_ACTIVATIONS = f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={grizzly_api_key}&action=getActiveActivations"

        request_response = request(method="GET", url=GET_ACTIVE_ACTIVATIONS).json()

        return request_response


    def get_current_prices_country(self, service, country):
        GET_CURRENT_COUNTRY = (
            f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={grizzly_api_key}&action=getPricesV3&service="
            f"{service}&country={country}"
        )

        request_response = request(method="GET", url=GET_CURRENT_COUNTRY).json()

        return request_response


    def set_static_usdt_address(self):
        STATIC_WALLET_FOR_TOP_UP = f"https://api.grizzlysms.com/public/crypto/wallet?api_key={grizzly_api_key}&coin=usdt&network=tron"

        request_response = request(method="GET", url=STATIC_WALLET_FOR_TOP_UP).json()

        return request_response


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

            request_response = request(method="GET", url=NUMBER_REQUEST_ENDPOINT).json()

            return request_response
        
        except Exception as error:
            print(error)

    def alter_activation_status(self, status, _id):
        ACTIVATION_STATUS_ALTER_ENDPOINT = f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={grizzly_api_key}&action=setStatus&status={status}&id={_id}"

        request_response = request(
            method="POST", url=ACTIVATION_STATUS_ALTER_ENDPOINT
        ).json()

        return request_response


    def get_activation_status(self, _id):
        ACTIVATION_STATUS_RETRIEVE_ENDPOINT = f"https://api.grizzlysms.com/stubs/handler_api.php?{grizzly_api_key}=api_key&action=getStatusV2&id={_id}"

        request_response = request(
            method="GET", url=ACTIVATION_STATUS_RETRIEVE_ENDPOINT
        ).json()

        return request_response

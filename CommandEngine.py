from ArgumentParser import ArgumentParser
from utilities.ApiHandler import ApiHandler, grizzly_api_key


class CommandEngine:
    def __init__(self):
        try:
            self.arguments = ArgumentParser().arguments
            self.api_handler = ApiHandler()

            if(grizzly_api_key is None):
                raise Exception("The key has not been provided you have to provide the")
        
        except Exception as error:
            print("Exception occured during command engine setup !", error)

    def command_run(self):
        try:
            pass
        
        except Exception as error:
            print("Command run error: ", error)
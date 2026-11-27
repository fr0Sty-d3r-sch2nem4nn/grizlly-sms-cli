from ArgumentParser import ArgsHandler
from utilities.ApiHandler import ApiHandler, grizzly_api_key


class CommandEngine:
    def __init__(self):
            self.arguments = ArgsHandler().arguments
            self.api_handler = ApiHandler()

            if(grizzly_api_key is None):
                print("You haven't set up the API-key ! Without it, you will not be able to perform any action related to your account.")
                self.api_handler.provide_api_key()
                return

    def command_run(self):
        try:
                
                if self.api_handler.static_methods.get(self.arguments.command):
                    self.api_handler.static_methods[self.arguments.command]()
                    return
                
                if self.api_handler.dynamic_methods.get(self.arguments.command):
                    self.api_handler.handle_parameter_methods(self.arguments, self.arguments.command)
                    return 
                
                raise Exception(f"No command of {self.arguments.command} has been found in the list of commands available.")
        
        except Exception as error:
            print("Command run error: ", error)
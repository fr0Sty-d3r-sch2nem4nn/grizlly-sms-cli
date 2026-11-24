from ArgumentParser import ArgumentParser
from utilities.ApiHandler import ApiHandler, grizzly_api_key


class CommandEngine:
    def __init__(self):
            self.arguments = ArgumentParser().arguments
            self.api_handler = ApiHandler()

            if(grizzly_api_key is None):
                print("You haven't set up the API-key ! Without it, you will not be able to perform any action related to your account.")
                self.api_handler.provide_api_key()
                return

    def command_run(self):
        try:
            for arg_tuple in self.arguments._get_kwargs():
                # print(arg_tuple)
                if self.api_handler.static_methods.get(arg_tuple[0]) and arg_tuple[1]:
                    self.api_handler.static_methods[arg_tuple[0]]()
                    break
                
                if self.api_handler.dynamic_methods.get(arg_tuple[0]) and arg_tuple[1]:
                    self.api_handler.handle_parameter_methods(self.arguments, arg_tuple[0])
                    break
        
        except Exception as error:
            print("Command run error: ", error)
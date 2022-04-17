class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class CustomMessages:

    @staticmethod
    def ok_blue(message):
        print(f"{bcolors.OKBLUE}{message}{bcolors.ENDC}")
    
    @staticmethod
    def ok_cyan(message):
        print(f"{bcolors.OKCYAN}{message}{bcolors.ENDC}")
    
    @staticmethod
    def ok_green(message):
        print(f"{bcolors.OKGREEN}Ok: {message}{bcolors.ENDC}")

    @staticmethod
    def warning(message):
        print(f"{bcolors.WARNING}Warning: {message}{bcolors.ENDC}")
        
    @staticmethod
    def fail(message):
        print(f"{bcolors.FAIL}Fail: {message}{bcolors.ENDC}")

    @staticmethod
    def bold(message):
        print(f"{bcolors.BOLD}{message}{bcolors.ENDC}")
    
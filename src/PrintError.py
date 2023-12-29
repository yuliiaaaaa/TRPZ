class Printer:
    def print_error(self, error_message):
        print("\033[91m" + f"Error: {error_message}" + "\033[0m")


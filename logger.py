from termcolor import colored

class Log:
    def success(string):
        print(f"[{colored('✔', 'green')}] {string}")

    def info(string):
        print(f"[{colored('i', 'blue')}] {string}")

    def warn(string):
        print(f"[{colored('!', 'yellow')}] {string}")

    def error(string):
        print(f"[{colored('✘', 'red')}] {string}")

    
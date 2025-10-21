from os import getcwd
from socket import gethostname


def print_initial_greeting():
    print("Welcome to Martin's interpreter project 1 for COMP 377.", end='\n')


def get_input_command():
    prompt_string = ("Enter your command, or type \"help\" for help.\n"
                     f"martin_interpreter@{gethostname()}:{getcwd()}>>>")

    user_input = get_raw_user_input(prompt_string)

    user_input = user_input.strip().split()

    command = user_input[0].lower()
    arguments = user_input[1:]

    return command, arguments


def get_raw_user_input(prompt_string):
    try:
        return input(prompt_string)
    except EOFError:
        return "quit"


def print_quit_message():
    print("Thank you for using this interpreter")

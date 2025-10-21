from .utils import interpreter_actions as ia
from .utils import interpreter_terminal_io as itio
from typing_extensions import assert_never

def main():
    # Greets user and executes the main event loop
    itio.print_initial_greeting()

    command, arguments = itio.get_input_command()

    while command != "quit":
        execute_input(command, arguments)

        command, arguments = itio.get_input_command()

    itio.print_quit_message()


def execute_input(command, arguments):
    # Matches the command to the correct branch of the interpreter
    match command:
        case "list":
            print("Executing list")
            ia.list_dir(arguments)
        case "chdir":
            print("Executing chdir")
            ia.chdir(arguments)
        case "run":
            print("Executing run")
            ia.run(arguments)
        case "remove":
            print("Executing remove")
            ia.remove(arguments)
        case "rename":
            print("Executing rename")
            ia.rename(arguments)
        case "help":
            print("Executing help")
            ia.user_help()
        case "quit":
            print("Executing quit")
            assert_never("quit")
        case _:
            ia.print_error_message(command)


if __name__ == "__main__":
    main()

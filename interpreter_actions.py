import os
import platform
import getpass
import subprocess
import sys


def list_dir(arguments):
    # lists the contents of the directory
    if len(arguments) not in [0, 1]:
        print(f"Either 0 or 1 arguments required, {len(arguments)} found.")
        return

    target_directory = filename_getter(arguments)

    if not os.path.exists(target_directory):
        print(f"Directory {target_directory} not found.")
        return

    directory_contents = os.listdir(target_directory)
    formatted_directory_contents = "\t".join(directory_contents)
    print(formatted_directory_contents)


def filename_getter(arguments):
    # parses filenames from the user, using common substitution rules
    if len(arguments) == 0:
        return '.'
    elif len(arguments) > 1:
        raise ValueError(f"{len(arguments)} arguments found; too many arguments.")

    target = arguments[0]

    if target[0] == "~" and platform.system() == "Windows":
        target = "C:\\Users\\" + getpass.getuser() + target[1:]
    elif target[0] == "~":
        target = "/home/" + getpass.getuser() + target[1:]

    return target


def chdir(arguments):
    # change directory
    if len(arguments) != 1:
        print(f"Exactly 1 argument required, {len(arguments)} found.")
        return

    target_directory = filename_getter(arguments)

    try:
        os.chdir(target_directory)
    except FileNotFoundError:
        print(f"Error: Directory {target_directory} not found.")


def run(arguments):
    # run a given executable
    if len(arguments) != 1:
        print(f"Exactly 1 argument required, {len(arguments)} found.")
        return

    if isinstance(arguments, list):
        arguments = ' '.join(arguments)

    pid = os.fork()
    if pid == 0:
        run_child(arguments)
    else:
        pid, status = os.waitpid(pid, 0)

    print(f"Parent {pid} ending command `run`.")



def run_child(external_command):
    # as a child, run an external executable
    try:
        process = subprocess.run(external_command, shell=True) # prints "hello from outside."
    except FileNotFoundError:
        print(f"File {external_command} not found.")
    finally:
        pid = os.getpid()
        print(f"Terminating child with pid: {pid}.")
        sys.exit()


def remove(arguments):
    # remove a file or folder from the files index
    if len(arguments) != 1:
        print(f"Exactly 1 argument required, {len(arguments)} found.")
        return

    target = filename_getter(arguments)

    if os.path.isdir(target):
        target_type = "dir"
    elif os.path.isfile(target):
        target_type = "file"
    else:
        print("Target type neither folder nor file. Could not complete remove action")
        return


    confirmation = input(f"remove {target}?\ny/n\t")
    if confirmation == "y":
        if target_type == "file":
            os.remove(target)
        else:
            os.rmdir(target)


def rename(arguments):
    # rename a file
    if len(arguments) != 2:
        print(f"Exactly 2 arguments required, {len(arguments)} found.")
        return

    target, destination = arguments[0], arguments[1]

    os.rename(target, destination)


def user_help():
    # print help for the user
    print(
        """\n\
Available commands:
    list [path]: (implemented)
        Lists the contents of the directory/folder at path. Uses the current location by default.
    chdir [path]: (implemented)
        Changes the working directory to path.
    run [path]: (implemented)
        Runs the executable file at path.
    remove [path]: (implemented)
        Removes the file from the index of its parent, deleting it.
    rename [old] [new]: (implemented)
        Renames the file named old to the name of new.
    help: (implemented)
        Prints this message.
    quit: (implemented)
        Exits the program.\n\
"""
    )


def print_error_message(command):
    # print an unrecognized command error message
    print(
        f"{command} is not a known command to this interpreter.",
        r'Type "help" for help or "quit" to quit.',
        sep="\n"
    )

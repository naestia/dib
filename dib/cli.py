# -*- coding: utf-8 -*-

# python std lib
import logging
import os
import pdb
import sys
import traceback

# 3rd party imports
from docopt import docopt, extras, Option, DocoptExit

base_args = """
Usage:
    dib [<command>] [options] [<args> ...]

Commands:
    cd     Change to the specified directory
    ls     List all files in the specified directory
    find   Print absolute path for the specified file/directory

Options:
    --help          Show this help message and exit
    --version       Display the version number and exit
"""


sub_cd_args = """
Usage:
    dib cd [options] [<path>]

Options:
    -h, --help       Show this help message and exit
"""


sub_ls_args = """
Usage:
    dib ls [options] [<path>]

Options:
    -a, --all        List all files in a directory, includes hidden "." files (as ls -a)
    -l               Use a long list format (as ls -l)
    -h, --help       Show this help message and exit
"""


sub_find_args = """
Usage:
    dib find (--type=<t>) [<path>]

Options:
    -t=<t>, --type=<t>       Defines either 'file' or 'dir'
    -h, --help               Show this help message and exit
"""


def parse_cli():
    """
    Parse the CLI arguments and options
    """
    import dib

    try:
        cli_args = docopt(
            base_args,
            options_first=True,
            version=dib.__version__,
            help=True,
        )
    except DocoptExit:
        extras(
            True,
            dib.__version__,
            [Option("-h", "--help", 0, True)],
            base_args,
        )

    # Set INFO by default, else DEBUG log level
    dib.init_logging(5 if "DEBUG" in os.environ else 4)

    argv = [cli_args["<command>"]] + cli_args["<args>"]

    if cli_args["<command>"] == "cd":
        sub_args = docopt(sub_cd_args, argv=argv)
    elif cli_args["<command>"] == "ls":
        sub_args = docopt(sub_ls_args, argv=argv)
    elif cli_args["<command>"] == "find":
        sub_args = docopt(sub_find_args, argv=argv)
    else:
        extras(
            True,
            dib.__version__,
            [Option("-h", "--help", 0, True)],
            base_args,
        )
        sys.exit(1)

    # In some cases there is no additional sub args of things to extract
    if cli_args["<args>"]:
        sub_args["<sub_command>"] = cli_args["<args>"][0]

    return (cli_args, sub_args)


def run(cli_args, sub_args):
    """
    Execute the CLI
    """
    log = logging.getLogger(__name__)

    retcode = 0

    log.debug(cli_args)
    log.debug(sub_args)

    from dib.core import DIB

    core = DIB(current_dir=sub_args.get("<path>"))

    if cli_args["<command>"] == "cd":
        retcode = core.cd()

    if cli_args["<command>"] == "ls":
        flags = ""
        if sub_args["--all"] and sub_args["-l"]:
            flags = "-al"
        elif sub_args["--all"]:
            flags = "-a"
        elif sub_args["-l"]:
            flags = "-l"

        retcode = core.ls(flags)

    if cli_args["<command>"] == "find":
        flag = ""

        if sub_args["--type"] == "f":
            flag = "f"
        elif sub_args["--type"] == "d":
            flag = "d"
        else:
            log.error("Option: '--type' must be either 'f' for 'file', or 'd' for 'directory'")
            log.error("Exiting with exitcode 1")
            return 1

        if flag:
            retcode = core.find(flag)

    return retcode


def cli_entrypoint():
    """
    Used by setup.py to create a cli entrypoint script
    """
    try:
        cli_args, sub_args = parse_cli()
        exit_code = run(cli_args, sub_args)
        sys.exit(exit_code)
    except Exception:
        ex_type, ex_value, ex_traceback = sys.exc_info()

        if "DEBUG" in os.environ:
            extype, value, tb = sys.exc_info()
            traceback.print_exc()

            if "PDB" in os.environ:
                pdb.post_mortem(tb)

            raise
        else:
            print(f"Exception type : {ex_type.__name__}")
            print(f"EXCEPTION MESSAGE: {ex_value}")
            print("To get more detailed exception set environment variable 'DEBUG=1'")
            print("To PDB debug set environment variable 'PDB=1'")

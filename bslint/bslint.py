"""bslint.bslint: provides entry point main()."""
__version__ = "0.6.0"
from bslint.interface_handler import InterfaceHandler as InterfaceHandler
import sys
import os


def main():
    interface_handler = InterfaceHandler()
    interface_handler.main()


def runner(to_lex=None):
    sys.argv = [sys.argv[0]]
    if to_lex is not None:
        sys.argv.append(os.path.abspath(to_lex))
    else:
        sys.argv.append(os.getcwd())
    interface_handler = InterfaceHandler()
    interface_handler.main()
    return interface_handler

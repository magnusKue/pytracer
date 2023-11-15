import sys

from colorama import init as colorama_init
from colorama import Fore, Back, Style
colorama_init()

class Error:
    def __init__(self) -> None:
        pass

    @staticmethod
    def raiseError(type:str, info:str, quitSrc:bool=False):
        print(f"\n\n{Back.RED}Error: {type}{Style.RESET_ALL}")
        print(f"\n{Fore.RED}{info}{Style.RESET_ALL}\n")
        if quitSrc:
            sys.exit()
import argparse, pathlib, sys, shutil
from rendertarget import str2bool
from colorama import init as colorama_init
from colorama import Fore, Back, Style
colorama_init()

class Parser:
    def __init__(self, defaultSamples, defaultAR, defaultImageWidth, defaultBounceCap, defaultDest, defaultPreview, defaultWhite) -> None:
        self.parser = argparse.ArgumentParser(description=f'{Back.GREEN}{Fore.BLACK} - A simple python raytracer - {Style.RESET_ALL}')

        self.parser.add_argument('--scene', "-S", "-scn",        type=str,      default="scene1",         help=f"{Fore.GREEN}Load a scene from world.json. {Fore.RED}No defaults{Style.RESET_ALL}")
        self.parser.add_argument('--samples', "-s", "-smp",      type=int,      default=defaultSamples,   help=f'{Fore.GREEN}Number of samples per pixel. {Fore.RED}Default is {defaultSamples}{Style.RESET_ALL}')
        self.parser.add_argument('--bounces', "-b", "-bnc",      type=int,      default=defaultBounceCap, help=f'{Fore.GREEN}Ray bounce cap. {Fore.RED}Default is {defaultBounceCap}{Style.RESET_ALL}')
        self.parser.add_argument('--resolution', "-r", "-res",   type=str,      default=None,             help=f'{Fore.GREEN}Image resolution as WIDTHxHEIGHT (Bsp: "600x400"). {Fore.RED}Default is {defaultImageWidth}x{max(1, int(defaultImageWidth / defaultAR))}{Style.RESET_ALL}')
        self.parser.add_argument('--destination', "-d", "-dest", type=str,      default=defaultDest,      help=f'{Fore.GREEN}Path to the rendered image. {Fore.RED}Default is {pathlib.Path(__file__).resolve().parent / pathlib.Path("../output.ppm")}{Style.RESET_ALL}')
        self.parser.add_argument('--preview', "-p", "-prev",     type=str2bool, default=defaultPreview,   help=f'{Fore.GREEN}Choose if you want a live pygame render preview. (Y/N|true/false|yes/no){Fore.RED}Default is true{Style.RESET_ALL}')
        self.parser.add_argument('--usewhite', "-u", "-uw",      type=str2bool, default=defaultWhite,     help=f'{Fore.GREEN}Choose if you want to use a white default font instead of a cyan one. {Fore.RED}Default is false{Style.RESET_ALL}')
        self.parser.add_argument('--about', '-a', action="store_true", help="About the project.")

        self.defaultAR = defaultAR
        self.defaultImageWidth = defaultImageWidth

    def getArgs(self):
        args = self.parser.parse_args()
        if args.about:
            with open(pathlib.Path(__file__).resolve().parent / pathlib.Path("../res/about.txt"), "r") as fp:
                about = fp.readlines()

            for x, line in enumerate(about):
                if x == 0:
                    print(f"\n"+(f"{Fore.BLACK}" + f"{Back.CYAN} - {line.replace("\n","")}: - {Style.RESET_ALL}\n".center(min(92, int(shutil.get_terminal_size().columns)))) + f"{Style.RESET_ALL}", end="")
                else:
                    print(f"{Fore.CYAN}{line.replace("\n","")}{Style.RESET_ALL}".center(92))
            print(f"\n"+(Fore.BLACK + f"- {Fore.RED}Magnus{Style.RESET_ALL}".center(min(92, int(shutil.get_terminal_size().columns)))), end="")
            

            sys.exit()
        return args

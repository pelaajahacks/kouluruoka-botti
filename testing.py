from colorama import Fore
from colorama import init as colorama_init

colorama_init()

colors = [x for x in dir(Fore) if x[0] != "_"]
print(colors)




colors = ['RED', 'LIGHTRED_EX', 'YELLOW', 'LIGHTYELLOW_EX', 'GREEN', 'LIGHTGREEN_EX', 'BLUE', 'CYAN', 'LIGHTBLUE_EX', 'LIGHTCYAN_EX', 'MAGENTA', 'LIGHTMAGENTA_EX']
colors_ansi = ["\033[31m", "\033[91m", "\033[33m", "\033[93m", "\033[32m", "\033[92m", "\033[34m", "\033[36m", "\033[94m", "\033[96m", "\033[35m", "\033[95m"]

for color in colors_ansi:
    print(color, "yooo")
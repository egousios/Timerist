import click
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

@click.command()
@click.option('--getjson', help='get editor settings json data')
@click.argument('user', required=True)
def get(user, getjson):
    try:
        with open(f"users/{user}/editor_settings.json") as file:
            data = file.readlines()
            file.close()
        ln_num = 0
        for ln in data:
            ln_num += 1
            print(Fore.CYAN + str(ln_num), ln)
    except Exception as E:
        print(Fore.RED + str(E))

@click.command()
@click.option('--clear', help='clear editor settings json data')
@click.argument('user', required=True)
def clear(user, clear):
    try:
        with open(f"users/{user}/editor_settings.json") as file:
            data = file.readlines()
            file.close()
        ln_num = 0
        for ln in data:
            ln_num += 1
            print(Fore.CYAN + str(ln_num), ln)
    except Exception as E:
        print(Fore.RED + str(E))

if __name__ == '__main__':
    clear()
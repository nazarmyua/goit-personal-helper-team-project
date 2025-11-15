from colorama import Fore, Style, init

init(autoreset=True)


def success(msg: str) -> str:
    return f"{Fore.GREEN}SUCCESS:{Style.RESET_ALL} {msg}"


def error(msg: str) -> str:
    return f"{Fore.RED}ERROR:{Style.RESET_ALL} {msg}"


def warning(msg: str) -> str:
    return f"{Fore.YELLOW}WARNING:{Style.RESET_ALL} {msg}"


def info(msg: str) -> str:
    return f"{Fore.BLUE}INFO:{Style.RESET_ALL} {msg}"


def simple_text(msg: str) -> str:
    return f"{Fore.BLUE}{msg}"

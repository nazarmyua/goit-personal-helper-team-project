from colorama import Fore, Style, init

init(autoreset=True)


def success(msg: str) -> str:
    """Format a success message with green color."""
    return f"{Fore.GREEN}SUCCESS:{Style.RESET_ALL} {msg}"


def error(msg: str) -> str:
    """Format an error message with red color."""
    return f"{Fore.RED}ERROR:{Style.RESET_ALL} {msg}"


def warning(msg: str) -> str:
    """Format a warning message with yellow color."""
    return f"{Fore.YELLOW}WARNING:{Style.RESET_ALL} {msg}"


def info(msg: str) -> str:
    """Format an info message with blue color."""
    return f"{Fore.BLUE}INFO:{Style.RESET_ALL} {msg}"


def simple_text(msg: str) -> str:
    """Format text with blue color."""
    return f"{Fore.BLUE}{msg}"

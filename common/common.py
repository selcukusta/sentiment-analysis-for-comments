class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def colored_print(print_type: bcolors, text: str):
    print(f"{print_type}{text}{bcolors.ENDC}")


if __name__ == '__main__':
    colored_print(bcolors.FAIL, "Epic Fail!")
    colored_print(bcolors.WARNING, "Are you sure you want to continue?")

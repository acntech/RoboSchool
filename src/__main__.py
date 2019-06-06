from sys import platform

if platform == "win32":
    from src.printout import print_image
elif platform == "linux" or platform == "linux2":
    from printout import print_image


def main():
    """
    Run print function from package
    """

    print_image()


if __name__ == '__main__':
    main()

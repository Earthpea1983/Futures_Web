import settings
import os

class Main:
    def __init__(self):
        print("Program started.")
        BASE_DIR = settings.base_dir() + "/app"
        os.system("python3 {0}/sf_crawler.py".format(BASE_DIR))
        os.system("python3 {0}/create_spot.py".format(BASE_DIR))
        os.system("python3 {0}/logic.py".format(BASE_DIR))
        os.system("python3 {0}/plot_figure.py".format(BASE_DIR))
        print("Program closed.")

if __name__ == "__main__":
    go = Main()
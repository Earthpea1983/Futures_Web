import settings
import os

class Main:
    def __init__(self):
        print("Program started.")
        BASE_DIR = settings.base_dir()
        app_dir = BASE_DIR + "\\app"
        os.system("python3 {0}\\sf_crawler.py".format(app_dir))
        os.system("python3 {0}\\create_spot.py".format(app_dir))
        os.system("python3 {0}\\logic.py".format(app_dir))
        os.system("python3 {0}\\plot_figure.py".format(app_dir))
        print("Program closed.")
        os.system("explorer {0}".format(BASE_DIR + "\\figure"))


if __name__ == "__main__":
    go = Main()
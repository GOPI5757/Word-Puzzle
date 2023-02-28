import sys
import os


def resource(abspath):
    try:
        basepath = sys._MEIPASS
    except:
        basepath = os.path.abspath('.')
    return os.path.join(basepath, abspath)

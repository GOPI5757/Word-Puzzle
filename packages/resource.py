import sys
import os


def resource(abspath):
    try:
        basepath = sys.MEI_PASS
    except:
        basepath = os.path.abspath('.')
    return os.path.join(basepath, abspath)

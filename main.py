import tkinter as tk
import logging
import unittest
from pprint import pprint

from connections import binance_futures as bf
from models import Contract

logger= logging.getLogger()


stream_handler= logging.StreamHandler()
formatter=logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logger.setLevel(logging.INFO)

stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_hadler=logging.FileHandler('info.log')
file_hadler.setFormatter(formatter)
file_hadler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_hadler)

logger.addHandler(stream_handler)


if __name__ == '__main__':
    binance_client = bf.BinanceFuturesClient("ad08cd0dca0ad5465e9b309259df0216931329d71422116937576e943c4352c0",
                                             "b233aedcb230204d811f21efecf8714d5af13b8a992f00d024270c75f871132d", True)

    root = tk.Tk()
    root.mainloop()



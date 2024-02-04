import logging

from connectors.binance_futures import BinanceFuturesClient
from connectors.bitmex import BitmexClient

from components.root_component import Root


logger = logging.getLogger()

logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


if __name__ == '__main__':

    binance = BinanceFuturesClient("ad08cd0dca0ad5465e9b309259df0216931329d71422116937576e943c4352c0",
                                                 "b233aedcb230204d811f21efecf8714d5af13b8a992f00d024270c75f871132d",
                                                 True)
    bitmex = BitmexClient("9DsUlvqgQlESbvh_uPMEAgBr", "lbExQpLSpHmGO9rJTNmh1-_PXQsqM7-5VRMgTokTj9mUq2V3", True)

    root = Root(binance, bitmex)
    root.mainloop()

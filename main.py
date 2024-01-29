import tkinter as tk
import logging
import binance_futures as bf
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

logger.info('this is logged in all cases')

if __name__ == '__main__':
    binanceContracts=bf.get_contracts()

    root = tk.Tk()
    root.title("Binance Futures Contracts")
    root.configure(bg='gray12')
    i=0
    j=0
    calibri_font = ("Calibri", 12, "bold")
    for contract in binanceContracts:
        label_widget=tk.Label(root, text=contract, borderwidth=2, relief="groove",bg='gray12',fg='white', padx=10, pady=10,font=calibri_font)
        label_widget.grid(row=i, column=j, sticky="nsew")
        if i==20:
            j+=1
            i=0
        else:
            i +=1

    root.mainloop()



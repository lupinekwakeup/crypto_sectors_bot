import ccxt
import sys
import shelve
import tkinter as tk

def show_output(output_text):
    output_box.config(state="normal")
    output_box.insert("end", output_text + "\n")
    output_box.config(state="disabled")

def submit():
    global api_key, secret_key
    api_key = api_key_entry.get()
    secret_key = secret_key_entry.get()

    db = shelve.open("bybit_keys")
    db["api_key"] = api_key
    db["secret_key"] = secret_key
    db.close()

    sector = sector_var.get()
    selected_sector = sectors[sector]
    side = side_var.get()
    money = float(money_entry.get())
    try:
        if money < 100:
            raise ValueError("Invalid input. Please type a number larger than 100.")
            show_output("Invalid input. Please type a number larger than 100.")
    except ValueError as ve:
        print(ve)
        sys.exit()

    exchange = ccxt.bybit({
        'apiKey': api_key,
        'secret': secret_key
    })

    for coin in selected_sector:
        fetch_pair = exchange.fetch_ticker(coin)
        price = fetch_pair['bid']
        money_per_coin = money / len(selected_sector)
        qty = money_per_coin / price
        try:
            exchange.create_market_order(coin, side, qty)
        except Exception as e:
            print(f"Error during order creation for {coin}: {e}")
            show_output(f"Error during order creation for {coin}: {e}")
            continue
        print(f"Bought {qty} of {coin} for {money_per_coin}$")
        show_output(f"Bought {qty} of {coin} for {money_per_coin}$")


def fetch_keys():
    db = shelve.open("bybit_keys")
    api_key = db.get("api_key", "")
    secret_key = db.get("secret_key", "")
    db.close()
    return api_key, secret_key

def logout():
    db = shelve.open("bybit_keys")
    del db["api_key"]
    del db["secret_key"]
    db.close()
    api_key_entry.delete(0, tk.END)
    secret_key_entry.delete(0, tk.END)


MetaverseGaming = ["RNDRUSDT", "TLMUSDT", "GALAUSDT", "ENJUSDT", "MANAUSDT", "ILVUSDT", "YGGUSDT", "ALICEUSDT",
                   "GALUSDT", "AXSUSDT", "SANDUSDT", "APEUSDT"]
Dinocoins = ["LTCUSDT", "NEOUSDT", "EOSUSDT", "BCHUSDT", "DASHUSDT", "DGBUSDT"]
DeFi = ["CVXUSDT", "FXSUSDT", "COMPUSDT", "1INCHUSDT", "CRVUSDT", "BALUSDT", "MKRUSDT", "YFIUSDT", "MKRUSDT", "UNIUSDT",
        "LDOUSDT", "AAVEUSDT", "RUNEUSDT", "SUSHIUSDT", "RENUSDT", "SNXUSDT"]
Layers = ["LRCUSDT", "ONEUSDT", "SOLUSDT", "FTMUSDT", "ATOMUSDT", "ADAUSDT", "AVAXUSDT", "MATICUSDT", "OPUSDT",
          "DOTUSDT", "KSMUSDT", "NEARUSDT"]
StorageOraclesInfra = ["ARUSDT", "BANDUSDT", "API3USDT", "GRTUSDT", "HNTUSDT", "LINKUSDT", "FILUSDT", "OCEANUSDT",
                       "TRBUSDT", "STORJUSDT"]
ZK = ["MINAUSDT", "DUSKUSDT", "MATICUSDT", "LRCUSDT", "IMXUSDT", "CELRUSDT"]

sectors = {
    "Metaverse & Gaming": MetaverseGaming,
    "Dinocoins": Dinocoins,
    "DeFi": DeFi,
    "Layer 1's & Layer 2's": Layers,
    "Storage, Oracles & Infrastructure": StorageOraclesInfra,
    "ZK-Rollups": ZK
}

root = tk.Tk()
root.title("Crypto Sectors")

api_key_label = tk.Label(root, text="Bybit API Key")
api_key_label.grid(row=0, column=0)
api_key, secret_key = fetch_keys()
api_key_entry = tk.Entry(root, textvariable=tk.StringVar(value=api_key))
api_key_entry.grid(row=0, column=1)

secret_key_label = tk.Label(root, text="Bybit Secret Key")
secret_key_label.grid(row=1, column=0)
secret_key_entry = tk.Entry(root, textvariable=tk.StringVar(value=secret_key), show="*")
secret_key_entry.grid(row=1, column=1)

sector_label = tk.Label(root, text="Sector")
sector_label.grid(row=2, column=0)
sector_var = tk.StringVar()
sector_var.set("Metaverse & Gaming")
sector_dropdown = tk.OptionMenu(root, sector_var, *sectors.keys())
sector_dropdown.grid(row=2, column=1)

side_label = tk.Label(root, text="Buy/Sell")
side_label.grid(row=3, column=0)
side_var = tk.StringVar()
side_var.set("buy")
side_dropdown = tk.OptionMenu(root, side_var, "buy", "sell")
side_dropdown.grid(row=3, column=1)

money_label = tk.Label(root, text="Order By Value (Only 100$+)")
money_label.grid(row=4, column=0)
money_entry = tk.Entry(root)
money_entry.grid(row=4, column=1)

logout_button = tk.Button(root, text="Logout API Keys", command=logout)
logout_button.grid(row=1, column=3)

submit_button = tk.Button(root, text="Submit Order", command=submit)
submit_button.grid(row=5, column=1)

output_box = tk.Text(root, wrap="word", state="disabled")
output_box.grid(row=6, column=1, sticky="nsew")

root.mainloop()

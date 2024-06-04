#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pygsheets
from constants import logging
from login_get_kite import get_kite
from traceback import print_exc
from pprint import pprint


def get_gsheet():
    try:
        # Load credentials from the JSON key file
        credentials = "../../wish-vishys.json"
        # Authorize the client
        gc = pygsheets.authorize(service_file=credentials)
        # Open the Google Sheet
        spreadsheet = gc.open("pappu_kumar")
        worksheet = spreadsheet.sheet1
        # Read the data from the Google Sheet
        gdata = worksheet.get_as_df()
        # use only first 5 columns drop others
        gdata = gdata.iloc[:, :8]
        return gdata
    except Exception as e:
        logging.error(f"get_gsheet: {e}")
        print_exc()


def cancel(api):
    try:
        resp = api.kite.get_gtts()
        pprint(resp)
        __import__("time").sleep(5)
        for gtt in resp:
            if gtt["status"] == "active":
                logging.debug(f'ancelling {gtt["condition"]["tradingsymbol"]}')
                resp = api.kite.delete_gtt(gtt["id"])
                logging.debug(resp)
    except Exception as e:
        logging.error(f"cancel: {e}")
        print_exc()


def place(api, df):
    lst = []
    if len(df.index) > 0:
        lst = df.to_dict("records")
        if len(lst) > 0:
            for dct in lst:
                """
                    {'Instrument': 'NSE:ABCAPITAL', 'SL-Qty': 352, 'SL-Trigger': 224.5, 'SL-Price': 224, 'Exit_Qty': 176, 'Exit_Price': 178}
                """
                exchsym = dct["Instrument"]
                args = dict(
                    trigger_type=api.kite.GTT_TYPE_OCO,
                    tradingsymbol=exchsym.split(":")[1],
                    exchange=exchsym.split(":")[0],
                    trigger_values=[dct["SL-Trigger"], dct["Exit_Trigger"]],
                    last_price=api.kite.ltp(exchsym)[exchsym]["last_price"],
                    orders=[
                        {
                            "exchange": exchsym.split(":")[0],
                            "tradingsymbol": exchsym.split(":")[1],
                            "transaction_type": "SELL",
                            "quantity": dct["SL-Qty"],
                            "order_type": "LIMIT",
                            "product": "CNC",
                            "price": dct["SL-Price"],
                        },
                        {
                            "exchange": exchsym.split(":")[0],
                            "tradingsymbol": exchsym.split(":")[1],
                            "transaction_type": "SELL",
                            "quantity": dct["Exit_Qty"],
                            "order_type": "LIMIT",
                            "product": "CNC",
                            "price": dct["Exit_Price"],
                        },
                    ],
                )
                try:
                    resp = api.kite.place_gtt(**args)
                    logging.debug(resp)
                    __import__("time").sleep(1)
                except Exception as e:
                    logging.error(f"place: {e} {exchsym.split(':')[1]}")
                    print_exc()


def main():
    api = get_kite()
    cancel(api)
    gdata = get_gsheet()
    place(api, gdata)


main()
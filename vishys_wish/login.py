from constants import logging, O_CNFG, O_FUTL, S_DATA


def get_kite():
    if O_CNFG.get("broker", "") == "bypass":
        logging.debug("trying login BYPASS ..")
        kite = _get_bypass()
    else:
        print("trying login ZERODHA ..")
        kite = _get_zerodha()
    return kite


def _get_bypass():
    try:
        from omspy_brokers.bypass import Bypass

        dct = O_CNFG["bypass"]
        tokpath = S_DATA + dct["userid"] + ".txt"
        enctoken = None
        if not O_FUTL.is_file_not_2day(tokpath):
            print(f"{tokpath} modified today ... reading {enctoken}")
            with open(tokpath, "r") as tf:
                enctoken = tf.read()
                if len(enctoken) < 5:
                    enctoken = None
        print(f"enctoken to broker {enctoken}")
        bypass = Bypass(dct["userid"], dct["password"], dct["totp"], tokpath, enctoken)
        if bypass.authenticate():
            if not enctoken:
                enctoken = bypass.kite.enctoken
                with open(tokpath, "w") as tw:
                    tw.write(enctoken)
    except Exception as e:
        print(f"unable to create bypass object {e}")
    else:
        return bypass


def _get_zerodha():
    try:
        from omspy_brokers.zerodha import Zerodha

        dct = O_CNFG["zerodha"]
        zera = Zerodha(
            userid=dct["userid"],
            password=dct["password"],
            totp=dct["totp"],
            api_key=dct["api_key"],
            secret=dct["secret"],
        )
        return zera
    except Exception as e:
        print(f"exception while creating zerodha object {e}")


def set_session(zera, userid):
    try:
        tokpath = S_DATA + userid + ".txt"
        with open(tokpath, "r") as tf:
            enctoken = tf.read()
            if len(enctoken) > 5:
                zera.kite.set_access_token(enctoken)
                return zera
    except Exception as e:
        logging.error(f"set_session: {e}")


def write_token(zera, userid):
    try:
        tokpath = S_DATA + userid + ".txt"
        if zera.authenticate():
            with open(tokpath, "w") as tw:
                tw.write(zera.enctoken)
    except Exception as e:
        logging.error(f"write_token: {e}")


if __name__ == "__main__":
    zera = get_kite()
    # write_token(zera, O_CNFG["zerodha"]["userid"])
    zera = set_session(zera, O_CNFG["zerodha"]["userid"])
    print(zera.profile)

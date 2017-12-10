import callr
HIST="https://devakademi.sahibinden.com/history"
TICK="https://devakademi.sahibinden.com/ticker"

api = callr.Api("marmarauniversity_1", "212427123")

description = """
    dev.akademi predictor scoin
    Usage: python predict.py  [OPTION] values
    Eg: python3 predict.py -d 10
    Eg: python3 predict.py -ds 5
"""
description2 = """
    dev.akademi bot sell ant buy scoin
    Usage: python bot.py  [OPTION] values
    Eg: python3 predict.py -s 10000 -n +905346639019
    Eg: python3 predict.py -b 11000 -n +905346639019
"""
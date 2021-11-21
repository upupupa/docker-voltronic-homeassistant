from .core import *


def parse_data(raw_data: str):
    if not isinstance(eval(raw_data), dict):
        raise TypeError

    operating_data: dict = eval(raw_data)
    battery_data = (
            x for x in operating_data.keys() 
            if x.startswith('Battery') or x.startswith('Max')
            )
    return battery_data

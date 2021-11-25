from inverter.core import *


def parse_data(raw_data: str):
    if not isinstance(eval(raw_data), dict):
        raise TypeError

    operating_data: dict = eval(raw_data)
    battery = parse_battery(operating_data)
    print(battery.__dict__)
    inverter = parse_inverter(operating_data)
    print(inverter.__dict__)
    ac = parse_ac(operating_data)
    print(ac.__dict__)
    pv = parse_pv(operating_data)
    print(pv.__dict__)
    return battery, inverter, ac, pv

def parse_battery(data_json: dict) -> Battery:
    battery = Battery(
            capacity=data_json['Battery_capacity'],
            voltage=data_json['Battery_voltage'],
            charge_current=data_json['Battery_charge_current'],
            discharge_current=data_json['Battery_discharge_current'],
            recharge_voltage=data_json['Battery_discharge_current'],
            under_voltage=data_json['Battery_discharge_current'],
            bulk_voltage=data_json['Battery_discharge_current'],
            float_voltage=data_json['Battery_float_voltage'],
            redischarge_voltage=data_json['Battery_redischarge_voltage'],
            max_charge_current=data_json['Max_charge_current'],
            max_grid_charge_current=data_json['Max_grid_charge_current']
            )
    return battery

def parse_inverter(data_json: dict) -> Inverter:
    inverter = Inverter(
            heatsink_temperature=data_json['Heatsink_temperature'],
            bus_voltage=data_json['Bus_voltage'],
            load_percent=data_json['Load_pct'],
            load_status_on=data_json['Load_status_on'],
            load_va=data_json['Load_status_on'],
            load_watt=data_json['Load_watt'],
            load_watthour=data_json['Load_watthour'],
            out_source_priority=data_json['Out_source_priority'],
            charge_priority=data_json['Charger_source_priority'],
            mode=data_json['Inverter_mode']
            )
    return inverter

def parse_ac(data_json: dict) -> AC:
    ac = AC(
        charge_on=data_json['AC_charge_on'],
        grid_frequency=data_json['AC_grid_frequency'],
        grid_voltage=data_json['AC_grid_voltage'],
        out_frequency=data_json['AC_out_frequency'],
        out_voltage=data_json['AC_out_voltage'],
        )
    return ac

def parse_pv(data_json: dict) -> PV:
    pv = PV(
        current=data_json['PV_in_current'],
        voltage=data_json['PV_in_voltage'],
        watthour=data_json['PV_in_watthour'],
        watt=data_json['PV_in_watts'],
        )
    return pv


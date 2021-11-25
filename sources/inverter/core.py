

class Device:
    def __init__(
            self, name: str, manufacturer: str, 
            firmware_version: str, serial_number: str,
            model: str) -> None:

        self.name = name
        self.mf = manufacturer
        self.sw = serial_number
        self.ids = firmware_version
        self.mdl = model


class Battery:
    def __init__(
            self, bulk_voltage: float, capacity: int, charge_current: int,
            discharge_current: int, float_voltage: float, recharge_voltage: float,
            redischarge_voltage: float, under_voltage: float, voltage: float,
            max_charge_current: int, max_grid_charge_current: int) -> None:

        self.capacity = (capacity, '%', 'battery-outline')
        self.voltage = (voltage, 'V', 'battery-outline')
        self.charge_current = (charge_current, 'A', 'current-dc')
        self.discharge_current = (discharge_current, 'A', 'current-dc')
        self.recharge_voltage = (recharge_voltage, 'V', 'current-dc')
        self.under_voltage = (under_voltage, 'V', 'current-dc')
        self.bulk_voltage = (bulk_voltage, 'V', 'current-dc')
        self.float_voltage = (float_voltage, 'V', 'current-dc') 
        self.redischarge_voltage = (redischarge_voltage, 'V', 'battery-negative')
        self.max_charge_current = (max_charge_current, 'A', 'current-dc')
        self.max_grid_charge_current = (max_grid_charge_current, 'A', 'current-dc')
    

class AC:
    def __init__(
            self, charge_on: bool , grid_frequency: float, grid_voltage: float,
            out_frequency: float, out_voltage: float) -> None:
        
        self.charge_on = (charge_on, '', 'power')
        self.grid_frequency = (grid_frequency, 'Hz', 'current-ac')
        self.grid_voltage = (grid_voltage, 'V', 'power-plug')
        self.out_frequency = (out_frequency, 'Hz', 'current-ac')
        self.out_voltage = (out_voltage, 'V', 'power-plug')


class PV:
    def __init__(
            self, current: float, voltage: float,          
            watthour: float, watt: float) -> None:

        self.current = (current, 'A', 'solar-panel-large')
        self.voltage = (voltage, 'V', 'solar-panel-large')
        self.watthour = (watthour, 'Wh', 'solar-panel-large', 'energy')
        self.watt = (watt, 'W', 'solar-panel-large')


class Inverter:
    def __init__(
            self, heatsink_temperature: int, bus_voltage: float,
            load_percent: int, load_status_on: int, load_va: int, load_watt: int,
            load_watthour: float, out_source_priority: int, 
            charge_priority: int, mode: int) -> None:

        self.heatsink_temperature = (heatsink_temperature, '°C', 'details')
        self.bus_voltage = (bus_voltage, 'V', 'details')
        self.load_percent = (load_percent, '%', 'brightness-percent')
        self.load_status_on = (load_status_on, '', 'power')
        self.load_va = (load_va, 'VA', 'chart-bell-curve')
        self.load_watt = (load_watt, 'W', 'chart-bell-curve')
        self.load_watthour = (load_watthour, 'Wh', 'chart-bell-curve', 'energy')
        self.out_source_priority = (out_source_priority, '', 'grid')
        self.charger_source_priority = (charge_priority, '', 'solar-power') 
        self.inverter_mode = (mode, 'solar-power')


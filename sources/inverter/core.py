

class Device:
    def __init__(
            self, name: str, manufacturer: str, 
            firmware_version: str, serial_number: str,
            model: str) -> None:

        self.name = name
        self.manufacturer = manufacturer
        self.firmware_version = firmware_version
        self.serial_number = serial_number
        self.model = model
    
    def get_all_data(self) -> tuple[str]:
        reutrn self.name, self.manufacturer, self.firmware_version,\
                self.serial_number, self.model

class Battery:
    def __init__(
            self, bulk_voltage: float, capacity: int, charge_current: int,
            discharge_current: int, float_voltage: float, recharge_voltage: float,
            redischarge_voltage: float, under_voltage: float, voltage: float,
            max_charge_current: int, max_grid_charge_current: int) -> None:

        self.capacity = capacity
        self.voltage = voltage
        self.charge_current = charge_current
        self.discharge_current = discharge_current
        self.recharge_voltage = recharge_voltage
        self.under_voltage = under_voltage
        self.bulk_voltage = bulk_voltage
        self.float_voltage = float_voltage 
        self.redischarge_voltage = redischarge_voltage
        self.max_charge_current = max_charge_current
        self.max_grid_charge_current = max_grid_charge_current
    

class AC:
    def __init__(
            self, charge_on: bool , grid_frequency: float, grid_voltage: float,
            out_frequency: float, out_voltage: float) -> None:
        
        self.charge_on = charge_on
        self.grid_frequency = grid_frequency
        self.grid_voltage = grid_voltage
        self.out_frequency = out_frequency
        self.out_voltage = out_voltage


class PV:
    def __init__(
            self, current: float, voltage: float,          
            watthour: float, watt: float) -> None:

        self.current = current
        self.voltage = voltage
        self.watthour = watthour
        self.watt = watt


class Inverter:
    def __init__(
            self, heatsink_temperature: int, bus_voltage: float,
            load_percent: int, out_source_priority: int, 
            charge_priority: int, mode: int) -> None:

        self.heatsink_temperature = heatsink_temperature
        self.bus_voltage = bus_voltage
        self.load_percent = load_percent
        self.out_source_priority = out_source_priority
        self.charge_priority = charge_priority
        self.mode = mode


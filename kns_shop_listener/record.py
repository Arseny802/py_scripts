from datetime import datetime
from enum import Enum

from common.log import get_logger


def log():
    return get_logger('record', 'kns_shop_listener')


class ComputerComponents(Enum):
    Motherboard = "Motherboard"
    VideoCard = "Video card"
    Processor = "Processor"
    RAM1 = "RAM 1"
    RAM2 = "RAM 2"
    ROM1 = "ROM 1"
    ROM2 = "ROM 2"
    Cooler = "Cooler"
    PowerBlock = "Power block"
    Corpus = "Corpus"
    Monitor1 = "Monitor 1"
    Monitor2 = "Monitor 2"
    Monitor3 = "Monitor 3"
    AudioSystem = "Audio system"
    AudioCard = "Audio card"


class Record:
    def __init__(self):
        self.components = dict()
        self.total_price = 0
        for component in ComputerComponents:
            self.components[component.name] = 0

    def add(self, key: ComputerComponents, price):
        self.components[key.name] = price
        self.total_price += price

    def get_total(self):
        return self.total_price

    def equal(self, other: 'Record'):
        if self.total_price != other.total_price:
            log().debug(f"Record '{self.to_string()}' and other record '{other.to_string()}' "
                        f"have different total prices ({self.total_price} != {other.total_price})")
            # ignoring that because different items prices may be similar

        for component_name, component_value in self.components.items():
            if other.components[component_name] != component_value:
                log().debug(f"Record '{self.to_string()}' and other record '{other.to_string()}' "
                            f"have different prices ({component_value} != {other.components[component_name]}) "
                            f"on {component_name}")
                return False

        log().debug(f"Record '{self.to_string()}' and other record '{other.to_string()}' are equal")
        return True

    def to_string(self):
        result = ""

        for component in ComputerComponents:
            result += str(self.components[component.name])
            result += ';'
        result += str(self.total_price) + ';'
        result += str(datetime.now())

        return result

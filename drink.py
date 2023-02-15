from dataclasses import dataclass, asdict, fields
from filter import CustomFilter

@dataclass
class Drink:
    name: str
    price: tuple  # (Kr, Cent)
    perc: float
    quantity: int # Millis
    type: str
    info: str

    def dict(self):
        return asdict(self)

    def from_dict(args):
        fieldSet = {f.name for f in fields(Drink) if f.init}
        filteredArgDict = {k : v for k, v in args.items() if k in fieldSet}
        return Drink(**filteredArgDict)

    def dummyPerc(perc):
        return Drink(name="", price=(0, 0), perc=perc, quantity=0, type="", info="")

    def id(self, extra=""):
        return self.name + "-" + id(self).to_bytes(6, "big").hex()
                                                                
    
    def getPrice(self):
        return self.price[0] + self.price[1] / 100
    
    def __str__(self):
        return f"{self.name:<33} {self.type:<40} {self.perc:>5} % {self.quantity:>5} ml {self.price[0] + self.price[1]/100:>5} SEK"

    def __repr__(self):
        return str(self)

    def ratio(self):
        if (self.quantity == 0):
            return 999999999999
        return (self.price[1] + 100 * (self.price[0])) / (self.perc * self.quantity)
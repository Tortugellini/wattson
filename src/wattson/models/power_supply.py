from pathlib import Path
from pydantic import BaseModel, Field, field_validator


class Battery(BaseModel, extra="allow"):
    """An object that holds information about the system battery."""

    information_location: str | Path = Field(..., description="The directory with the power supplies of the system.")
    battery_name: str = Field(..., description="The name of the battery to investigate.")
    properties: str | list = Field(..., description="The properties to grab from 'information_location'.")
    
    @field_validator("information_location", mode="before")
    @classmethod
    def _check_location(cls, il: str | Path) -> Path:
        """
        An internal method for ensuring that the location provided exists.
        ---
        Parameters:
            il, str | Path: The location of the power supply information passed to 'BaseModel'.
        """

        if Path(il).exists():
            return Path(il) # Guarantees that "information_location" is a Path object.
        else:
            raise FileNotFoundError("The provided location does not exist.")

    @field_validator("battery_name", mode="before")
    @classmethod
    def _check_battery_name(cls, bn: str) -> str:
        """
        Checks that the battery name provided is a battery on the system.
        ---
        Parameters:
            bn, str: The name of the battery on the system to check.
        """

        # Establishing the expected prefix of the battery filename.
        prefix = "BAT"

        if prefix in bn and isinstance(int(bn.strip(prefix)), int):
            return bn
        else:
            raise ValueError(f"The battery must be '{prefix}' followed by an integer.")

    @field_validator("properties", mode="before")
    @classmethod
    def _check_properties_format(cls, p: str | list) -> list:
        """
        Checks that the properties variable is the right format for both the str
        and list formats.
        ---
        Parameters:
            p, str | list: The desired properties of the battery.
        """

        if isinstance(p, str):
            _p = p.split(", ")
            if len(_p) == 1:
                return _p
            elif "" in _p:
                return list(filter(lambda _: _ != "", _p))
            elif _p[0] == p:
                raise ValueError("The properties must be separated by commas.")
        
        elif isinstance(p, list):
            if not all(list(map(lambda _: isinstance(_, str), p))):
                raise ValueError("The properties must by strings.")
            return p

    def model_post_init(self, _):
        """
        An initialization function that is run after all Pydantic checks above pass.
        
        Instantiates a 'Battery' object with attributes that are listed in 'properties'.
        """
        
        # Attaching all the properties as attributes of 'Battery'.
        for property in self.properties:
            with open(self.information_location / self.battery_name / property, "r") as f:
                content = f.readlines()
                setattr(self, property, content[0].strip("\n"))

    
if __name__ == "__main__":
    battery = Battery(
        information_location="/sys/class/power_supply",
        battery_name="BAT0",
        properties=["serial_number", ""]
    )

    print(battery.model_extra)

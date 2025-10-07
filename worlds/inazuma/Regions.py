from BaseClasses import Region
from .Types import InazumaLocation
from .Locations import location_table, is_valid_location
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import InazumaWorld

# This is where you will create your imaginary game world
# IE: connect rooms and areas together
# This is NOT where you'll add requirements for how to get to certain locations thats in Rules.py
# This is also long and tediouos
def create_regions(world: "InazumaWorld"):
    # The functions that are being used here will be located at the bottom to view
    # The important part is that if its not a dead end and connects to another place then name it
    # Otherwise you can just create the connection. Not that naming it is bad

    # You can technically name your connections whatever you want as well
    # You'll use those connection names in Rules.py
    menu = create_region(world, "Menu")
    prologue = create_region_and_connect(world, "Prologue", "Menu -> Prologue", menu)
    overworld = create_region_and_connect(world, "overworld", "Menu -> overworld", menu)
    match = create_region_and_connect(world, "match", "Menu -> match", menu)

    # ---------------------------------- Prologue ----------------------------------
    prologue = create_region_and_connect(world, "Prologue", prologue)

    # ---------------------------------- Overworld ------------------------------------------
    raimon_high = create_region_and_connect(world, "Raimon High", "overworld -> Raimon High", overworld)
    match = create_region_and_connect(world, "match", "overworld -> match", overworld)
    raimon_high.connect(raimon_high, "overworld -> Raimon High")
    match.connect(match, "overworld -> match")

def create_region(world: "InazumaWorld", name: str) -> Region:
    reg = Region(name, world.player, world.multiworld)

    # When we create the region we go through all the locations we made and check if they are in that region
    # If they are and are valid, we attach it to the region
    for (key, data) in location_table.items():
        if data.region == name:
            if not is_valid_location(world, key):
                continue
            location = InazumaLocation(world.player, key, data.ap_code, reg)
            reg.locations.append(location)
    
    world.multiworld.regions.append(reg)
    return reg

# This runs the create region function while also connecting to another region
# Just simplifies process since you woill be connecting a lot of regions
def create_region_and_connect(world: "InazumaWorld",
                               name: str, entrancename: str, connected_region: Region) -> Region:
    reg: Region = create_region(world, name)
    connected_region.connect(reg, entrancename)
    return reg
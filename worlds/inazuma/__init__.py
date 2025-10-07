
import logging
import settings
import typing
from BaseClasses import MultiWorld, Item, Tutorial
from worlds.AutoWorld import World, CollectionState, WebWorld
from typing import Dict

from .Locations import get_location_names, get_total_locations
from .Items import create_item, create_itempool, item_table
from .Options import InazumaOptions
from .Regions import create_regions
from .Types import ChapterType, chapter_type_to_name
class InazumaWeb(WebWorld):
    theme = "Party"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Inazuma Eleven 2 for Archipelago. "
        "English",
        "setup_en.md",
        "setup/en",
        ["1theory"]
    )]
class InazumaWorld(World):
    """
    Inazuma Eleven is a soccer-RPG.
    """
    game = "Inazuma Eleven 2"
    item_name_to_id = {name: data.ap_code for name, data in item_table.items()}
    location_name_to_id = get_location_names()
    options_dataclass = InazumaOptions
    options = InazumaOptions
    web = InazumaWeb()

    # There are other built in variables for AP. You can look at other worlds to see your options
    # Like PLEASE look at the various worlds. Its so helpful. Find one you like and you can duplicate a bunch of it

    # This is where you put stuff that need to be done RIGHT away. Typically you can just leave it alone but it can be useful to pop some things here as needed
    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

    # Generate early you do things just before the generation
    # Super important for doing things like adjusting the item pool based on options and the like
    # Can technically be skipped if you dont need to do anything or if you handle it elsewhere like a short hike
    #def generate_early(self):
        # I highly recommend looking at other apworlds init files to see some examples
        # sly1 (hey i did that), ahit, and bomb rush cyberfunk are some good ones

        # Push precollected is how you give your player items they need to start with
        # This is for options though. Dont worry about the starting inventory option thats in all yamls
        # AP handles that one
    #    self.multiworld.push_precollected(self.create_item())

    # Regions are the different locations in your world. So like Undead Burgh in dark souls or Pacifilog Town in pokemon
    # They dont have to match your game, they can be whatever you need them to be for organization
    def create_regions(self):
        # This function comes from your Regions.py and dont worry that it matches the function that its in
        create_regions(self)

        # You can also use this space to do other location creation activities
        # Like if an option is enabled to add extra locations
        # Or the opposite, whatever it is. Just be careful that you arent duplicating locations

    # These are some examples of creating items. The create_itempool(self) function is coming from Items.py in this instance
    # The important part is that the items get into the self.multiworld.itempool as a list of Items
    # Ill try to explain better in the Items.py file 
    def create_items(self):
        self.multiworld.itempool += create_itempool(self)

    # This is just a helper function for turning names into Items. You could do some other stuff here as well
    # ahit does similar if you want another look and bomb rush cyberfunk does it in a slightly different way by turning it into a specific item for that game
    # Again hopefully I do a better job of explaining the Items.py file
    def create_item(self, name: str) -> Item:
        return create_item(self, name)
    
    # The slot data is what youre sending to the AP server kinda. You dont have to add all your options. Really you want the ones you think a pop tracker would use
    # Seed, Slot, and TotalLocations are all super important for AP though, you need those
    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {
            "options": {
                "ExtraLocations":           self.options.ExtraLocations.value,
                "TrapChance":               self.options.TrapChance.value,
                "RayDarkTrapWeight":       self.options.RayDarkTrapWeight.value
            },
            "Seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "Slot": self.multiworld.player_name[self.player],  # to connect to server
            "TotalLocations": get_total_locations(self) # get_total_locations(self) comes from Locations.py
        }

        return slot_data
    
    # These are used by AP to add and remove items from the player. You can probably just leave them alone
    def collect(self, state: "CollectionState", item: "Item") -> bool:
        return super().collect(state, item)
    
    def remove(self, state: "CollectionState", item: "Item") -> bool:
        return super().remove(state, item)
from typing import List, Dict, Any
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Choice, OptionGroup, Toggle, Range

# If youve ever gone to an options page and seen how sometimes options are grouped
# This is that
def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in inazuma_option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list

class ExtraLocations(Toggle):
    """
    This will enable the extra locations option. Toggle is just true or false.
    """
    display_name = "Add Extra Locations"

class TrapChance(Range):
    """
    Determines the chance for any junk item to become a trap.
    Set it to 0 for no traps.
    Range is in fact a range. You can set the limits and its default.
    """
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 0

class RayDarkTrapWeight(Range):
    """
    The weight of forcefem traps in the trap pool.
    Does really cool stuff to your body.
    """
    display_name = "RayDark Trap Weight"
    range_start = 0
    range_end = 100
    default = 100


@dataclass
class InazumaOptions(PerGameCommonOptions):
    ExtraLocations:             ExtraLocations
    TrapChance:                 TrapChance
    RayDarkTrapWeight:         RayDarkTrapWeight

# This is where you organize your options
# Its entirely up to you how you want to organize it
inazuma_option_groups: Dict[str, List[Any]] = {
    "General Options": [ExtraLocations],
    "Trap Options": [TrapChance, RayDarkTrapWeight]
}
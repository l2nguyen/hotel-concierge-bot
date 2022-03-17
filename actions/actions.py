from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

def split_room_number(rnumber):
    """ splits the room number to check it's a valid one"""
    # simple check for now
    # improve to add occupancy
    padded_number = rnumber.zfill(4)
    valid_number = rnumber.isdigit()
    if len(padded_number)==4 and valid_number:
        # probably should add a try
        rn_list = [int(padded_number[:2]), int(padded_number[2:])]
        return rn_list
    else:
        return None

def check_valid_room(floor, room):
    valid_floor = (1 <= floor <= 10)
    valid_room = (1 <= room <= 20)

    valid_room = (valid_floor & valid_room)

    return valid_room

class ValidateItemRequestForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_item_request_form"

    def validate_room_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate room number value."""
        
        room_number_list = split_room_number(slot_value)

        if room_number_list is not None:
            floor_num, room_num = room_number_list
            room_is_valid = check_valid_room(floor_num, room_num)
        else:
            room_is_valid = False

        if room_is_valid:
            return {"room_number": slot_value}
        else:
            dispatcher.utter_message(text="I think there is a typo somewhere. That's not a room in this hotel.")
            return {"room_number": None}
        
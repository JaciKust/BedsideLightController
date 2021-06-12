from datetime import timedelta

from Constants import Relay as RelayConstant
from Interactable.Relay import Relay
from Interactable.RemoteRelay import RemoteRelay

ODDISH_RELAY = Relay(RelayConstant.ODDISH_ID, RelayConstant.ODDISH_PIN, timedelta(hours=12))

SOUND_SYSTEM_RELAY = RemoteRelay(RelayConstant.SOUND_SYSTEM_ID, RelayConstant.SOUND_SYSTEM_PIN)

POWER_RELAY = RemoteRelay(RelayConstant.POWER_PIN_ID, RelayConstant.POWER_PIN)

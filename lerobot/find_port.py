# Copyright 2024 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Helper to find the USB port associated with your MotorsBus.

Example:

```shell
python -m lerobot.find_port
```
"""

import time


def find_available_ports():
    from serial.tools import list_ports  # Part of pyserial library

    # ``list_ports`` already handles the platform specific logic and, unlike
    # globbing ``/dev`` on Unix, only returns the ports that are actually
    # accessible.  This prevents us from collecting a long list of static
    # ``/dev/ttyS*`` entries, which previously meant that disconnecting the
    # MotorsBus did not change the list and the port could not be detected.
    return [port.device for port in list_ports.comports()]


def find_port():
    print("Finding all available ports for the MotorsBus.")
    ports_before = find_available_ports()
    print("Ports before disconnecting:", ports_before)

    print("Remove the USB cable from your MotorsBus and press Enter when done.")
    input()  # Wait for user to disconnect the device

    time.sleep(0.5)  # Allow some time for port to be released
    ports_after = find_available_ports()
    ports_diff = list(set(ports_before) - set(ports_after))

    if len(ports_diff) == 1:
        port = ports_diff[0]
        print(f"The port of this MotorsBus is '{port}'")
        print("Reconnect the USB cable.")
    elif len(ports_diff) == 0:
        raise OSError(f"Could not detect the port. No difference was found ({ports_diff}).")
    else:
        raise OSError(f"Could not detect the port. More than one port was found ({ports_diff}).")


if __name__ == "__main__":
    find_port()

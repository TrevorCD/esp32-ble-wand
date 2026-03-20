# Host side application for magic wand communications
# written to Python 3.14.3 specifications
#
#-------------------------------------------------------------------------------
#
#   Copyright 2026 Trevor B. Calderwood
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#-------------------------------------------------------------------------------

import asyncio
import os
import bleak    # bluetooth lib
import shutil   # shell utilities
import signal   # signal catching
import curses   # terminal printing

# Globals ----------------------------------------------------------------------

# Classes ----------------------------------------------------------------------

class Style:
    RED    = '\033[31m'
    GREEN  = '\033[32m'
    YELLOW = '\033[33m'
    BLUE   = '\033[34m'
    PURPLE = '\033[35m'
    CYAN   = '\033[36m'
    
    BOLD   = '\033[1m'
    RESET  = '\033[0m'
    
    RED_BOLD    = '\033[1;31m'
    GREEN_BOLD  = '\033[1;32m'
    YELLOW_BOLD = '\033[1;33m'
    BLUE_BOLD   = '\033[1;34m'
    PURPLE_BOLD = '\033[1;35m'
    CYAN_BOLD   = '\033[1;36m'

# Helper functions -------------------------------------------------------------

async def bluetooth_connect() -> BleakClient:
    
    # find bluetooth device
    print(f"{Style.BOLD}Bluetooth devices available:\n{Style.RESET}")
    devices = await bleak.BleakScanner.discover()
    i = 0
    for d in devices:
        print(f"{Style.BOLD}{i}: {Style.RESET}{d.address}: {Style.BOLD}{d.name}{Style.RESET}")
        i += 1
        
    if i == 0:
        print(f"{Style.RED_BOLD}Failed to find any bluetooth devices{Style.RESET}")
        return None
    
    # select bluetooth device
    print(f"\n{Style.BOLD}Enter number to select device{Style.RESET}")
    selection = -1
    while True:
        try:
            selection = int(input())
            assert (selection < i) and (selection > -1)
            print(f"{Style.GREEN_BOLD}Selected device {selection}: {devices[selection]}{Style.RESET}")
            break;
        except ValueError:
            print(f"{Style.RED_BOLD}Invalid input. Enter a number{Style.RESET}")
        except AssertionError:
            print(f"{Style.RED_BOLD}Enter a number that corresponds to a device{Style.RESET}")

    # connect to bluetooth device
    client = bleak.BleakClient(devices[selection].address)
    try:
        await client.connect()
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print(f"Model Number: {model_number.decode()}")
    except Exception:
        print(f"{Style.RED_BOLD}Failed to connect to bluetooth device{Style.RESET}")
        return None

    print(f"{Style.BLUE_BOLD}Bluetooth device connected{Style.RESET}")
    return devices[selection]

# Main -------------------------------------------------------------------------

async def main():

    stdscr = None
    client = None
    
    def resize_handler(signum, frame):
        size = shutil.get_terminal_size()
        curses.resizeterm(size.lines, size.columns)
        stdscr.refresh()

    signal.signal(signal.SIGWINCH, resize_handler)

    def sigint_handler(signum, frame):
        if stdscr != None:
            curses.nocbreak()
            stdscr.keypad(False)
            #stdscr.nodelay(False)
            curses.echo()
            curses.endwin()
        if client != None:
            client.disconnect()
        exit()

    signal.signal(signal.SIGINT, sigint_handler)
    
    def keypress_q():
        curses.nocbreak()
        stdscr.keypad(False)
        #stdscr.nodelay(False)
        curses.echo()
        curses.endwin()
        client.disconnect()
        exit()

    
    client = await bluetooth_connect()
    if client == None:
        exit()
    
    # before starting curses, prompt for any key
    print(f"{Style.BOLD}Press enter to start magic drawing board{Style.RESET}")
    input()
            
    # curses setup
    stdscr = curses.initscr()
    curses.noecho() # turns off automatic echoing of keys to screen
    curses.cbreak()
    stdscr.nodelay(True) # makes getch() non-blocking
    stdscr.keypad(True)
        
    # loop for catching bluetooth communication and updating screen
    while(True):
        # bluetooth comm

        # update screen
        stdscr.addstr(0, 0, str(curses.LINES))
        stdscr.addstr(1, 0, str(curses.COLS))
        stdscr.refresh()

        key = stdscr.getch()
        match key:
            case 113: # 'q'
                keypress_q()
                

asyncio.run(main())

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
import struct
import time

# Globals ----------------------------------------------------------------------
stdscr = None
client = None

# Classes ----------------------------------------------------------------------

class Style:
    RED    = '\033[31m'
    GRE  = '\033[32m'
    YEL = '\033[33m'
    BLU   = '\033[34m'
    PUR = '\033[35m'
    CYA   = '\033[36m'
    
    BLD   = '\033[1m'
    RST  = '\033[0m'
    
    RED_BLD    = '\033[1;31m'
    GRE_BLD  = '\033[1;32m'
    YEL_BLD = '\033[1;33m'
    BLU_BLD   = '\033[1;34m'
    PUR_BLD = '\033[1;35m'
    CYA_BLD   = '\033[1;36m'

# Helper functions -------------------------------------------------------------

async def bluetooth_connect() -> BleakClient:
    
    # find bluetooth device
    print(f"{Style.BLD}Bluetooth devices available:\n{Style.RST}")
    devices = await bleak.BleakScanner.discover()
    i = 0
    for d in devices:
        print(f"{Style.BLD}{i}: {Style.RST}"
              f"{d.address}: {Style.BLD}{d.name}{Style.RST}")
        i += 1
        
    if i == 0:
        print(f"{Style.RED_BLD}Failed to find any bluetooth devices{Style.RST}")
        return None
    
    # select bluetooth device
    print(f"\n{Style.BLD}Enter number to select device{Style.RST}")
    selection = -1
    while True:
        try:
            selection = int(input())
            assert (selection < i) and (selection > -1)
            print(f"{Style.GRE_BLD}Selected device {selection}: "
                  f"{devices[selection]}{Style.RST}")
            break;
        except ValueError:
            print(f"{Style.RED_BLD}Invalid input. Enter a number{Style.RST}")
        except AssertionError:
            print(f"{Style.RED_BLD}Enter a number that corresponds to a device"
                  f"{Style.RST}")

    # connect to bluetooth device
    client = bleak.BleakClient(devices[selection].address)
    try:
        await client.connect()
    except Exception:
        print(f"{Style.RED_BLD}Failed to connect to bluetooth device"
              f"{Style.RST}")
        return None

    print(f"{Style.BLU_BLD}Bluetooth device connected{Style.RST}")
    return client

# Main -------------------------------------------------------------------------

async def main():

    global stdscr, client

    cursor_char = 'O'
    midpoint_char = '•' # bullet 0d149
    
    shutdown = False # main loop catches this and exits with ble_cleanup_exit()

    x = None
    y = None
    z = None
    
    size = shutil.get_terminal_size()
    midpoint_x = float(size.columns / 2)
    midpoint_y = float(size.lines / 2)
    max_x = size.columns - 2
    max_y = size.lines - 1
    cursor_x = None
    cursor_y = None
    old_cursor_x = None
    old_cursor_y = None

    time_ms = 0
    
    # restores window to default state and disconnects BLE client if connected
    async def ble_cleanup_exit():
        await client.disconnect()
        if stdscr != None:
            curses.nocbreak()
            stdscr.keypad(False)
            #stdscr.nodelay(False)
            curses.echo()
            curses.endwin()
        exit()
    
    def resize_handler(signum, frame):
        nonlocal size, midpoint_x, midpoint_y, max_x, max_y
        size = shutil.get_terminal_size()
        midpoint_x = float(size.columns / 2)
        midpoint_y = float(size.lines / 2)
        max_x = size.columns - 2
        max_y = size.lines - 1
        curses.resizeterm(size.lines, size.columns)
        stdscr.refresh()

    def sigint_handler(signum, frame):
        nonlocal shutdown
        shutdown = True
        if client == None:
            exit()
    
    def ble_notification_handler(sender, data):
        nonlocal x, y, z
        nonlocal old_cursor_x, old_cursor_y, cursor_x, cursor_y
        nonlocal time_ms
        x, y, z = struct.unpack('fff', data)  # 'fff' = 3 floats
        # update cursor
        old_cursor_x = cursor_x
        old_cursor_y = cursor_y
        cursor_x -= (z * 0.01)
        cursor_y -= (x * 0.005)
        # bounds check on cursor
        if cursor_x < 0:
            cursor_x = 0
        if cursor_x > max_x:
            cursor_x = max_x
        if cursor_y < 0:
            cursor_y = 0;
        if cursor_y > max_y:
            cursor_y = max_y
        # update time
        new_time_ms = time.time_ns() // 1_000_000
        diff_time_ms = new_time_ms - time_ms
        time_ms = new_time_ms
        # update screen
        stdscr.addstr(0, 0, "          ")
        stdscr.addstr(0, 0, str(diff_time_ms))
        stdscr.addch(int(old_cursor_y), int(old_cursor_x), ' ')
        stdscr.addch(int(midpoint_y), int(midpoint_x), midpoint_char)
        stdscr.addch(int(cursor_y), int(cursor_x), cursor_char, curses.A_BOLD)
        stdscr.refresh()
        
    # set signal handlers
    signal.signal(signal.SIGINT, sigint_handler)
    
    # Bluetooth low energy setup
    client = await bluetooth_connect()
    if client == None:
        exit()

    service_uuid = "3cd00375-4415-4fe2-aa41-42bd35f1c526"
    characteristic_uuid = "cc84a98c-36be-4fe1-8345-be620545fd34"
    
    # curses setup
    stdscr = curses.initscr()
    signal.signal(signal.SIGWINCH, resize_handler)
    curses.noecho() # turns off automatic echoing of keys to screen
    curses.cbreak()
    stdscr.nodelay(True) # makes getch() non-blocking
    stdscr.keypad(True)
    curses.curs_set(0) # make terminal cursor invisible
    
    # cursor initialization
    cursor_x = midpoint_x
    cursor_y = midpoint_y
    old_cursor_x = cursor_x
    old_cursor_y = cursor_y

    time_ms = time.time_ns() // 1_000_000
    
    # start catching BLE notifications
    try:
        await client.start_notify(characteristic_uuid, ble_notification_handler)
    except:
        print(f"{Style.RED_BLD}Failed to subscribe to notifications{Style.RST}")
        await ble_cleanup_exit()
    # loop for catching input
    while True:
        if shutdown == True:
            await ble_cleanup_exit()
        await asyncio.sleep(0.01)  # yield control to asyncio
        key = stdscr.getch()
        match key:
            case 113: # 'q' -> quit
                await ble_cleanup_exit()
            case 114: # 'r' -> reset screen
                cursor_x = midpoint_x
                cursor_y = midpoint_y
                stdscr.clear()
asyncio.run(main())

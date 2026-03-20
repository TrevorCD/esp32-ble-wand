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

# Helper functions -------------------------------------------------------------

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
# end clear_screen


# Main -------------------------------------------------------------------------

async def main():
    
    def resize_handler(signum, frame):
        size = shutil.get_terminal_size()
        curses.resizeterm(size.lines, size.columns)
        stdscr.addstr(2, 0, f"resizes: {resizes}")
        stdscr.refresh()
    # end resize_handler
    signal.signal(signal.SIGWINCH, resize_handler)
    
    def keypress_q():
        curses.nocbreak()
        stdscr.keypad(False)
        #stdscr.nodelay(False)
        curses.echo()
        curses.endwin()
        exit()
    # end keypress_q
    
    # find bluetooth device
    print(f"{Style.BOLD}Bluetooth devices available:{Style.RESET}")
    devices = await bleak.BleakScanner.discover()
    i = 0
    for d in devices:
        print(f"{i}: {d}")
        i += 1
        
    # select bluetooth device
    print("\nEnter number to select device")

    selection = -1
    while True:
        try:
            selection = int(input())
            assert (selection < i) and (selection > -1)
            print(f"selected device {selection}: {devices[selection]}")
            break;
        except ValueError:
            print("\nInvalid input. Enter a number")
        except AssertionError:
            print("\nInvalid input. Enter a number that corresponds to a device")
    # end while
    
    # connect to bluetooth device


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
                
        # endif
        
    #end while
    
# end main

asyncio.run(main())

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

import bleak    # bluetooth lib
import shutil   # shell utilities
import signal   # signal catching
import curses   # terminal printing

# Globals ----------------------------------------------------------------------
resizes = 0
# Handlers ---------------------------------------------------------------------

# Helper functions -------------------------------------------------------------


# Main -------------------------------------------------------------------------

def main(stdscr):
    
    def resize_handler(signum, frame):
        global resizes
        size = shutil.get_terminal_size()
        curses.resizeterm(size.lines, size.columns)
        resizes += 1
        stdscr.addstr(2, 0, f"resizes: {resizes}")
        stdscr.refresh()
    # end resize_handler
    signal.signal(signal.SIGWINCH, resize_handler)

    
    # curses extra setup
    curses.noecho() # turns off automatic echoing of keys to screen
    stdscr.nodelay(True) # makes getch() non-blocking
    
    # loop for catching bluetooth communication and updating screen
    while(True):
        # bluetooth comm

        # update screen
        stdscr.addstr(0, 0, str(curses.LINES))
        stdscr.addstr(1, 0, str(curses.COLS))
        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('q'):
            break
        # endif
        
    #end while
    
# end main

curses.wrapper(main) # curses wrapper calls main

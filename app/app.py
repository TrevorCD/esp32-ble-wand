# Trevor B. Calderwood
# GPOS side application for magic wand communications
# written to Python 3.14.3 specifications

import bleak    # bluetooth lib
import shutil   # shell utilities
import signal   # signal catching

terminal_columns = -1 # terminal width in characters
terminal_lines   = -1 # terminal height in characters

def handle_resize(signum, frame):
    terminal_size = shutil.get_terminal_size()
    terminal_columns = terminal_size.columns
    terminal_lines = terminal_size.lines
    
# end handle_resize
    
def main(argv):
    terminal_size = shutil.get_terminal_size().columns # .columns .lines

    while(1):

        
    #end while
    
# end main

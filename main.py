import colorama
import sys
from typing import Union, Dict, List, Tuple
from ctypes import c_short
import json
import pathlib
from tkinter import Tk



def set_clipboard(text:str):
    """Set the clipboard

    Args:
        text (str): Text to be later pasted
    """        
    tk = Tk()
    tk.withdraw()
    tk.clipboard_clear()
    tk.clipboard_append(text)
    tk.update()
    input("Press enter when done pasting")
    tk.destroy()

def get_cursor():
    """Get cursor position in console

    Returns:
        Tuple[int,int]: X, Y corodinates
    """
    sys.stdout.write("\x1b[6n");a=sys.stdin.read(10)
    ret = a.removeprefix('\x1b[').removesuffix('R').splitlines(';')
    return ret[0], ret[1]

            
def display_res(startBits:int, fill1:int, fill1Value:bool, middleBits:int, fill2:int, fill2Value:bool, endBits:int):
    """Display the result bits (old way)

    Args:
        startBits (int): 8 starting bits
        fill1 (int): Number of recurring bits before middle
        fill1Value (bool): Fill bit value
        middleBits (int): 16 middle bits
        fill2 (int): Number of recurring bits before end
        fill2Value (bool): Fill bit value
        endBits (int): 8 end bits
    """
    for _ in range(10):
        print()
    
    # Header
    s=colorama.Fore.RESET 
    s+='Result: '
    
    # Start bits
    sb = format(startBits, 'b').rjust(8, '0')
    sbr = sb[:4] + "'" + sb[4:]
    s+=colorama.Fore.CYAN
    s+=sbr
    
    if not(fill1 == 0 and fill1Value):
        # Fill1
        s+=' '+colorama.Fore.GREEN
        for i in range(abs(fill1)):
            if i != 0 and i % 4 == 0:
                s+="'"
            s+= '1' if fill1Value else '0'
            
        # Middle bits
        s+=' '+colorama.Fore.MAGENTA
        mb = format(middleBits, 'b').rjust(16, '0')
        mbr = f"{mb[:4]}'{mb[4:8]}'{mb[8:12]}'{mb[12:]}"
        s+=mbr
        
    # Fill2
    if fill2 != 0:
        s+=' '+colorama.Fore.YELLOW
    for i in range(abs(fill2)):
        if i != 0 and i % 4 == 0:
            s+="'"
        s+= '1' if fill2Value else '0'
    
    # Start bits
    eb = format(endBits, 'b').rjust(8, '0')
    ebr = eb[:4] + "'" + eb[4:]
    
    s+=' '+colorama.Fore.BLUE
    s+=ebr
    
    print(s)
    
def bin_input(prompt:str, count:int):
    """Binary input

    Args:
        prompt (str): Text to be displayed before input
        count (int): Number of required bits

    Returns:
        int: Resulting integer
    """
    while True:
        try:
            v = input(prompt)
            if len(v) != count:
                print(colorama.Fore.RED+f"Must contain exactly {count} bits!"+colorama.Fore.RESET)
                continue
            res = int(v, 2)
            return res
        except ValueError:
            print(colorama.Fore.RED+f"Invalid input must be composed of only '1' or '0' (exactly {count} bits)!"+colorama.Fore.RESET)
            continue

def int_input(prompt:str):
    """Integer input

    Args:
        prompt (str): Text to be displayed before input

    Returns:
        int: Resulting integer
    """
    while True:
        try:
            v = input(prompt)
            res = int(v)
            return res
        except ValueError:
            print(colorama.Fore.RED+f"Invalid input must be integer!"+colorama.Fore.RESET)
            continue

def int_choice_input(prompt:str, choices:List[str]):
    """Prints a list of choices and waits for an integer input

    Args:
        prompt (str): Text to be displayed at the top
        choices (List[str]): List of choices not including Exit

    Returns:
        int: 0 if exit was selected or x+1 where the value choices[x] was selected
    """
    while True:
        print(prompt)
        print(f'0-> Exit')
        for i, name in enumerate(choices):
            print(f"{i+1}-> {name}")
        try:
            v = input("Enter value: ")
            res = int(v)
            if res < 0 or res > len(choices):
                print(f"{colorama.Fore.RED}Invalid input, must be between 0 and {len(choices)}!{colorama.Fore.RESET}")
            return res
        except ValueError:
            print(colorama.Fore.RED+f"Invalid input must be integer!"+colorama.Fore.RESET)
            continue

def yn_input(prompt:str):
    """Yes no input

    Args:
        prompt (str): Text to be displayed before input

    Returns:
        bool: _description_
    """
    while True:
        v = input(prompt).lower()
        if not v in 'yn':
            print(colorama.Fore.RED+"Invalid input must be 'y' or 'n'!"+colorama.Fore.RESET)
            continue
        
        return v == 'y'

def convert_to_words(startBits:int, fill1:int, fill1Value:bool, middleBits:int, fill2:int, fill2Value:bool, endBits:int):
    word1 = c_short((startBits << 8) | (0b10000000 if fill1Value else 0) | abs(fill1))
    word2 = c_short(middleBits)
    word3 = c_short((endBits << 8) | (0b10000000 if fill2Value else 0) | abs(fill2))
    return word1, word2, word3

def singleSequence():
    startBits = bin_input(colorama.Fore.RESET+"Enter 8 start bits (1/0): "+colorama.Fore.CYAN, 8)
    hasMiddle = yn_input(colorama.Fore.RESET+"Does the sequence require a middle section (16 middle bits)? (y/n): ")
    fill1 = 0
    fill1Value = True
    middleBits = 0
    if hasMiddle:
        fill1 = int_input(colorama.Fore.RESET+"Fill 1 section, enter number of repeating bits before middle bits.\nPositive value for fill with '1's, negative to fill with '0's. Count: "+colorama.Fore.GREEN)
        fill1Value = fill1 >= 0
        middleBits = bin_input(colorama.Fore.RESET+"Enter 16 middle bits (0/1): "+colorama.Fore.MAGENTA, 16)
    fill2 = int_input(colorama.Fore.RESET+"Fill 2 section, enter number of repeating bits before last 8 bits.\nPositive value for fill with '1's, negative to fill with '0's. Count: "+colorama.Fore.YELLOW)
    fill2Value = fill2 >= 0
    endBits = bin_input(colorama.Fore.RESET+"Enter the last 8 bits (1/0): "+colorama.Fore.BLUE, 8)
    display_res(startBits, fill1, fill1Value, middleBits, fill2, fill2Value, endBits)
    word1, word2, word3 = convert_to_words(startBits, fill1, fill1Value, middleBits, fill2, fill2Value, endBits)
    print()
    print(colorama.Fore.RESET+"Result:")
    print(word1.value,end=',')
    print(word2.value,end=',')
    print(word3.value)
    return startBits, word1.value&255, middleBits, word3.value&255, endBits

def simplified():
    while True:
        singleSequence()
        input("Press enter to continue")

def advanced():
    NO_FILL = 128
    sequenceTemplate = {
        'StartBits': int('00000000',2),
        'Fill1': NO_FILL,
        'MiddleBits': int('0000000000000000',2),
        'Fill2': 0,
        'EndBits': int('00000000',2)
    }
    
    def ReturnNoneOnInterrupt(func):
        def funcCall(*args, **kwargs):
            print(colorama.Fore.YELLOW+"Pressing CTRL+C will go back to previous menu/input"+colorama.Fore.RESET)
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                print()
                return None
        return funcCall
    
    def reorder_drills_first(part:Dict[str, Dict[str, int]]):
        res = {}
        for k, v in part.items():
            if k.startswith('Feed'):
                continue
            res[k] = v
        for k, v in part.items():
            if not k.startswith('Feed'):
                continue
            res[k] = v
        return res
    
    def display_part(part:Dict[str, Dict[str, int]]):
        s = ''
        just = 4
        for n in part.keys(): # Get the maximum name length to justify the name column
            just = max(just, len(n))
        
        s+='Name'.ljust(just)+'  ' # Justify name    
        for i in range(69): # nice
            if i%2 == 0:
                s+=colorama.Back.BLACK
            else:
                s+=colorama.Back.LIGHTBLACK_EX
            s+=str(i+1).zfill(2)
        s+='\n'
        
        for k, v in part.items():
            index = 0
            startBits = v['StartBits']
            fill1 = v['Fill1']
            fill1Count = fill1&127
            fill1Value = fill1&128 == 128
            middleBits = v['MiddleBits']
            fill2 = v['Fill2']
            # Bits: VCCCCCCC
            fill2Count = fill2&127 # Last 7 bits is the count 
            fill2Value = fill2&128 == 128 # First bit 
            endBits = v['EndBits']
            
            
            s += k.ljust(just)+'  ' # Justify the name
            
            # Start bits
            sb = format(startBits, 'b').rjust(8, '0')
            s+=colorama.Fore.CYAN
            for b in sb:
                if index%2 == 0:
                    s+=colorama.Back.BLACK
                else:
                    s+=colorama.Back.LIGHTBLACK_EX
                index+=1
                s+=b+' '
            
            if fill1 != 128:
                # Fill1
                s+=colorama.Fore.GREEN
                for i in range(fill1Count):
                    if index%2 == 0:
                        s+=colorama.Back.BLACK
                    else:
                        s+=colorama.Back.LIGHTBLACK_EX
                    index+=1
                    s+= '1 ' if fill1Value else '0 '
                    
                # Middle bits
                s+=colorama.Fore.MAGENTA
                mb = format(middleBits, 'b').zfill(16)
                for b in mb:
                    if index%2 == 0:
                        s+=colorama.Back.BLACK
                    else:
                        s+=colorama.Back.LIGHTBLACK_EX
                    index+=1
                    s+=b+' '
                
                
            # Fill2
            s+=colorama.Fore.YELLOW
            for i in range(fill2Count):
                if index%2 == 0:
                    s+=colorama.Back.BLACK
                else:
                    s+=colorama.Back.LIGHTBLACK_EX
                index+=1
                s+= '1 ' if fill2Value else '0 '
            
            # End bits
            s+=colorama.Fore.BLUE
            eb = format(endBits, 'b').zfill(8)
            for b in eb:
                if index%2 == 0:
                    s+=colorama.Back.BLACK
                else:
                    s+=colorama.Back.LIGHTBLACK_EX
                index+=1
                s+=b+' '
            
            s+=colorama.Back.RESET+colorama.Fore.RESET+'\n' # Change line
        print(s)
        print(colorama.Back.RESET+colorama.Fore.RESET)
        print("Results:")
        s=''
        clipboard=''
        for k, v in part.items():
            startBits = v['StartBits']
            fill1 = v['Fill1']
            fill1Count = fill1&127
            fill1Value = fill1&128 == 128
            middleBits = v['MiddleBits']
            fill2 = v['Fill2']
            # Bits: VCCCCCCC
            fill2Count = fill2&127 # Last 7 bits is the count 
            fill2Value = fill2&128 == 128 # First bit 
            endBits = v['EndBits']
            
            word1, word2, word3 = convert_to_words(startBits, fill1Count, fill1Value, middleBits, fill2Count, fill2Value, endBits)
            
            s+=k.ljust(just)+'  '
            s+=str(word1.value).ljust(8)
            s+=str(word2.value).ljust(8)
            s+=str(word3.value).ljust(8)
            s+='\n'
            clipboard+=k+'\t'
            clipboard+=str(word1.value)+'\t'
            clipboard+=str(word2.value)+'\t'
            clipboard+=str(word3.value)+'\n'
        print(s)
        return clipboard.removesuffix('\n')
    
    def select_part():
        cwd = pathlib.Path().cwd()
        parts = []
        for f in cwd.iterdir():
            if f.suffix == '.json':
                parts.append(f.stem.split('\\')[-1])
        
        p = int_choice_input('Select a part', parts)
        if p == 0:
            return None
        return parts[p-1]
    
    def edit(name:str):
        part = {}
        try:
            with open(name+'.json', 'r') as r:
                part = json.load(r)
                display_part(part)
        except FileNotFoundError:
            pass
        while True:
            choice = ReturnNoneOnInterrupt(int_choice_input)(f"Creating {name}", ['Add sequence', 'Remove sequence', 'Save'])
            if choice == None or choice == 0: # Exit
                if yn_input("Are you sure you want to exit? Unsaved progress will be lost. (y/n) "):
                    return
                else:
                    continue
            if choice == 1: # Add sequence
                seqName = ReturnNoneOnInterrupt(input)('Enter a name for this sequence: ')
                if seqName == None:
                    continue
                try:
                    startBits, fill1, middleBits, fill2, endBits = singleSequence()
                    seq = sequenceTemplate.copy()
                    seq['StartBits'] = startBits
                    seq['Fill1'] = fill1
                    seq['MiddleBits'] = middleBits
                    seq['Fill2'] = fill2
                    seq['EndBits'] = endBits
                    part[seqName] = seq
                    display_part(part)
                except KeyboardInterrupt:
                    continue
            if choice == 2: # Remove sequence
                choices = list(part.keys())
                rmSeq = ReturnNoneOnInterrupt(int_choice_input)("Choose a sequence to remove", choices)
                if rmSeq == None or rmSeq == 0:
                    continue
                part.pop(choices[rmSeq-1])
            if choice == 3: # Save
                with open(name+'.json', 'w') as w:
                    json.dump(part, w, indent=4)
    
    def sequence_to_bits(sequence:Dict[str, int]):
        startBits:int = sequence['StartBits']
        fill1:int = sequence['Fill1']
        fill1Count:int = fill1&127
        fill1Value:int = fill1&128 == 128
        middleBits:int = sequence['MiddleBits']
        fill2:int = sequence['Fill2']
        # Bits: VCCCCCCC
        fill2Count:int = fill2&127 # Last 7 bits is the count 
        fill2Value:int = fill2&128 == 128 # First bit 
        endBits:int = sequence['EndBits']
        
        s=''
        # Start bits
        sb = format(startBits, 'b').zfill(8)
        for b in sb:
            s+=b
        
        if fill1 != 128:
            # Fill1
            for _ in range(fill1Count):
                s+= '1' if fill1Value else '0'
                
            # Middle bits
            mb = format(middleBits, 'b').zfill(16)
            for b in mb:
                s+=b
            
            
        # Fill2
        for _ in range(fill2Count):
            s+= '1' if fill2Value else '0'
        
        # End bits
        eb = format(endBits, 'b').zfill(8)
        for b in eb:
            s+=b
            
        return [b=='1' for b in s]
        
    def check_feed_overlap(part:Dict[str, Dict[str, int]]):
        bits = []
        names = []
        errorCount = 0
        for k, v in part.items():
            if not k.startswith('Feed'):
                continue
            names.append(k)
            bits.append(list(sequence_to_bits(v)))
        bitsForSteps = list(zip(*bits))
        
        for step, actions in enumerate(bitsForSteps):
            feedHappened = False
            first = -1
            for actionID, action in enumerate(actions):
                if (not feedHappened) and action:
                    first = actionID
                    feedHappened = True
                    continue
                if feedHappened and action:
                    print(f"{colorama.Fore.RED}Conflict between {names[first]} and {names[actionID]} at step {step+1}.{colorama.Fore.RESET}")
                    errorCount+=1
            if not feedHappened:
                print(f"{colorama.Fore.RED}No feed instruction at step {step+1}.{colorama.Fore.RESET}")
                errorCount+=1
        if errorCount == 0:
            print(f"{colorama.Fore.GREEN}No overlap or empty feed detected!{colorama.Fore.RESET}")
        return errorCount
        
            
        
    
    def create():
        name = ReturnNoneOnInterrupt(input)('Enter a name for this part: ')
        if name == None:
            return
        edit(name)
    
    def read():
        partName = select_part()
        if partName == None:
            return
        part = {}
        try:
            with open(partName+'.json', 'r') as r:
                part = json.load(r)
        except FileNotFoundError:
            print(f"Unable to open {partName}.json")
            return
        c = ReturnNoneOnInterrupt(int_choice_input)("Display option", ['As shown in excel (Feeds first then drills)', 'As shown in PLC data files (Drills first then feeds)'])
        if c == None or c == 0:
            return
        if c == 2: # Drills first
            # Files are encoded in the order found in excel file, so it needs to be reordered
            part = reorder_drills_first(part)
        clipboard = display_part(part)
        
        c = ReturnNoneOnInterrupt(yn_input)("Copy to clipboard?")
        if c == None or c == False:
            return
        set_clipboard(clipboard)
    
    def edit_part():
        partName = select_part()
        if partName == None:
            return
        edit(partName)
    
    def check():
        partName = select_part()
        if partName == None:
            return
        part = {}
        try:
            with open(partName+'.json', 'r') as r:
                part = json.load(r)
        except FileNotFoundError:
            print(f"Unable to open {partName}.json")
            return
        display_part(part)
        errorCount = check_feed_overlap(part)
        
        print(f"Check completed, found {errorCount} errors.")
    
    while True:
        v = int_choice_input("Main menu", ['Create a part', 'Read a part', 'Edit part', 'Validate a part'])
        if v == 0:
            break
        if v == 1:
            create()
        if v == 2:
            read()
        if v == 3:
            edit_part()
        if v == 4:
            check()
        

def run():
    
    
    while True:
        print("This program has two modes, simplified and advanced.")
        print("Simplified is the base logic that allows you to make a single encoding every time.")
        print("Advanced allows you to create a json file and encode a whole sequence all at once.")
        
        print()
        res = int_choice_input("Enter mode: ", ["Simplified","Advanced"])
        if res == 0:
            return
        if res == 1:
            simplified()
        if res == 2:
            advanced()
        if res > 2:
            print(f"{colorama.Fore.RED}Invalid input, must be 0, 1 or 2.{colorama.Fore.RESET}")

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        pass
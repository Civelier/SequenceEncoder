# Sequence encoder
A small script to encode step actions into 3 words.

## Requirements
- Python 3.11.4 or above
- Visual Studio Code with python extensions

## Setup
Install python 3.11.4 or above and make sure to add python to PATH.

Test python by openning a cmd prompt and write:
```sh
python --version
```
If the command isn't found, python might not have been added to path, see [How to add python to PATH](https://www.educative.io/answers/how-to-add-python-to-path-variable-in-windows).

Start Visual Studio Code and open this folder. Open a new terminal and create the venv:
```sh
python -m venv .venv
```
Then, activate the venv:
```sh
.\.venv\Scripts\Activate.ps1
```
Install the dependencies:
```sh
pip install -r requirements.txt
```
Now you're all set up...
To run the program (remember to activate the venv in every new terminal you open):
```sh
python -m main.py
```
Or press F5 in Visual Studio Code with the file main.py open.


## Encoding style
This program will generate three 16-bit integers that can then be copied in the PLC data table.

The steps are encoded such that, given a step number, the result will be a boolean indicating whether or not to execute the action.

There are 5 sections:
- Start bits (8 first steps)
- Fill 1 (1s or 0s repeated a given number of times, optionnal)
- Middle bits (16 middle steps, optionnal)
- Fill 2 (1s or 0s repeated a number of times)
- End bits (8 last steps)

![Encoding style](https://github.com/Civelier/SequenceEncoder/blob/main/images/Encoding%20Style.PNG?raw=true)

### Word 1
Word 1 contains the information for the 8 start bits and fill 1. Since in some cases, the 16 middle bits are not needed, there is a way to skip them. If fill vaalue is 1 and fill 1 count is 0, the fill 1 and middle steps are skipped.

![Word 1](https://github.com/Civelier/SequenceEncoder/blob/main/images/Word%201.PNG?raw=true)

Example:
```
#        8 first bits      | bit 7 == 1 | fill 1 count
Word1 = 0b1010110000000000 | 128        | 8

# Would result in steps:
1010110011111111<rest of sequence>...
```

### Word 2
Word 2 is simply the 16 middle steps encoded as bits, where bit 15 comes before bit 0 in the sequence. Thsi is so that values can be read in binary format more easily.

![Word 2](https://github.com/Civelier/SequenceEncoder/blob/main/images/Word%202.PNG?raw=true)

### Word 3
Word 3 contains the 8 end bits and fill 2.

![Word 3](https://github.com/Civelier/SequenceEncoder/blob/main/images/Word%203.PNG?raw=true)


### Examples
#### With middle bits:
```
# Start bits: 01011100
# Fill 1: fill with 0s 8 times (0000 1000)
# Middle bits: 0000111100001010
# Fill 2: fill with 1s 9 times (1000 1001)
# End bits: 10100011

Word1 = 23560 # 0101 1100 0000 1000
Word2 = 3850 # 0000 1111 0000 1010
Word3 = -23671 # 1010 0011 1000 1001

# Result:
# Start   |  Fill 1  |     Middle bits     |  Fill 2   | End bits
0101 1100   00000000   0000 1111 0000 1010   111111111   1010 0011
```

#### Without middle bits:
```
# Start bits: 01011100
# Fill 1: skip, so 128 (1000 0000)
# Middle bits: 0000000000000000
# Fill 2: fill with 0s 3 times (0000 0011)
# End bits: 10100011

Word1 = 23680 # 0101 1100 1000 0000
Word2 = 0 # 0000 0000 0000 0000
Word3 = -23805 # 1010 0011 0000 0011

# Result:
# Start   | Fill 2 | End bits
0101 1100    000     1010 0011
```

## Usage
### Simplified mode
Simplified mode is the old method to create a single sequence.

### Advanced mode (recommended)
Advanced mode allows you to save multiple sequences into a file and load them later.
# Sequence encoder for Metaltech
A small script to encode step actions into 3 words.

## Requirements
- Python 3.11.4 or above
- Visual Studio Code with python extensions

## Usage
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
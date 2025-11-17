# Turing
This is an interpreter for Turing machines.

## System requirements
+ `Python` version >= 3.10

## Usage

```python
from Turing import *

with open("Programs/addition_machine.tur", "r") as f:
    text = f.read()

machine = TuringMachine.parse(text)

tape_str = "I#IIII"
tape = list(tape_str)

ret_tape = machine.run(tape, debug_strength=1)
```

Where `.tur` files should be of a form similar to:
```
Q0 I Q0 I R
Q0 # Q1 I R
Q1 I Q1 I R
Q1 b Q2 b L
Q2 I QE b S
```

Tape symbols need to be exactly one character and the empty symbol is `b`. 

## License

[MIT](https://choosealicense.com/licenses/mit/)



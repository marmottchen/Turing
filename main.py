from Turing import *


with open("Programs/Sheet_4/Ex1.tur", "r") as f:
    text = f.read()

machine = TuringMachine.parse(text)

tape_str = "111222111111222"
tape = list(tape_str)

ret_tape = machine.run(tape, debug_strength=1)

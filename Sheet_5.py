from Turing import *


def ex1():
    with open("Programs/Sheet_5/Ex1.tur", "r") as f:
        text = f.read()

    machine = TuringMachine.parse(text)

    tape_strs = ["11", "1010", "1001", "100101"]
    for tape_str in tape_strs:
        tape = list(tape_str)
        ret_tape, final_state = machine.run(tape)
        print(f"Input {tape_str} halted in state {final_state}.")


def ex1_div_three():
    with open("Programs/Sheet_5/Ex1.tur", "r") as f:
        text = f.read()

    machine = TuringMachine.parse(text)

    for c in range(1000):
        b = format(c, 'b')
        tape = list(b)
        ret_tape, final_state = machine.run(tape)

        if c % 3 == 0:
            assert final_state == "Qak"
        else:
            assert final_state == "Qab"

    print("Test successfully completed.")


def ex2():
    with open("Programs/Sheet_5/Ex2.tur", "r") as f:
        text = f.read()

    machine = TuringMachine.parse(text)
    tape = list("010011")
    ret_tape, final_state = machine.run(tape, debug_strength=2)


def ex3():
    with open("Programs/Sheet_5/Ex3.tur", "r") as f:
        text = f.read()

    machine = TuringMachine.parse(text)

    tape_strs = ["11", "00000111111", "000000", "00011110"]
    for tape_str in tape_strs:
        tape = list(tape_str)
        ret_tape, final_state = machine.run(tape)
        print(f"Input {tape_str} halted in state {final_state}.")


if __name__ == "__main__":
    ex3()

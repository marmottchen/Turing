from dataclasses import dataclass


EMPTY = "b"
START_STATE = "Q0"

L = -1
R = 1
S = 0


@dataclass()
class TuringCommand:
    """
    Stores a single command of the form: inp_state, inp_symbol -> ret_state, ret_symbol, ret_move.
    The symbols need to have length exactly one and ret_move can be L=-1, R=1 or S=0.
    """
    inp_state: str
    inp_symbol: str

    ret_state: str
    ret_symbol: str
    ret_move: L | R | S

    def __post_init__(self):
        if len(self.inp_symbol) != 1:
            raise ValueError(f"Symbols need to have length one, but inp_symbol is {self.inp_symbol} with length "
                             f"{len(self.inp_symbol)}.")
        if len(self.ret_symbol) != 1:
            raise ValueError(f"Symbols need to have length one, but ret_symbol is {self.ret_symbol} with length "
                             f"{len(self.ret_symbol)}.")
        if self.ret_move not in [L, R, S]:
            raise ValueError(f"ret_moves needs to be either L=-1, R=1 or S=0, but is {self.ret_move}.")

    @classmethod
    def parse(cls, text: str) -> 'TuringCommand':
        """Creates a TuringCommand from its string representation."""
        inp_state, inp_symbol, ret_state, ret_symbol, ret_move_str = text.split(" ")

        match ret_move_str:
            case "L":
                ret_move = L
            case "R":
                ret_move = R
            case "S":
                ret_move = S
            case _:
                raise ValueError(f"The move of a command needs to be saved as either 'L', 'R' or 'S', but tried to "
                                 f"parse '{ret_move_str}' in command '{text}'.")

        return cls(inp_state, inp_symbol, ret_state, ret_symbol, ret_move)


@dataclass()
class TuringState:
    """Stores the state of a Turing machine and the tape."""
    tape: list[str]
    position: int = 0
    offset: int = 0
    state: str = START_STATE

    @property
    def symbol(self) -> str:
        """
        Return the symbol at the position in the tape.

        >>> ts = TuringState(["-2", "-1", "0", "1", "2", "3"], 2, 2)
        >>> ts.symbol
        '2'
        """
        return self.tape[self.position + self.offset]

    def execute_command(self, command: TuringCommand):
        """
        Executes a single TuringCommand if its requirements are met, else raises an error.

        >>> ts = TuringState(["-2", "-1", "0", "1", "2", "3"], 2, 2, "Q1")
        >>> tc = TuringCommand("Q1", "2", "Q2", "3", L)
        >>> ts.execute_command(tc)
        >>> ts.tape
        ['-2', '-1', '0', '1', '3', '3']
        >>> ts.position
        1
        >>> ts.state
        'Q2'

        >>> ts = TuringState(["0", "1"], 0, 0, "Q1")
        >>> tc = TuringCommand("Q1", "0", "Q2", "0", L)
        >>> ts.execute_command(tc)
        >>> ts.tape
        ['b', '0', '1']
        >>> ts.position
        -1
        >>> ts.offset
        1

        >>> ts = TuringState(["0", "1"], 1, 0, "Q1")
        >>> tc = TuringCommand("Q1", "1", "Q2", "1", R)
        >>> ts.execute_command(tc)
        >>> ts.tape
        ['0', '1', 'b']
        >>> ts.position
        2
        """
        if self.state == command.inp_state:

            if self.symbol == command.inp_symbol:
                self.tape[self.position + self.offset] = command.ret_symbol
                self.state = command.ret_state

                self.position += command.ret_move

                # Handling out of tape bound movements
                if self.position + self.offset < 0:
                    self.offset += 1
                    self.tape = [EMPTY] + self.tape
                elif self.position + self.offset >= len(self.tape):
                    self.tape = self.tape + [EMPTY]

                assert 0 <= self.position + self.offset < len(self.tape)

            else:
                raise ValueError(f"Command requires symbol {command.inp_symbol}, but current symbol is {self.symbol}.")

        else:
            raise ValueError(f"Command requires state {command.inp_state}, but current state is {self.state}.")

    def __str__(self) -> str:
        string = f"{''.join(self.tape)}\n{' ' * (self.position + self.offset)}^{self.state}"
        return string


@dataclass()
class TuringMachine:
    """Stores a program of the form dict[(state, symbol): command]."""
    programm: dict[(str, str): TuringCommand]

    @classmethod
    def parse(cls, text: str) -> 'TuringMachine':
        """Creates a TuringMachine from its string representation."""
        programm = {}
        lines = text.split("\n")
        for line in lines:
            if len(line) != 0:
                command = TuringCommand.parse(line)
                programm[(command.inp_state, command.inp_symbol)] = command

        return cls(programm)

    def single_step(self, turing_state: TuringState) -> bool:
        """
        Returns False if the program contains no commands for the given turing_state, else executes a single fitting
        command on the turing_state and returns True.

        >>> ts = TuringState(["0", "1"], 0, 0, "Q1")
        >>> tm = TuringMachine({("Q1", "0"): TuringCommand("Q1", "0", "Q2", "1", R)})
        >>> tm.single_step(ts)
        True
        >>> ts.tape
        ['1', '1']

        >>> tm = TuringMachine({})
        >>> tm.single_step(ts)
        False
        >>> ts.tape
        ['1', '1']
        """
        state, symbol = (turing_state.state, turing_state.symbol)

        if (state, symbol) in self.programm:
            command: TuringCommand = self.programm[(state, symbol)]
            turing_state.execute_command(command)

            return True
        else:
            return False

    def run(self, tape: list[str], start_state: str = START_STATE, debug_strength: int = 0) -> (list[str], str):
        """
        Runs the program on the given tape until it halts and returns the resulting tape and the final state.

        The amount of debug output can be controlled through debug_strength, with: \n
        0: no debug printing \n
        1: Printing the final result \n
        2: Printing results of every step
        """
        turing_state = TuringState(tape, state=start_state)

        run = True
        while run:
            if debug_strength >= 2:
                print(turing_state)

            run = self.single_step(turing_state)

        if debug_strength >= 1:
            print(f"Program finished on state {turing_state.state} and tape: \n{''.join(turing_state.tape)}")
        return turing_state.tape, turing_state.state


if __name__ == "__main__":
    import doctest
    doctest.testmod()

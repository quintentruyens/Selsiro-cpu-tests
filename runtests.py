"""
Provides the run_tests function to run all of the test case on an implementation of the CPU
"""

from typing import List, Dict, Literal, Tuple, Union, Optional
from .tester import Tester


FORMAT_BOLD_RED = "\x1B[1;91m"
FORMAT_BOLD_GREEN = "\x1B[1;92m"
FORMAT_BOLD_YELLOW = "\x1B[1;93m"
FORMAT_END = "\x1B[0m"

# Temporary format for tests, should be updated later to use the assembler.
# This should allow the easy creation of tests with assembly language and the corresponding
# assertions together.
Instruction = int
Control = str
TestCase = List[Union[Instruction, Control]]
Address = int

tests: Dict[str, TestCase] = {
    "empty-test": [
        "r0 == 0",
        "r1 == 0",
        "r2 == 0",
        "r3 == 0",
        "r4 == 0",
        "r5 == 0",
        "r6 == 0",
        "r7 == 0",
        "r8 == 0",
        "r9 == 0",
        "r10 == 0",
        "r11 == 0",
        "r12 == 0",
        "r13 == 0",
        "r14 == 0",
        "r15 == 0",
        "r16 == 0",
        "r17 == 0",
        "r18 == 0",
        "r19 == 0",
        "r20 == 0",
        "r21 == 0",
        "r22 == 0",
        "r23 == 0",
        "r24 == 0",
        "r25 == 0",
        "r26 == 0",
        "r27 == 0",
        "r28 == 0",
        "r29 == 0",
        "r30 == 0",
        "r31 == 0",
        "end",
    ],
    "addi-test": [
        "r0 == 0",
        "r1 == 0",
        "r5 == 0",
        0x00100093,  # addi x1, x0,  1
        "r0 == 0",
        "r1 == 1",
        "r5 == 0",
        0x00908293,  # addi x5, x1,  9
        "r0 == 0",
        "r1 == 1",
        "r5 == a",
        0xFFD28293,  # addi x5, x5, -3
        "r0 == 0",
        "r1 == 1",
        "r5 == 7",
        "end",
    ],
}


def run_tests(tester: Tester) -> bool:
    """Run all of the test cases on the given implementation of the CPU"""
    success = True
    for name, test in tests.items():
        success = success and run_test_case(name, test, tester)

    if success:
        print(f"{FORMAT_BOLD_GREEN}All tests passed{FORMAT_END}")
    return success


Program = bytes
Controls = Dict[Address, List[Control]]


def parse_test_case(test: TestCase) -> Tuple[Program, Controls]:
    """
    Extract from the test case the program as a bytes object and the controls associated with
    every instruction address
    """
    program: Program = bytes()
    controls: Controls = {}
    program_counter = 0

    for line in test:
        if isinstance(line, Instruction):
            program += line.to_bytes(4, byteorder="little")
            program_counter += 1
        else:
            controls[program_counter] = controls.get(program_counter, []) + [line]

    return (program, controls)


ControlResult = Optional[Literal["AssertionFailed", "EndTest"]]


def run_controls(
    testname: str, program_counter: int, controls: List[str], tester: Tester
) -> ControlResult:
    """Run the controls and assertions in the given list of controls"""
    for control in controls:
        if control == "end":
            return "EndTest"

        # Currently only 'r# == #' assertions are supported
        reg, val = control.split("==")
        assert reg.startswith("r")
        regnum = int(reg.strip(" ")[1:])
        expected = int(val.strip(" "), 16)
        actual = tester.get_register(regnum)

        if actual != expected:
            print(
                f"{FORMAT_BOLD_RED}Test '{testname}' failed: "
                + f"assertion '{control}' failed at address '{program_counter}'{FORMAT_END}"
            )
            print(
                f"{FORMAT_BOLD_RED}Expected value: {expected}, Actual value: {actual}{FORMAT_END}"
            )
            return "AssertionFailed"
    return None


def run_test_case(name: str, test: TestCase, tester: Tester) -> bool:
    """Run a single test case on the given implementation"""
    print(f"{FORMAT_BOLD_YELLOW}Running test case '{name}'{FORMAT_END}")
    program, controls = parse_test_case(test)

    tester.start(program)
    program_counter = 0

    while True:
        curr_controls = controls.get(program_counter, [])
        control_result = run_controls(name, program_counter, curr_controls, tester)
        if control_result is not None:
            tester.stop()
            if control_result == "AssertionFailed":
                return False
            elif control_result == "EndTest":
                return True
            else:
                raise AssertionError("Invalid result from test_assertions")

        tester.clock()
        program_counter = tester.get_pc()

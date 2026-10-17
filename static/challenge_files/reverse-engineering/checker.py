#!/usr/bin/env python3
"""
A tiny "license checker" — safe to read, safe to run.
Reverse the logic (don't just brute force at runtime) to recover the flag.
"""

EXPECTED = [
    84, 85, 76, 91, 97, 104, 127, 108, 127, 104, 105, 115, 116, 125, 69, 115,
    105, 69, 112, 111, 105, 110, 69, 104, 127, 123, 126, 115, 116, 125, 103,
]

KEY = 0x1A  # hiding in plain sight


def check(candidate: str) -> bool:
    if len(candidate) != len(EXPECTED):
        return False
    return all((ord(c) ^ KEY) == expected for c, expected in zip(candidate, EXPECTED))


if __name__ == "__main__":
    guess = input("Enter flag: ")
    print("Correct!" if check(guess) else "Incorrect.")

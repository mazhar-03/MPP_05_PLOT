#!/usr/bin/env python3
"""
Interactive Game of Life on a finite 2D grid with cyclic boundaries.
Allows rule changes at runtime (birth/survival).
"""

import numpy as np
import sys
import os


def load_grid(path="initial_grid.csv"):
    if not os.path.isfile(path):
        print(f"Error: Cannot find '{path}'. Please create it as comma-separated 0/1.")
        sys.exit(1)
    try:
        grid = np.loadtxt(path, dtype=int, delimiter=",")
    except Exception as e:
        print("Failed to load grid:", e)
        sys.exit(1)
    return grid


def print_grid(grid):
    # ASCII display: live=█, dead=·
    for row in grid:
        print("".join("█" if cell else "·" for cell in row))
    print()


def step(grid, birth_set, survive_set):
    h, w = grid.shape
    new = np.zeros_like(grid)
    # use roll for wrap-around neighbor sums
    nbrs = (
            np.roll(np.roll(grid, 1, 0), 1, 1) +  # up-left
            np.roll(np.roll(grid, 1, 0), 0, 1) +  # up
            np.roll(np.roll(grid, 1, 0), -1, 1) +  # up-right
            np.roll(np.roll(grid, 0, 0), 1, 1) +  # left
            np.roll(np.roll(grid, 0, 0), -1, 1) +  # right
            np.roll(np.roll(grid, -1, 0), 1, 1) +  # down-left
            np.roll(np.roll(grid, -1, 0), 0, 1) +  # down
            np.roll(np.roll(grid, -1, 0), -1, 1)  # down-right
    )
    for r in range(h):
        for c in range(w):
            n = nbrs[r, c]
            if grid[r, c] == 1:
                new[r, c] = 1 if n in survive_set else 0
            else:
                new[r, c] = 1 if n in birth_set else 0
    return new


def parse_set(s):
    # e.g. "3 2,4" → {2,3,4}
    parts = s.replace(",", " ").split()
    try:
        return set(int(p) for p in parts)
    except:
        return set()


def main():
    grid = load_grid()
    # default Conway rules
    birth = {3}
    survive = {2, 3}
    print("Interactive Game of Life (wrap-around).")
    print("Commands:")
    print("  step (s)    → advance one generation")
    print("  run N (r N) → advance N generations")
    print("  rules (u)   → update birth/survival sets")
    print("  show (p)    → print current grid")
    print("  quit (q)    → exit\n")
    print("Starting grid:")
    print_grid(grid)
    print(f"Current rules: Birth={sorted(birth)}  Survival={sorted(survive)}\n")

    while True:
        cmd = input(">>> ").strip().lower().split()
        if not cmd:
            continue
        if cmd[0] in ("quit", "q", "exit"):
            print("Goodbye!")
            break

        if cmd[0] in ("step", "s"):
            grid = step(grid, birth, survive)
            print_grid(grid)
            continue

        if cmd[0] in ("run", "r") and len(cmd) >= 2 and cmd[1].isdigit():
            n = int(cmd[1])
            for _ in range(n):
                grid = step(grid, birth, survive)
            print(f"After {n} generations:")
            print_grid(grid)
            continue

        if cmd[0] in ("show", "p", "print"):
            print_grid(grid)
            continue

        if cmd[0] in ("rules", "u", "update"):
            b_in = input("Enter birth counts (e.g. '3' or '2 3'): ")
            s_in = input("Enter survival counts (e.g. '2 3'): ")
            b_set = parse_set(b_in)
            s_set = parse_set(s_in)
            if b_set and s_set:
                birth, survive = b_set, s_set
                print(f"Rules updated: Birth={sorted(birth)}  Survival={sorted(survive)}\n")
            else:
                print("Invalid input; rules unchanged.\n")
            continue

        print("Unknown command. Type 'step', 'run N', 'rules', 'show', or 'quit'.")


if __name__ == "__main__":
    main()

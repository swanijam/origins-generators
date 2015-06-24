#!/usr/bin/env python3
import sys

def main():
    args = sys.argv[1:]

    expected_lines = []
    actual_lines = []

    # Convert each output file to a list.
    for line in open('testing/expected.csv'):
        expected_lines.append(line)

    for line in open('testing/test_output.csv'):
        actual_lines.append(line)

    # Sort the lists so that dictionary random-ordering can be ignored.
    expected_lines = sorted(expected_lines)
    actual_lines = sorted(actual_lines)

    # Compare the lists.
    if expected_lines == actual_lines:
        sys.stdout.write('Output matches.\n')
    else:
        sys.stdout.write('Output does not match!\n')

if __name__ == "__main__":
    main()

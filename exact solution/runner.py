#!/usr/bin/env python3
import subprocess
import time
import os

SCRIPT = os.path.join("test_cases", "run_test_cases.sh")

def main():
    if not os.path.exists(SCRIPT):
        print(f"Error: {SCRIPT} does not exist.")
        return

    start = time.time()

    # Call bash on all platforms
    result = subprocess.run(
        ["bash", SCRIPT],
        capture_output=True,
        text=True
    )

    end = time.time()
    total = end - start

    print("===== WALL CLOCK TIME =====")
    print(f"{total:.4f} seconds")
    print("===========================\n")

    if result.stdout.strip():
        print(result.stdout)
    if result.stderr.strip():
        print("===== ERRORS =====")
        print(result.stderr)

if __name__ == "__main__":
    main()

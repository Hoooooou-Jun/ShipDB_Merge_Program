from typing import List
import sys


if __name__ == "__main__":
    case: int = int(sys.stdin.readline())
    for _ in range(case):
        command: str = sys.stdin.readline()
        command = command[:-1]
        size: int = int(sys.stdin.readline())
        arr = ""
        if size == 0:
            arr = sys.stdin.readline()
            arr = []
        else:
            arr = sys.stdin.readline()
            arr = list(map(int, arr[1:-2].split(',')))
        is_revers = False
        is_ok = True
        front = 0
        rear = 0
        for i in range(len(command)):
            if command[i] == 'R':
                arr.reverse()
            else:
                if len(arr) == 0:
                    arr = "error"
                    break
                arr.pop(0)
        if arr == "error":
            print(arr)
        else:
            print("[" + ','.join(map(str, arr)) + "]")
        
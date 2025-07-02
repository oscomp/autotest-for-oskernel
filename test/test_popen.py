import subprocess
import sys

if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) == 2:
        print("This is stdout")
        print("This is stderr", file=sys.stderr)
        sys.exit(0)
    p = subprocess.Popen(f'python {sys.argv[0]} sub', stdout=open("stdout.txt", "w"), stderr=open("stderr.txt", "w"))
    p.wait()

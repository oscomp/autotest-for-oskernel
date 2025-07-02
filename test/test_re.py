
import re

s = "[m#### OS COMP TEST GROUP START basic-musl ####"
start = re.compile(r"#### OS COMP TEST GROUP START ([a-zA-Z0-9-]+) ####")
print(start.findall(s))

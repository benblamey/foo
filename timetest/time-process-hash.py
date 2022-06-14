import hashlib
import pathlib
import time
import subprocess

start = time.time()
print(hashlib.md5(pathlib.Path('../image/original_0.png').read_bytes()).hexdigest())
end = time.time()

# duration was 0.002
print(f'duration was {end-start}')

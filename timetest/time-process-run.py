import time
import subprocess

start = time.time()
subprocess.run(["python3", "time-process-run-foo.py"])
end = time.time()

# duration was 7.4
# duration was 6
print(f'duration was {end-start}')

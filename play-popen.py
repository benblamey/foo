import subprocess

with subprocess.Popen(["python3","play-async-core.py"],
                      stdout=subprocess.PIPE,
                      stdin=subprocess.PIPE,
                      text=True) as proc:
    i = 0
    while True:
        i = i + 1

        # Read one line of output.
        data = proc.stdout.readline()
        proc.stdout.flush()

        line = data.rstrip()
        print(line)

        proc.stdin.write(f'foo {i}\n')
        proc.stdin.flush()

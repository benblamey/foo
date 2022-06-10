import asyncio

async def run():
    i = 0
    proc = await asyncio.create_subprocess_shell(
        'python3 play-async-core.py',
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT)

    while True:
        i = i + 1
        proc.stdin.write(f'foo {i}\n'.encode('ascii'))
        # Read one line of output.
        data = await proc.stdout.readline()
        line = data.decode('ascii').rstrip()
        print(line)

    # Wait for the subprocess exit.
    await proc.wait()
    return line


asyncio.run(run())
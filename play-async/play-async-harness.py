import asyncio

async def foo():
    proc = await asyncio.create_subprocess_shell(
        'python3 play-async-core.py',
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    return proc

async def run():
    i = 0


    while True:
        proc.stdin.write(f'foo {i}\n'.encode('ascii'))
        # Read one line of output.
        data = await proc.stdout.readline()
        line = data.decode('ascii').rstrip()
        print(line)
        i = i + 1

    # Wait for the subprocess exit.
    await proc.wait()
    return line


proc = asyncio.wait(foo())
asyncio.run(run())
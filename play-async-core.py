import sys

print('hej.')
while True:
    foo = sys.stdin.readline().rstrip()
    #sys.stdin.flush()

    print(f'input was {foo}.', flush=True)



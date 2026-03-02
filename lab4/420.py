g = 0  # global variable

def outer(commands):
    n = 0  # outer variable

    def inner():
        nonlocal n
        global g

        for cmd in commands:
            scope, val = cmd.split()
            val = int(val)

            if scope == "global":
                g += val
            elif scope == "nonlocal":
                n += val
            elif scope == "local":
                x = val  # local variable, does not affect g or n

        return n

    n = inner()
    return n

# Read input
m = int(input())
commands = [input() for _ in range(m)]

n_final = outer(commands)
print(g, n_final)
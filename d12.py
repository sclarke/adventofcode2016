from collections import defaultdict

test_input = ("cpy 41 a\n",
              "inc a\n",
              "inc a\n",
              "dec a\n",
              "jnz a 2\n",
              "dec a")

with open('d12.txt') as f:
    raw_input = f.readlines()


registers = defaultdict(int)
registers['c'] = 1  # part 2


def cpy(j, k):
    registers[k] = int(j) if j.isdecimal() else registers[j]


def inc(j):
    registers[j] += 1


def dec(j):
    registers[j] -= 1


pointer = 0


def jnz(j, k):
    global pointer
    if (j.isdecimal() and int(j) == 0) or (j in ('a', 'b', 'c', 'd') and registers[j] == 0):
        pointer += 1
    else:
        pointer += int(k)

commands = {
    'cpy': cpy,
    'inc': inc,
    'dec': dec,
    'jnz': jnz,
}

while pointer < len(raw_input):
    try:
        cmd, *par = raw_input[pointer].split()
    except IndexError:
        break
    commands[cmd](*par)
    if cmd != 'jnz':
        pointer += 1

    # print(cmd, par, pointer, registers)

print(registers)

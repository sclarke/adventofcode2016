
test_input = ("cpy 2 a\n"
              "tgl a\n"
              "tgl a\n"
              "tgl a\n"
              "cpy 1 a\n"
              "dec a\n"
              "dec a".splitlines())

puzzle_input = ("cpy a b\n"
                "dec b\n"
                "cpy a d\n"
                "cpy 0 a\n"
                "cpy b c\n"
                "inc a\n"
                "dec c\n"
                "jnz c -2\n"
                "dec d\n"
                "jnz d -5\n"
                "dec b\n"
                "cpy b c\n"
                "cpy c d\n"
                "dec d\n"
                "inc c\n"
                "jnz d -2\n"
                "tgl c\n"
                "cpy -16 c\n"
                "jnz 1 c\n"
                "cpy 99 c\n"
                "jnz 77 d\n"
                "inc a\n"
                "inc d\n"
                "jnz d -2\n"
                "inc c\n"
                "jnz c -5\n".splitlines())


registers = {k: 0 for k in 'a b c d'.split()}
registers['a'] = 7  # part 1
registers['a'] = 12  # part 2


def cpy(j, k):
    registers[k] = registers[j] if j in 'a b c d'.split() else int(j)


def inc(j):
    registers[j] += 1


def dec(j):
    registers[j] -= 1


pointer = 0


def jnz(j, k):
    global pointer
    if (j.isdecimal() and int(j) == 0) or (j in ('a', 'b', 'c', 'd') and registers[j] == 0):
        pointer += 1
        return
    elif k in ('a', 'b', 'c', 'd'):
        offset = registers[k]
    else:
        offset = int(k)

    pointer += offset


def toggle(cmd):
    cmd_list = cmd.split()
    if len(cmd_list) == 3:
        if cmd_list[0] == 'jnz':
            cmd_list[0] = 'cpy'
        else:
            cmd_list[0] = 'jnz'
    elif len(cmd_list) == 2:
        if cmd_list[0] == 'inc':
            cmd_list[0] = 'dec'
        else:
            cmd_list[0] = 'inc'
    else:
        raise NotImplementedError

    return ' '.join(cmd_list)


def tgl(j):
    global pointer
    if j in ('a', 'b', 'c', 'd'):
        offset = registers[j]
    else:
        offset = int(j)

    try:
        program[pointer + offset] = toggle(program[pointer + offset])
    except IndexError:
        pass


commands = {
    'cpy': cpy,
    'inc': inc,
    'dec': dec,
    'jnz': jnz,
    'tgl': tgl,
}

pointer_hist = list()
program = puzzle_input.copy()
while pointer < len(program):
    try:
        pointer_hist.append(pointer)
        cmd, *par = program[pointer].split()
    except IndexError:
        break
    if pointer == 9:
        # by inspection, instructions 4 to 9 are computing b * d. Could expand this further; looks like the commands
        # 0 to 19 are calculating a! once the toggles are accounted for.
        registers['a'] += registers['b'] * registers['d']
        registers['d'] = 0
    commands[cmd](*par)
    if cmd != 'jnz':
        pointer += 1

    # print(cmd, par, pointer, registers)

print(registers)

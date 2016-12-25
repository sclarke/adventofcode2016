from itertools import count

puzzle_input = ('cpy a d\n'
                'cpy 7 c\n'
                'cpy 365 b\n'
                'inc d\n'
                'dec b\n'
                'jnz b -2\n'
                'dec c\n'
                'jnz c -5\n'
                'cpy d a\n'
                'jnz 0 0\n'
                'cpy a b\n'
                'cpy 0 a\n'
                'cpy 2 c\n'
                'jnz b 2\n'
                'jnz 1 6\n'
                'dec b\n'
                'dec c\n'
                'jnz c -4\n'
                'inc a\n'
                'jnz 1 -7\n'
                'cpy 2 b\n'
                'jnz c 2\n'
                'jnz 1 4\n'
                'dec b\n'
                'dec c\n'
                'jnz 1 -4\n'
                'jnz 0 0\n'
                'out b\n'
                'jnz a -19\n'
                'jnz 1 -21\n')

puzzle_input = [line.split() for line in puzzle_input.splitlines()]


def cpy(j, k): registers[k] = registers[j] if j in 'abcd' else int(j)


def inc(j): registers[j] += 1


def dec(j): registers[j] -= 1


def jnz(j, k):
    global pointer
    if (j in 'abcd' and registers[j] == 0) or j == '0':
        pointer += 1
    elif k in 'abcd':
        pointer += registers[k]
    else:
        pointer += int(k)


def toggle(cmd_list):
    if len(cmd_list) == 3:
        cmd_list[0] = 'cpy' if cmd_list[0] == 'jnz' else 'jnz'
    elif len(cmd_list) == 2:
        cmd_list[0] = 'dec' if cmd_list[0] == 'inc' else 'inc'
    else:
        raise NotImplementedError

    return cmd_list


def tgl(j):
    global pointer
    offset = registers[j] if j in 'abcd' else int(j)
    try:
        program[pointer + offset] = toggle(program[pointer + offset])
    except IndexError:
        pass


def out(j): return registers[j] if j in 'abcd' else int(j)


commands = dict(cpy=cpy, inc=inc, dec=dec, jnz=jnz, tgl=tgl, out=out)
observation_length = 100
pointer_max = len(puzzle_input)
for i in count():
    output = []
    output_length = 0  # may as well just track this length manually to avoid calling len() so much.
    pointer = 0
    registers = dict(a=i, b=0, c=0, d=0)
    program = puzzle_input.copy()  # in case there are any toggles present, make a fresh copy
    while pointer < pointer_max and output_length < observation_length:
        # Watch the first {observation_length} charaters returned
        cmd, *par = program[pointer]
        out_val = commands[cmd](*par)
        if cmd == 'out':
            output.append(out_val)
            output_length += 1
            try:
                if output[-1] == output[-2]:
                    # Give up on this sequence early if it's already failed to toggle
                    break
            except IndexError:
                # The first time through there's no output[-2] to compare against
                pass
        if cmd != 'jnz':
            pointer += 1
    if output_length == observation_length:
        print('Working Code!: Initial value: {}'.format(i))
        break
    else:
        print('   failed sequence #{:4}, after {} characters'.format(i, len(output)))

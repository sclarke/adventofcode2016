
def next_row(r):
    return ['.'] + ['^' if r[i-1] != r[i+1] else '.' for i in range(1, len(r)-1)] + ['.']


def tiles_formatter(row_list):
    row_strings = [''.join(row[1:-1]) for row in row_list]
    return '\n'.join(row_strings)


def gen_tiles(first_row, length=3):
    rows = [first_row, ]
    while len(rows) < length:
        rows.append(next_row(rows[-1]))
    return rows


sample_input = ['.'] + list('..^^.') + ['.']

tiles = tiles_formatter(gen_tiles(sample_input))
print('Total traps: {}'.format(tiles.count('.')), '\n' + tiles, end='\n\n')


sample_input = ['.'] + list('.^^.^.^^^^') + ['.']

tiles = tiles_formatter(gen_tiles(sample_input, length=10))
print('Total traps: {}'.format(tiles.count('.')), '\n' + tiles, end='\n\n')


sample_input = ['.'] + list('^^^^......^...^..^....^^^.^^^.^.^^^^^^..^...^^...^'
                            '^^.^^....^..^^^.^.^^...^.^...^^.^^^.^^^^.^^.^..^.^') + ['.']

tiles = tiles_formatter(gen_tiles(sample_input, length=40))
print('Total traps: {}'.format(tiles.count('.')), '\n' + tiles, end='\n\n')

tiles = tiles_formatter(gen_tiles(sample_input, length=400000))
print('Total traps: {}'.format(tiles.count('.')), end='\n\n')

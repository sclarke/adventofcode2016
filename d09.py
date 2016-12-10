# ### Part 1
# out = ''
# with open('d09.txt') as f:
#     while True:
#         c = f.read(1)
#         if not c:
#             break
#
#         if c == '(':
#             pattern = ''
#             while True:
#                 pattern_char = f.read(1)
#                 if pattern_char == ')':
#                     break
#                 else:
#                     pattern += pattern_char
#
#             length, count = (int(n) for n in pattern.split('x'))
#             repstr = f.read(length)
#             out += repstr * count
#
#         else:
#             out += c
#
# print(len(out), end='\n\n')

from collections import deque


class Reader():
    def __init__(self, file_handle):
        self.fh = file_handle
        self.queue = deque()

    def read(self, length):
        char = ''
        for _ in range(length):
            try:
                char += self.queue.popleft()
            except IndexError:
                char += self.fh.read(1)
        return char

    def write(self, seq):
        self.queue.extendleft(reversed(seq))


size = 0
with open('d09.txt') as f:
    filequeue = Reader(f)
    while True:
        c = filequeue.read(1)
        if not c:
            break

        if c == '(':
            pattern = ''
            while True:
                pattern_char = filequeue.read(1)
                if pattern_char == ')':
                    break
                else:
                    pattern += pattern_char

            length, count = (int(n) for n in pattern.split('x'))
            repstr = filequeue.read(length)  # throw away this string now
            filequeue.write(repstr*count)

        else:
            size += 1

        if size % 100000 == 0:
            print(size // 100000, len(filequeue.queue), f.tell())

print(size, end='\n\n')

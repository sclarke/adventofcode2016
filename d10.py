from collections import defaultdict
from functools import reduce
from operator import mul

import attr
import re


@attr.s
class Bot(object):
    low_dest_type = attr.ib()
    low_dest_id = attr.ib(convert=int)
    high_dest_type = attr.ib()
    high_dest_id = attr.ib(convert=int)
    chips = attr.ib(default=attr.Factory(list))


@attr.s
class Output(object):
    chips = attr.ib(default=attr.Factory(list))


with open('d10.txt') as f:
    instructions = sorted(line.strip() for line in f)


def bot_instruction_parser(bot_ins):
    pattern = re.compile('bot (?P<id>\d+) gives '
                         'low to (?P<low_dest_type>\w+) (?P<low_dest_id>\d+) and '
                         'high to (?P<high_dest_type>\w+) (?P<high_dest_id>\d+)')

    bot_dict = pattern.match(bot_ins).groupdict()
    bot_id = int(bot_dict.pop('id'))
    return bot_id, Bot(**bot_dict)


def init_instruction_parser(init_ins):
    pattern = re.compile('value (?P<chip_id>\d+) goes to bot (?P<bot_id>\d+)')
    return tuple(int(n) for n in pattern.match(init_ins).groups())


bot_instructions = [line for line in instructions if line.startswith('bot ')]
bots = dict(bot_instruction_parser(instruct) for instruct in bot_instructions)

initial_locations = [init_instruction_parser(line) for line in instructions if line.startswith('value ')]
for chip, bot in initial_locations:
    bots[bot].chips.append(chip)

outputs = defaultdict(Output)
dest = {
    'bot': bots,
    'output': outputs,
}

while True:
    active_bots = {bot_id: bot for bot_id, bot in bots.items() if len(bot.chips) == 2}
    if not active_bots:
        break

    for bot_id, bot in active_bots.items():
        low_chip, high_chip = sorted(bot.chips)
        if (low_chip, high_chip) == (17, 61):
            print(bot_id, bot)

        dest[bot.low_dest_type][bot.low_dest_id].chips.append(low_chip)
        dest[bot.high_dest_type][bot.high_dest_id].chips.append(high_chip)

        del bot.chips[:]

print(reduce(mul, (outputs[n].chips[0] for n in (0, 1, 2))))

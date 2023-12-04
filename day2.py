from functools import partial, reduce

from day2_input import real_input

example_input = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

available = dict(red=12, green=13, blue=14)

def is_game_possible(rounds: str):
    return all(map(is_round_possilbe, rounds.split(';')))


def is_round_possilbe(r: str):
    return all(map(is_pull_possible, r.split(',')))

def is_pull_possible(pull: str):
    number, color = pull.split()
    return int(number) <= available[color]

def gameScore(game: str):
    gameNumber, rounds = game.split(':')
    return int(gameNumber[5:]) if is_game_possible(rounds) else 0


def part1(all_input = example_input):
    return sum(map(partial(gameScore), all_input.splitlines()))


def get_required_power(game: str):
    mins = reduce(maxes, map(get_required_for_round, game.split(':')[1].split(';')))
    return mins["red"]*mins["green"]*mins["blue"]


def maxes(dict1, dict2):
    return dict(
        red=max(dict1.get("red", 0), dict2.get("red", 0)),
        blue=max(dict1.get("blue", 0), dict2.get("blue", 0)),
        green=max(dict1.get("green", 0), dict2.get("green", 0))
    )


def get_required_for_round(r: str):
    return reduce(maxes, map(get_required_for_pull, r.split(',')))


def get_required_for_pull(p: str):
    number, color = p.split()
    return { color: int(number) }


def part2(all_input = example_input):
    return sum(map(get_required_power, all_input.splitlines()))


print(part1(real_input), part2(real_input))


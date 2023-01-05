from math import lcm

import os
os.system('')

# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797exi


def input_int(text=''):
    while not (inp := input(text)).isdigit():
        print('\x1b[1A\x1b[2K invalid digit')
    return int(inp)


def select_folder(path='.'):
    folders = []
    for root, dirs, files in os.walk(path):
        if not dirs:
            folders.append(root)
    for i, folder in enumerate(folders):
        print(f'{i}: {folder}')
    i = input_int(f'select a folder ({0}-{len(folders) - 1}): ')
    return folders[i]


def iter_path(fromx: int, fromy: int, tox: int, toy: int):
    if fromx == tox and fromy == toy:
        return
    dy = toy - fromy
    dx = tox - fromx
    if dy and dx:
        step = lcm(abs(dx), abs(dy))
    else:
        step = max(abs(dx), abs(dy))
    stepx = dx // step
    stepy = dy // step
    fromy += stepy
    fromx += stepx
    while (fromy != toy or fromx != tox):
        yield fromx, fromy
        fromy += stepy
        fromx += stepx
    return

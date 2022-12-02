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

# pyinstaller --onefile --icon=1.ico pip_update.py
import subprocess
import platform
import os

os.system("")

py_ver = subprocess.run('python --version', stdout=subprocess.PIPE, encoding='utf-8').stdout
print(f'\n{platform.node()}, {platform.system()}-{platform.release()}')
print(f'Updating modules {py_ver}', end='')
major, minor = py_ver.split()[1].split('.')[:2]
VER = f'py -{major}.{minor} -m'
# VER = "py -3.7-32 -m"
# VER = "py -3.7-64 -m"
# VER = "py -3.7 -m"

path = os.path.join(os.path.dirname(__file__), 'pipignore.txt')
with open(path) as f:
    not_update = f.read().split()
"""
# Определяем имена модулей, запрещенных для обновления
not_update = [
    'cloudpickle', 'tensorflow-probability', 'gast', 'tensorflow',
    'tensorflow-estimator', 'tensorboard', 'dlib', 'scipy',
    'VideoCapture', 'PyAudio', 'torch', 'torchvision', 'pocketsphinx',
    'PyOpenGL', 'PyOpenGL-accelerate', 'scikit-learn',
    'torch', 'torchvision'
]
"""
ORANGE, RED, GREEN, BLUE, RESET, RESET_ALL, UP = \
    '\033[38;2;255;150;0m', '\033[31m', '\033[32m', '\033[34m', \
    '\033[39m', '\033[0m', '\033[F\033[K'


def check():
    print(f'{GREEN}START{RESET}')
    # Определяем имена модулей, требующих обновления
    cmd = eval(subprocess.run(
        f'{VER} pip list -o --format=json',  # shell=True,
        stdout=subprocess.PIPE).stdout)
    if len(cmd) == 0:
        return False
    # df = pandas.DataFrame(cmd)  # import pandas
    c = max(cmd, key=len)
    list_length = [0] * len(c)
    print(GREEN)
    for i in range(len(cmd)):
        for j, couple in enumerate(cmd[i].items()):
            length = max(len(couple[0]), len(couple[1]))
            if list_length[j] < length:
                list_length[j] = length
    for i, key in enumerate(c.keys()):
        print(key.replace('_', ' '), end=(list_length[i] - len(key) + 2) * ' ')
    print(BLUE)
    for i in range(len(c)):
        print(list_length[i] * '-', end='  ')
    print(RESET)
    for i in range(len(cmd)):
        for j, val in enumerate(cmd[i].values()):
            print(
                f'{RESET if val not in not_update else ORANGE}{val}',
                end=(list_length[j] - len(val) + 2) * ' ')
        print()
    return cmd


def updates():
    # Обновляем
    if result:
        query = input('\ncontinue? (y/n) ')
        if query == 'y':
            print(f'{UP}continue?', 'yes')
            print(f'\n{GREEN}UPDATES')
            try:
                for name in result:
                    if name["name"] in not_update:
                        print(f'{ORANGE}{name["name"]} - skipped without update')
                    else:
                        print(f'{RESET}{name["name"].center(70, "-")}')
                        subprocess.run(f'{VER} pip install -U {name["name"]}')
                print(f'{GREEN}END OF UPDATES')
                # Убеждаемся, что установленные пакеты имеют совместимые зависимости
                print(f'\n{BLUE}[DEPENDENCE]{RESET}')
                subprocess.run(f'{VER} pip check')
            except Exception as e:
                print(f'{RED}[ERROR] {e}')
        else:
            print(f'{UP}continue?', 'no')
    else:
        print(f'{GREEN}NO UPDATES')


if __name__ == "__main__":
    result = check()
    updates()

    print(f'\n{ORANGE}press any key to exit{RESET_ALL}')
    if os.name == 'nt':
        import msvcrt
        _key_ = ord(msvcrt.getch())
        if _key_:
            print('[EXIT]')

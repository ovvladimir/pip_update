# pyinstaller --onefile --icon=1.ico pip_upgrade.py
import subprocess
import msvcrt
import platform
if platform.release() == '10' and platform.version() >= '10.0.14393':
    from ctypes import windll
    windll.kernel32.SetConsoleMode(windll.kernel32.GetStdHandle(-11), 7)
else:
    from colorama import init
    init(autoreset=False)

# ver = "py -3.7-32 -m"
# ver = "py -3.7-64 -m"
# ver = "py -3.8 -m"
py_ver = subprocess.run('python --version', stdout=subprocess.PIPE, encoding='utf-8').stdout
print(f'\nModules Update {py_ver}', end='')
major, minor = py_ver.split()[1].split('.')[:2]
ver = f'py -{major}.{minor} -m'

# Определяем имена модулей, запрещенных для обновления
not_update = ['cloudpickle', 'tensorflow-probability', 'gast', 'tensorflow',
              'tensorflow-estimator', 'tensorboard', 'dlib', 'numpy',
              'VideoCapture', 'PyAudio', 'torch', 'torchvision', 'pocketsphinx',
              'PyOpenGL', 'PyOpenGL-accelerate', 'scikit-learn']
'P.S. в scikit-learn с версии 0.22 закрыты некоторые общедоступные инструменты'

ORANGE, RED, GREEN, BLUE, RESET, RESET_ALL = \
    '\033[38;2;255;150;0m', '\033[31m', '\033[32m', '\033[34m', '\033[39m', '\033[0m'


def check(VER):
    print(f'{GREEN}START{RESET}')
    # Определяем имена модулей, требующих обновления (shell=True для Linux)
    cmd = eval(subprocess.run(
        f'{VER} pip list -o --format=json',  # shell=True,
        stdout=subprocess.PIPE).stdout)
    # df = pandas.DataFrame(cmd)  # import pandas
    list_length = [0] * len(cmd[0])
    print(GREEN)
    for i in range(len(cmd)):
        for j, couple in enumerate(cmd[i].items()):
            length = max(len(couple[0]), len(couple[1]))
            if list_length[j] < length:
                list_length[j] = length
    for i, key in enumerate(cmd[0].keys()):
        print(key, end=(list_length[i] - len(key) + 2) * ' ')
    print(BLUE)
    for i in range(len(cmd[0])):
        print(list_length[i] * '-', end='  ')
    print(RESET)
    for i in range(len(cmd)):
        for j, val in enumerate(cmd[i].values()):
            print(
                f'{RESET if val not in not_update else ORANGE}{val}',
                end=(list_length[j] - len(val) + 2) * ' ')
        print()
    return cmd


def updates(VER):
    # Обновляем
    if len(result) != 0:
        print(f'\n{GREEN}UPDATES')
        try:
            for name in result:
                if name["name"] in not_update:
                    print(f'{ORANGE}{name["name"]} - skipped without update')
                else:
                    print(f"{RESET}{'-' * 22}", name["name"], '-' * 22)
                    subprocess.run(f'{VER} pip install -U {name["name"]}')
            print(f'{GREEN}END OF UPDATES')
        except Exception as e:
            print(f'{RED}[ERROR] {e}')
    else:
        print(f'{GREEN}NO UPDATES')

    # Убеждаемся, что установленные пакеты имеют совместимые зависимости
    print(f'\n{BLUE}[DEPENDENCE]{RESET}')
    subprocess.run(f'{VER} pip check')


if __name__ == "__main__":
    result = check(ver)
    query = input('\ncontinue? (y/n) ')
    if query == 'y':
        print('\033[F\033[Kcontinue?', 'yes')
        updates(ver)
    else:
        print('\033[F\033[Kcontinue?', 'no')

    print(f'\n{ORANGE}press any key to exit{RESET_ALL}')
    _key_ = ord(msvcrt.getch())
    if _key_:
        print('[EXIT]')

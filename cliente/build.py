import PyInstaller.__main__ as PI


def main():
    PI.run([
        'gui.py',
        '--onefile',
        '--windowed',
        '--specpath',
        'build',
        '-n',
        'Cliente'
    ])


if __name__ == "__main__":
    main()

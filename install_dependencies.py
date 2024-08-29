import os
import subprocess
import sys

def install(package)
    subprocess.check_call([sys.executable, -m, pip, install, package])

def main()
    dependencies = [
        requests,
        beautifulsoup4,
        lxml,
        playwright
    ]

    print(Inizio installazione delle dipendenze...)

    for package in dependencies
        try
            install(package)
            print(f'{package}' installato con successo.)
        except subprocess.CalledProcessError as e
            print(fErrore nell'installazione di '{package}' {e})

    # Installazione dei browser necessari per Playwright
    try
        subprocess.check_call([sys.executable, -m, playwright, install])
        print(Browser Playwright installati con successo.)
    except subprocess.CalledProcessError as e
        print(fErrore nell'installazione dei browser Playwright {e})

    print(Tutte le dipendenze sono state installate.)

if __name__ == __main__
    main()

import subprocess
import sys

# Запуск функции в отдельном процессе
subprocess.Popen([sys.executable, 'main.py'])
sys.exit()
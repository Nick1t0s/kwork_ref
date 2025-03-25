import subprocess
import sys

# Запуск функции в отдельном процессе
subprocess.Popen([sys.executable, '/root/refBot/kwork_ref/main.py'])
sys.exit()
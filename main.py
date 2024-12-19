import sys
import subprocess

try:
    subprocess.check_call([sys.executable,
        "-m", "pip", "install", "-r", "requirements.txt"])
except subprocess.CalledProcessError:
    print("Error importing modules")

from defendish import Defendish

if __name__ == "__main__":
    d_game = Defendish()
    d_game.run_game()
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HARVEST_DIR = ROOT / "CinnHarvest-backend"
ORACLE_DIR = ROOT / "CinnOracle_backend"


def run_setup_harvest():
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "uv"],
        cwd=HARVEST_DIR,
        check=True,
    )
    subprocess.run(["uv", "sync"], cwd=HARVEST_DIR, check=True)


def run_setup_oracle():
    venv_dir = ORACLE_DIR / ".venv"
    venv_python = venv_dir / "Scripts" / "python.exe"

    if not venv_python.exists():
        subprocess.run([sys.executable, "-m", "venv", ".venv"], cwd=ORACLE_DIR, check=True)

    subprocess.run(
        [str(venv_python), "-m", "pip", "install", "-r", "requirements.txt"],
        cwd=ORACLE_DIR,
        check=True,
    )
    return venv_python


def main():
    run_setup_harvest()
    venv_python = run_setup_oracle()

    harvest_proc = subprocess.Popen(
        ["uv", "run", "python", "main.py"],
        cwd=HARVEST_DIR,
    )

    oracle_proc = subprocess.Popen(
        [str(venv_python), "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=ORACLE_DIR,
    )

    try:
        harvest_proc.wait()
        oracle_proc.wait()
    except KeyboardInterrupt:
        pass
    finally:
        for proc in (harvest_proc, oracle_proc):
            if proc.poll() is None:
                proc.terminate()


if __name__ == "__main__":
    main()

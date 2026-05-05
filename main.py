import subprocess
import sys


def run_streamlit():
    """Launch the Streamlit dashboard."""
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "Dashboard/app.py"],
        check=True,
    )


if __name__ == "__main__":
    run_streamlit()
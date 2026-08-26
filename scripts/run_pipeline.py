import subprocess
import sys
import logging

# initialise
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

from paths import PIPELINE_ROOT

scripts = [
    PIPELINE_ROOT / "generate.py",
    PIPELINE_ROOT / "extract.py",
    PIPELINE_ROOT / "transform.py",
    PIPELINE_ROOT / "aggregate.py",
    PIPELINE_ROOT / "stats.py",
]

for script in scripts:
    
    print(f"Running {script}...")

    subprocess.run(
        [sys.executable, str(script)],
        check=True,
    )

    print(f"Completed {script}")

logging.info("✅ Pipeline completed successfully")
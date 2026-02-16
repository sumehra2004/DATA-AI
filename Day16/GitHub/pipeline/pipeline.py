import os
import shutil
import subprocess
import sys
import logging

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
BUILD_DIR = os.path.join(PROJECT_ROOT, "build")
DIST_DIR = os.path.join(PROJECT_ROOT, "dist")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(BUILD_DIR, exist_ok=True)
os.makedirs(DIST_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "pipeline.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run(cmd):
    logging.info("RUN: %s", " ".join(cmd))
    subprocess.run(cmd, cwd=PROJECT_ROOT, check=True)

def install_deps():
    run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def run_pytest():
    run([sys.executable, "-m", "pytest", "tests"])

def run_unittest():
    run([sys.executable, "-m", "unittest", "discover", "tests"])

def build_zip():
    # clean build dir
    for name in os.listdir(BUILD_DIR):
        path = os.path.join(BUILD_DIR, name)
        if os.path.isfile(path):
            os.remove(path)

    shutil.copy(os.path.join(PROJECT_ROOT, "app", "calculator.py"), BUILD_DIR)
    shutil.make_archive(os.path.join(DIST_DIR, "app"), "zip", BUILD_DIR)

def deploy():
    # create deploy.zip at root (artifact)
    shutil.copy(os.path.join(DIST_DIR, "app.zip"), os.path.join(PROJECT_ROOT, "deploy.zip"))

def main():
    logging.info("Pipeline started")
    install_deps()
    run_pytest()
    run_unittest()
    build_zip()
    deploy()
    logging.info("Pipeline finished")
    print("✅ Pipeline finished successfully")

if __name__ == "__main__":
    main()

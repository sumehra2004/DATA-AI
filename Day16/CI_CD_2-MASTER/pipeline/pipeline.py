import subprocess
import os
import shutil
import logging
import sys

# PROJECT_ROOT = folder one level above this file (because this file is in pipeline/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Ensure project root is in PYTHONPATH so 'app' can be imported
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.makedirs(os.path.join(PROJECT_ROOT, "logs"), exist_ok=True)

logging.basicConfig(
    filename=os.path.join(PROJECT_ROOT, "logs", "pipeline.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def install_dependencies():
    logging.info("Installing dependencies")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        check=True,
        cwd=PROJECT_ROOT
    )

def run_pytest():
    logging.info("Running pytest")
    subprocess.run(
        [sys.executable, "-m", "pytest", "tests"],
        check=True,
        cwd=PROJECT_ROOT
    )

def run_unittest():
    logging.info("Running unittest")
    subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "tests"],
        check=True,
        cwd=PROJECT_ROOT
    )

def build_project():
    logging.info("Building project")
    build_dir = os.path.join(PROJECT_ROOT, "build")
    dist_dir = os.path.join(PROJECT_ROOT, "dist")

    os.makedirs(build_dir, exist_ok=True)
    os.makedirs(dist_dir, exist_ok=True)

    # clean build dir (keep it simple)
    for name in os.listdir(build_dir):
        path = os.path.join(build_dir, name)
        if os.path.isfile(path):
            os.remove(path)

    shutil.copy(os.path.join(PROJECT_ROOT, "app", "calculator.py"), build_dir)

    shutil.make_archive(
        os.path.join(dist_dir, "app"),
        "zip",
        build_dir
    )

def deploy_project():
    logging.info("Deploying project")
    shutil.copy(
        os.path.join(PROJECT_ROOT, "dist", "app.zip"),
        os.path.join(PROJECT_ROOT, "deploy.zip")
    )

def main():
    logging.info("Pipeline started")
    install_dependencies()
    run_pytest()
    run_unittest()
    build_project()
    deploy_project()
    logging.info("Pipeline completed successfully")
    print("✅ Pipeline completed successfully")

if __name__ == "__main__":
    main()

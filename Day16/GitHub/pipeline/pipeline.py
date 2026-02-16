import os
import shutil
import subprocess
import sys
import logging

# -------------------- CONFIG --------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
BUILD_DIR = os.path.join(PROJECT_ROOT, "build")
DIST_DIR = os.path.join(PROJECT_ROOT, "dist")

# Ensure directories exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(BUILD_DIR, exist_ok=True)
os.makedirs(DIST_DIR, exist_ok=True)

# -------------------- LOGGING --------------------
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "pipeline.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------- HELPER --------------------
def run(cmd, cwd=PROJECT_ROOT):
    """Run a shell command and log it."""
    logging.info("RUN: %s", " ".join(cmd))
    try:
        subprocess.run(cmd, cwd=cwd, check=True)
    except subprocess.CalledProcessError as e:
        logging.error("Command failed: %s", e)
        print(f"❌ Command failed: {' '.join(cmd)}. Check logs.")
        sys.exit(1)

# -------------------- PIPELINE STEPS --------------------
def install_deps():
    """Install Python dependencies from requirements.txt"""
    req_file = os.path.join(PROJECT_ROOT, "requirements.txt")
    if os.path.exists(req_file):
        run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        logging.warning("No requirements.txt found, skipping dependency installation.")

def run_pytest():
    """Run pytest tests"""
    test_dir = os.path.join(PROJECT_ROOT, "tests")
    if os.path.exists(test_dir):
        run([sys.executable, "-m", "pytest", "tests"])
    else:
        logging.warning("No 'tests' directory found, skipping pytest.")

def run_unittest():
    """Run unittest discovery"""
    test_dir = os.path.join(PROJECT_ROOT, "tests")
    if os.path.exists(test_dir):
        run([sys.executable, "-m", "unittest", "discover", "tests"])
    else:
        logging.warning("No 'tests' directory found, skipping unittest.")

def clean_build():
    """Clean the build directory"""
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    os.makedirs(BUILD_DIR)

def build_zip():
    """Build a zip artifact containing the full app/ directory"""
    app_src = os.path.join(PROJECT_ROOT, "app")
    if not os.path.exists(app_src):
        logging.error("'app' directory not found. Cannot build zip.")
        print("❌ 'app' directory not found. Cannot build zip.")
        sys.exit(1)

    clean_build()
    shutil.copytree(app_src, os.path.join(BUILD_DIR, "app"), dirs_exist_ok=True)

    zip_path = os.path.join(DIST_DIR, "app")
    shutil.make_archive(zip_path, "zip", BUILD_DIR)
    logging.info("Build zip created at: %s.zip", zip_path)

def deploy():
    """Deploy the artifact to project root"""
    src = os.path.join(DIST_DIR, "app.zip")
    dst = os.path.join(PROJECT_ROOT, "deploy.zip")
    if os.path.exists(src):
        shutil.copy(src, dst)
        logging.info("Deploy artifact copied to: %s", dst)
        print(f"✅ Deployment artifact ready: {dst}")
    else:
        logging.error("Build artifact not found, cannot deploy.")
        print("❌ Build artifact not found, cannot deploy.")
        sys.exit(1)

# -------------------- MAIN PIPELINE --------------------
def main():
    logging.info("Pipeline started")
    print("🚀 Pipeline started...")

    install_deps()
    run_pytest()
    run_unittest()
    build_zip()
    deploy()

    logging.info("Pipeline finished successfully")
    print("🎉 Pipeline finished successfully!")

# -------------------- ENTRY POINT --------------------
if __name__ == "__main__":
    main()

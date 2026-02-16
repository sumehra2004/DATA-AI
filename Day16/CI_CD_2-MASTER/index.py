import subprocess

def run_tests():
    result = subprocess.run(["pytest"], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Tests passed")
    else:
        print("Tests failed")
        print(result.stdout)

run_tests()

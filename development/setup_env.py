# Development Environment Setup
# This script helps initialize the development environment
import subprocess
import sys
import os

def run_command(command):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(command, shell=True, check=True, 
                               capture_output=True, text=True)
        print(f"✓ Command succeeded: {command}")
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"✗ Command failed: {command}")
        print(f"Error: {e.stderr}")
        return None

def main():
    print("=== Development Environment Setup ===")
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    venv_path = os.path.join(script_dir, "venv")
    activate_script = os.path.join(venv_path, "bin", "activate")
    
    print(f"Virtual environment path: {venv_path}")
    print(f"Activate script exists: {os.path.exists(activate_script)}")
    
    # Test if we can run python from venv
    try:
        result = run_command(f"{venv_path}/bin/python --version")
        if result:
            print(f"Python version from venv: {result.strip()}")
    except:
        pass
    
    # Install loguru if not already installed
    print("Installing loguru...")
    run_command(f"{venv_path}/bin/pip install loguru")
    
    # Check if node is available
    print("Checking Node.js...")
    node_result = run_command("node --version")
    npm_result = run_command("npm --version")
    
    print("=== Setup Complete ===")

if __name__ == "__main__":
    main()
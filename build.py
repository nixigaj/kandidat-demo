#!/usr/bin/env python3

import argparse
import os
import platform
import shutil
import subprocess
import sys


def get_platform_string():
	system = platform.system().lower()
	if "windows" in system:
		os_name = "windows"
	elif "darwin" in system:
		os_name = "macos"
	elif "linux" in system:
		os_name = "linux"
	else:
		raise ValueError(f"Unsupported OS: {system}")

	arch = platform.machine().lower()
	if arch in ["x86_64", "amd64"]:
		arch_name = "x86-64"
	elif arch in ["arm64", "aarch64"]:
		arch_name = "aarch64"
	else:
		raise ValueError(f"Unsupported architecture: {arch}")

	return f"{os_name}-{arch_name}"


def build():
	print(f"Building for platform: {get_platform_string()}")

	if not os.path.exists(".venv"):
		print("Creating virtual environment...")
		subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)

	# Determine platform-specific paths
	venv_python = os.path.join(".venv", "Scripts" if os.name == "nt" else "bin", "python")

	print("Installing requirements...")
	subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

	print("Building with maturin...")
	subprocess.run([venv_python, "-m", "maturin", "develop", "--release"], check=True)

	print("Building executable with PyInstaller...")
	subprocess.run([venv_python, "-m", "PyInstaller", "src/main.py", "--name", "kandidat-demo", "--noconfirm"], check=True)

	print("Creating zip archive...")
	source_dir = os.path.join("dist", "kandidat-demo")
	zip_path = os.path.join("dist", f"kandidat-demo-{get_platform_string()}.zip")

	if sys.platform == "win32":
		subprocess.run(["tar", "-a", "-c", "-f", zip_path, source_dir], check=True)
	else:
		subprocess.run(["zip", "--symlinks", "-r", zip_path, source_dir], check=True)

	print(f"Created {zip_path}")


def clean():
	for dir_path in [".venv", "build", "dist"]:
		if os.path.exists(dir_path):
			print(f"Removing {dir_path}...")
			shutil.rmtree(dir_path)

	print("Removing .so and .dll files in src...")
	for root, dirs, files in os.walk("src"):
		for file in files:
			if file.endswith(".so") or file.endswith(".dll"):
				os.remove(os.path.join(root, file))

	spec_file = "kandidat-demo.spec"
	if os.path.exists(spec_file):
		print(f"Removing {spec_file}...")
		os.remove(spec_file)

	rust_dir = "rust"
	if os.path.exists(rust_dir):
		print("Running cargo clean...")
		subprocess.run(["cargo", "clean"], cwd=rust_dir, shell=(os.name == "nt"))


def main():
	parser = argparse.ArgumentParser(description="Build script for kandidat-demo")
	parser.add_argument(
		"command",
		nargs="?",
		default="build",
		choices=["build", "clean"],
		help="Command to run (build or clean)"
	)
	args = parser.parse_args()

	if args.command == "build":
		build()
	elif args.command == "clean":
		clean()


if __name__ == "__main__":
	main()

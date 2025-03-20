# Kandidat demo

## Requirements
- Git
- Python 3.11+
- pip
- Rust
- Zip (only needs to be installed on Linux)

## Download
```console
git clone https://github.com/nixigaj/kandidat-demo
cd kandidat-demo
```

## Run for development
```console
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
maturin develop  # add --release for optimized build
python src/main.py
```

## Build release
```console
python3 build.py
```

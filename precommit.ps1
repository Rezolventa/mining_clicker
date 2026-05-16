$ErrorActionPreference = "Stop"

python -m isort .
python -m black .

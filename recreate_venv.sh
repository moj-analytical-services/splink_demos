set -exuo pipefail

rm -rf venv/
python3.12 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip

python -m pip install -r requirements.txt
python -m ipykernel install --user --name=splink_demos

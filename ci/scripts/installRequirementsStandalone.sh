# Title : Fichier permettant d'installer les requirements pour les scripts Python en standalone

echo "Installation des requirements pour les scripts Python"
python -m venv .venv
source .venv/bin/activate
pip install -r ../../requirements.txt
echo "Installation terminée."

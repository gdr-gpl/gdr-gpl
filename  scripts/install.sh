#!/bin/bash
set -e

echo "Mise à jour et installation des dépendances..."
sudo apt update
sudo apt install -y git nginx wget

echo "Installation de Hugo v0.148.0..."
if ! command -v hugo &> /dev/null; then
  wget https://github.com/gohugoio/hugo/releases/download/v0.148.0/hugo_extended_0.148.0_Linux-64bit.deb
  sudo dpkg -i hugo_extended_0.148.0_Linux-64bit.deb
  rm hugo_extended_0.148.0_Linux-64bit.deb
fi

echo "Installation terminée."

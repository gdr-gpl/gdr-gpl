## Site GdR GPL <br>
[Site actuel](https://gdr-gpl.cnrs.fr/) <br>
[Site du CNRS](https://mygdr.hosted.lip6.fr/accueilGDR/7/10)

# Déploiement site Hugo sur VM

## Prérequis
- Git, Hugo, Nginx

## Commandes d’installation

```bash
sudo apt update
sudo apt install -y git nginx
wget https://github.com/gohugoio/hugo/releases/download/v0.148.0/hugo_extended_0.148.0_Linux-64bit.deb
sudo dpkg -i hugo_extended_0.148.0_Linux-64bit.deb

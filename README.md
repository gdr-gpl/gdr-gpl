## Site GdR GPL <br>
[Site actuel](https://gdr-gpl.cnrs.fr/) <br>
[Site du CNRS](https://mygdr.hosted.lip6.fr/accueilGDR/7/10)

## Redirections vers documentation

### Pour les utilisateurs  
Consultez la documentation utilisateur ici :  
[docs/utilisateur.md](docs/utilisateur.md)

---

### Pour les techniciens  
Consultez la documentation technique ici :  
[docs/technique.md](docs/technique.md)


# Déploiement site Hugo sur VM

## Prérequis
- Git
- Hugo
- Nginx

## Commandes d’installation

```bash
sudo apt update
sudo apt install -y git nginx
wget https://github.com/gohugoio/hugo/releases/download/v0.148.0/hugo_extended_0.148.0_Linux-64bit.deb
sudo dpkg -i hugo_extended_0.148.0_Linux-64bit.deb

### `install.sh`

Installe les dépendances :

- `git`
- `nginx`
- `hugo v0.148.0` (version spécifique)

```bash
./install.sh

### `deploy.sh`

Déploie ou met à jour le site :

- Clone ou pull le repo GitHub
- Construit le site avec Hugo
- Configure Nginx si nécessaire
- Recharge Nginx

```bash
./deploy.sh
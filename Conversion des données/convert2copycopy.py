import os, re
import xml.etree.ElementTree as ET

import html2text  # Pour convertir HTML vers Markdown
import yaml       # Pour générer le front matter YAML

# Charger le fichier XML d'export WordPress
XML_FILE = "gdrgpl.WordPress.2025-09-03.xml"
tree = ET.parse(XML_FILE)
root = tree.getroot()

# Définition des espaces de noms XML utilisés dans l'export WordPress
ns = {
    "wp": "http://wordpress.org/export/1.2/",           # Éléments WordPress
    "content": "http://purl.org/rss/1.0/modules/content/", # Contenu des articles
    "dc": "http://purl.org/dc/elements/1.1/",            # Dublin Core (métadonnées)
    "excerpt": "http://wordpress.org/export/1.2/excerpt/", # Extraits d'articles
}

# Configuration du convertisseur HTML vers Markdown
h = html2text.HTML2Text()
h.ignore_links = False  # Conserver les liens dans la conversion
h.body_width = 0        # Pas de coupure de ligne automatique (largeur infinie)

# Dictionnaire pour mapper les IDs de posts vers les noms de catégories
post_id_to_category = {}

def tx(el):
    """
    Fonction utilitaire pour extraire le texte d'un élément XML de façon sécurisée.
    Retourne une chaîne vide si l'élément est None ou si le texte est None.
    """
    return el.text if el is not None and el.text is not None else ""

def safe_slug(s, fallback):
    """
    Génère un slug sécurisé pour les noms de fichiers à partir d'une chaîne.
    """
    s = (s or "").strip().lower().replace(" ", "-")
    s = re.sub(r"[^a-z0-9\-._]", "", s)  # Supprimer tous les caractères non autorisés
    return s or fallback

def find_items(xPaths):
    """
    Fonction pour traiter les catégories et termes WordPress.
    Crée les dossiers et mappe les IDs de posts vers les catégories.
    """
    for xPath in xPaths:
        print(f"Items for XPath: {xPath}")
        for item in root.findall(xPath, ns):
            # Extraction des métadonnées des catégories/termes
            term_id = tx(item.find("wp:term_id", ns))
            name = tx(item.find("wp:cat_name", ns)) or tx(item.find("wp:term_name", ns))
            slug = tx(item.find("wp:category_nicename", ns)) or tx(item.find("wp:term_slug", ns))
            parent = tx(item.find("wp:category_parent", ns)) or tx(item.find("wp:term_parent", ns))
            description = tx(item.find("wp:category_description", ns)) or tx(item.find("wp:term_description", ns))
            taxonomy = tx(item.find("wp:term_taxonomy", ns))  # Type de taxonomie (category, tag, etc.)
            
            # Détermination du dossier selon la hiérarchie
            if parent and parent != "0":
                # Trouver le nom du parent
                parent_name = find_parent_name(parent)
                if parent_name:
                    directoryPath = f"content/{parent_name}/{name}"
                else:
                    directoryPath = f"content/{name}"
            else:
                directoryPath = f"content/{name}"
                
            print(f"Création du dossier: {directoryPath}")
            os.makedirs(directoryPath, exist_ok=True)
            
            # Mapper les IDs vers les chemins de dossiers pour les utiliser dans les pages
            post_id_to_category[term_id] = directoryPath

def find_parent_name(parent_id):
    """
    Trouve le nom d'une catégorie parent par son ID
    """
    for item in root.findall(".//wp:category", ns):
        term_id = tx(item.find("wp:term_id", ns))
        if term_id == parent_id:
            return tx(item.find("wp:cat_name", ns))
    return None

def get_page_directory(post_parent, cats):
    """
    Détermine le dossier de destination d'une page selon sa hiérarchie
    """
    # Si la page a un parent spécifique (comme post_parent == "27" pour groupes)
    if post_parent == "27":
        return "content/groupes"
    
    # Si la page a des catégories, utiliser la première
    if cats:
        category_name = cats[0]
        # Chercher si on a créé un dossier pour cette catégorie
        for category_path in post_id_to_category.values():
            if category_name.lower() in category_path.lower():
                return category_path
    
    # Fallback : dossier pages par défaut
    return "content/pages"

# D'abord créer la structure des dossiers
find_items([".//wp:category", ".//wp:term"])

# TRAITEMENT PRINCIPAL : Conversion des articles, pages et autres contenus WordPress
for item in root.findall("./channel/item"):
    # Filtrage par type de contenu - ne traiter que les types supportés
    ptype = tx(item.find("wp:post_type", ns))
    if ptype not in ["page"]: #"post", , "attachment", "nav_menu_item"
        print(f"⚠️ Ignored item of type '{ptype}'")
        continue
    
    # === EXTRACTION DES MÉTADONNÉES DE BASE ===
    title = tx(item.find("title"))           # Titre de l'article/page
    pubDate = tx(item.find("pubDate"))       # Date de publication RSS

    # === GÉNÉRATION DU SLUG (nom de fichier) ===
    slug_in = tx(item.find("wp:post_name", ns))  # Slug WordPress original
    fallback_slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    slug = safe_slug(slug_in, fallback_slug)

    # === MÉTADONNÉES SUPPLÉMENTAIRES ===
    post_id = tx(item.find("wp:post_id", ns))               # ID unique WordPress
    post_parent = tx(item.find("wp:post_parent", ns))    # ID du parent (pour hiérarchie)
    post_type = tx(item.find("wp:post_type", ns))        # Type de contenu

    # === CONVERSION DU CONTENU HTML VERS MARKDOWN ===
    content_html = tx(item.find("content:encoded", ns))
    content_md = h.handle(content_html)  # Conversion avec html2text

    # Extrait de l'article (résumé)
    excerpt = item.find("excerpt:encoded", ns)
    status = tx(item.find("wp:status", ns))                  # publish/draft/private
    
    # === TRAITEMENT DES CATÉGORIES ET TAGS ===
    cats, tags = [], []
    for c in item.findall("category"):
        label = tx(c)
        if not label:
            continue
        dom = c.get("domain")  # "post_tag" pour les tags, "category" pour les catégories
        if dom == "post_tag":
            tags.append(label)
        else:
            cats.append(label)
    
    # === DÉTERMINATION DU DOSSIER DE DESTINATION ===
    outdir = get_page_directory(post_parent, cats)
    
    # Assurer que le dossier existe
    os.makedirs(outdir, exist_ok=True)
    
    # === CRÉATION DU FRONT MATTER HUGO ===
    fm = {
        "title": title,
        "type": "page",
        "pubDate": pubDate or None,
        "draft": (status != "publish"),
        "menu": "hero" if ptype == "page" else None,
        "categories": cats if cats else None,
        "tags": tags if tags else None,
    }

    # Création du fichier Markdown avec front matter YAML + contenu
    filename = os.path.join(outdir, f"{slug}.md")
    print(f"Création du fichier: {filename}")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("---\n")                           # Début du front matter YAML
        f.write(yaml.dump(fm, sort_keys=False))    # Métadonnées en YAML
        f.write("---\n\n")                         # Fin du front matter
        f.write(content_md)                        # Contenu en Markdown

print("✅ Conversion en Markdown terminée.")
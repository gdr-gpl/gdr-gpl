# Script de conversion d'export WordPress XML vers format Markdown Hugo
# Ce script extrait les données d'un export WordPress et les convertit
# en fichiers Markdown compatibles avec le générateur de site statique Hugo

import os, re
import xml.etree.ElementTree as ET

import html2text  # Pour convertir HTML vers Markdown
import yaml       # Pour générer le front matter YAML

# Charger le fichier XML d'export WordPress
XML_FILE = "gdrgpl.WordPress.2025-09-03.xml"
tree = ET.parse(XML_FILE)
root = tree.getroot()

# Définition des espaces de noms XML utilisés dans l'export WordPress
# Ces préfixes permettent d'accéder aux éléments spécifiques à WordPress
ns = {
    "wp": "http://wordpress.org/export/1.2/",           # Éléments WordPress
    "content": "http://purl.org/rss/1.0/modules/content/", # Contenu des articles
    "dc": "http://purl.org/dc/elements/1.1/",            # Dublin Core (métadonnées)
    "excerpt": "http://wordpress.org/export/1.2/excerpt/", # Extraits d'articles
}

# Création de la structure de dossiers pour Hugo
# Hugo organise le contenu dans différents types de dossiers
os.makedirs("content/toutesInfos/posts", exist_ok=True)        # Articles de blog
os.makedirs("content/toutesInfos/pages", exist_ok=True)        # Pages statiques
os.makedirs("content/toutesInfos/attachment", exist_ok=True)   # Fichiers attachés (images, documents)
os.makedirs("content/toutesInfos/nav_menu_item", exist_ok=True) # Éléments de menu de navigation

# Configuration du convertisseur HTML vers Markdown
h = html2text.HTML2Text()
h.ignore_links = False  # Conserver les liens dans la conversion
h.body_width = 0        # Pas de coupure de ligne automatique (largeur infinie)

def tx(el):
    """
    Fonction utilitaire pour extraire le texte d'un élément XML de façon sécurisée.
    Retourne une chaîne vide si l'élément est None ou si le texte est None.
    """
    return el.text if el is not None and el.text is not None else ""

def safe_slug(s, fallback):
    """
    Génère un slug sécurisé pour les noms de fichiers à partir d'une chaîne.
    
    Args:
        s: La chaîne à convertir en slug
        fallback: Valeur de fallback si s est vide ou invalide
        
    Returns:
        Un slug sécurisé contenant uniquement des caractères alphanumériques, 
        tirets, points et underscores
    """
    s = (s or "").strip().lower().replace(" ", "-")
    s = re.sub(r"[^a-z0-9\-._]", "", s)  # Supprimer tous les caractères non autorisés
    return s or fallback

def find_items(xPaths):
    """
    Fonction pour traiter les catégories et termes WordPress.
    
    Args:
        xPaths: Liste des chemins XPath à traiter (catégories et termes)
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
            
            # Création du front matter pour les métadonnées
            fm = {
                "term_id": term_id or None,
                "name": name or None,
                "slug": slug or None,
                "parent": parent or None,
                "description": description or None,
                "taxonomy": taxonomy or None,
            }
            
            # Détermination du dossier de sortie selon le type d'élément
            match xPath:
                case ".//wp:category":
                    outdir = "content/toutesInfos/categories"
                case ".//wp:term":
                    outdir = "content/toutesInfos/terms"
                case _:
                    continue
                
            # Écriture du fichier Markdown avec front matter YAML
            filename = os.path.join(outdir, slug + ".md")
            with open(filename, "w",encoding="utf-8") as f:
                f.write("---\n")
                f.write(yaml.dump(fm, sort_keys=False))
                f.write("---\n\n")

# TRAITEMENT PRINCIPAL : Conversion des articles, pages et autres contenus WordPress
for item in root.findall("./channel/item"):
    # Filtrage par type de contenu - ne traiter que les types supportés
    ptype = tx(item.find("wp:post_type", ns))
    if ptype not in ["post", "page", "attachment", "nav_menu_item"]:
        print(f"⚠️ Ignored item of type '{ptype}'")
        continue
    
    # === EXTRACTION DES MÉTADONNÉES DE BASE ===
    title = tx(item.find("title"))           # Titre de l'article/page
    
    pubDate = tx(item.find("pubDate"))       # Date de publication RSS
    
    # Dates WordPress (locales et GMT)
    date = tx(item.find("wp:post_date", ns))
    date_gmt = tx(item.find("wp:post_date_gmt", ns))
    
    # Dates de modification
    modified = tx(item.find("wp:post_modified", ns))
    modified_gmt = tx(item.find("wp:post_modified_gmt", ns))

    # États et paramètres WordPress
    comment_status = tx(item.find("wp:comment_status", ns))  # open/closed
    ping_status = tx(item.find("wp:ping_status", ns))        # open/closed  
    creator = tx(item.find("dc:creator", ns))                # Auteur
    post_id = tx(item.find("wp:post_id", ns))               # ID unique WordPress

    # === GÉNÉRATION DU SLUG (nom de fichier) ===
    slug_in = tx(item.find("wp:post_name", ns))  # Slug WordPress original
    # Fallback : générer un slug à partir du titre si le slug WordPress est vide
    fallback_slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    slug = safe_slug(slug_in, fallback_slug)

    # === MÉTADONNÉES SUPPLÉMENTAIRES ===
    post_parent = tx(item.find("wp:post_parent", ns))    # ID du parent (pour hiérarchie)
    post_type = tx(item.find("wp:post_type", ns))        # Type de contenu

    menu_order = tx(item.find("wp:menu_order", ns))      # Ordre dans les menus

    attachement_url = tx(item.find("wp:attachment_url", ns))  # URL si c'est un attachement

    # === CONVERSION DU CONTENU HTML VERS MARKDOWN ===
    content_html = tx(item.find("content:encoded", ns))
    content_md = h.handle(content_html)  # Conversion avec html2text

    # Catégories (code non utilisé - voir plus bas pour le traitement réel)
    categories = [c.text for c in item.findall("category") if c.text]

    # Extrait de l'article (résumé)
    excerpt = item.find("excerpt:encoded", ns)
    
    status = tx(item.find("wp:status", ns))     

    # Front matter Hugo (commentaire obsolète - voir ci-dessous)
    front_matter = "---\n"

    # === TRAITEMENT DES CATÉGORIES ET TAGS ===
    # Séparation entre catégories et tags selon le domaine WordPress
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

    # === CRÉATION DU FRONT MATTER HUGO ===
    # Dictionnaire contenant toutes les métadonnées pour Hugo
    fm = {
        "title": title,
        "slug": slug,
        "date": date or None,
        "date_gmt": date_gmt or None,
        "lastmod": modified or None,            # Date de dernière modification
        "lastmod_gmt": modified_gmt or None,
        "pubDate": pubDate or None,
        "draft": (status != "publish"),         # Article en brouillon si pas publié
        "author": creator or None,
        "post_id": post_id or None,
        "post_parent": post_parent or None,
        "post_type": post_type or None,
        "menu_order": menu_order or None,
        "attachment_url": attachement_url or None,
        "comment_status": comment_status or None,
        "ping_status": ping_status or None,
        "categories": cats if cats else None,   # Liste des catégories
        "tags": tags if tags else None,         # Liste des tags
        "summary": tx(excerpt) if excerpt is not None else None,  # Résumé de l'article
    }


    # === ÉCRITURE DES FICHIERS MARKDOWN ===
    # Détermination du dossier de sortie selon le type de contenu
    match ptype:
        case "post":
            outdir = "content/toutesInfos/posts"           # Articles de blog
        case "page":
            outdir = "content/toutesInfos/pages"           # Pages statiques
        case "attachment":
            outdir = "content/toutesInfos/attachment"      # Fichiers joints
        case "nav_menu_item":
            outdir = "content/toutesInfos/nav_menu_item"   # Éléments de menu
        case _:
            continue  # Ignorer les autres types
            
    # Création du fichier Markdown avec front matter YAML + contenu
    filename = os.path.join(outdir, f"{slug}.md")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("---\n")                           # Début du front matter YAML
        f.write(yaml.dump(fm, sort_keys=False))    # Métadonnées en YAML
        f.write("---\n\n")                         # Fin du front matter
        f.write(content_md)                        # Contenu en Markdown
    

            
# === TRAITEMENT DES CATÉGORIES ET TERMES WORDPRESS ===
# Création des dossiers pour les taxonomies WordPress
os.makedirs("content/toutesInfos/categories", exist_ok=True)
os.makedirs("content/toutesInfos/terms", exist_ok=True)

# # Appel de la fonction pour traiter les catégories et termes
find_items([".//wp:category", ".//wp:term"])

print("✅ Conversion en Markdown terminée.")

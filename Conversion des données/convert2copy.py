# Script de conversion d'export WordPress XML vers format Markdown Hugo
# Ce script extrait les données d'un export WordPress et les convertit
# en fichiers Markdown compatibles avec le générateur de site statique Hugo

import os, re
import xml.etree.ElementTree as ET

import html2text  # Pour convertir HTML vers Markdown
import yaml      

# Charger le fichier XML d'export WordPress
XML_FILE = "gdrgpl.WordPress.2025-09-03.xml"
tree = ET.parse(XML_FILE)
root = tree.getroot()

# Définition des espaces de noms XML utilisés dans l'export WordPress
# Ces préfixes permettent d'accéder aux éléments spécifiques à WordPress
ns = {
    "wp": "http://wordpress.org/export/1.2/",           
    "content": "http://purl.org/rss/1.0/modules/content/", 
    "dc": "http://purl.org/dc/elements/1.1/",            
    "excerpt": "http://wordpress.org/export/1.2/excerpt/", 
}

os.makedirs("content/posts", exist_ok=True)
os.makedirs("content/pages", exist_ok=True)
os.makedirs("content/categ", exist_ok=True)

h = html2text.HTML2Text()
h.ignore_links = False  # Conserver les liens dans la conversion
h.body_width = 0        # Pas de coupure de ligne automatique (largeur infinie)

def tx(el):
    """
    Fonction utilitaire pour extraire le texte d'un élément XML de façon sécurisée.
    Retourne une chaîne vide si l'élément est None ou si le texte est None.
    """
    return el.text if el is not None and el.text is not None else ""

def safe_slug(s):

    s = (s or "").strip().lower().replace(" ", "-")
    s = re.sub(r"[^a-z0-9\-._]", "", s)  # Supprimer tous les caractères non autorisés
    return s

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
            
            fm = {
                "term_id": term_id or None,
                "name": name or None,
                "slug": slug or None,
                "parent": parent or None,
                "description": description or None,
                "taxonomy": taxonomy or None,
            }
            if parent is None:
                directoryPath = "content/categ/"+ name
            else:
                directoryPath = "content/categ/"+ parent +"/"+ name
                
            print(directoryPath)
            os.makedirs(directoryPath, exist_ok=True)
            
            
            # # Détermination du dossier de sortie selon le type d'élément
            # match xPath:
            #     case ".//wp:category":
            #         outdir = "content/categories"
            #     case ".//wp:term":
            #         outdir = "content/terms"
            #     case _:
            #         continue
                
            # # Écriture du fichier Markdown avec front matter YAML
            # filename = os.path.join(outdir, slug + ".md")
            # with open(filename, "w",encoding="utf-8") as f:
            #     f.write("---\n")
            #     f.write(yaml.dump(fm, sort_keys=False))
            #     f.write("---\n\n")
                

for item in root.findall("./channel/item"):
    
    ptype = tx(item.find("wp:post_type", ns))
    if ptype not in ["post"]: #""page", ", , "attachment", "nav_menu_item"
        print(f"⚠️ Ignored item of type '{ptype}'")
        continue
    
    # Extraction des données
    title = tx(item.find("title"))           # Titre de l'article/page
    
    pubDate = tx(item.find("pubDate"))       # Date de publication RSS

    # (nom de fichier) 
    slug_in = tx(item.find("wp:post_name", ns))  # Slug WordPress original
    slug = safe_slug(slug_in)

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
    

    # Catégories associées à l'article
    cats = []
    for c in item.findall("category"):
        label = tx(c)
        if not label:
            continue
        cats.append(label)
            
    
    # Dans quel dossier enregistrer le fichier 
    match ptype:
        case "post":
            outdir = "content/posts"
            post_type = "news"
        case "page":
            outdir = "content/pages/"  
            menu = "hero"
        case "attachment":
            outdir = "content/attachment"      
        case "nav_menu_item":
            outdir = "content/nav_menu_item"   
        case _:
            continue 
    

    fm = {
        "title": title,
        "type": post_type,                      
        "pubDate": pubDate or None,
        "draft": (status != "publish"), 
        "categories": cats or None,
    }

            
    # # Création du fichier Markdown avec front matter YAML + contenu
    filename = os.path.join(outdir, f"{slug}.md")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("---\n")                           
        f.write(yaml.dump(fm, sort_keys=False))
        f.write("---\n\n")                         
        f.write(content_md)                        
    

            
# Création des dossiers pour les taxonomies WordPress            
# os.makedirs("content/categories", exist_ok=True)
# os.makedirs("content/terms", exist_ok=True)

# Appel de la fonction pour traiter les catégories et termes
# find_items([".//wp:category", ".//wp:term"])

print("Conversion en Markdown terminée.")

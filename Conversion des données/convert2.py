import os, re
import xml.etree.ElementTree as ET

import html2text
import yaml

# Charger le XML
XML_FILE = "gdrgpl.WordPress.2025-09-03.xml"
tree = ET.parse(XML_FILE)
root = tree.getroot()

ns = {
    "wp": "http://wordpress.org/export/1.2/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
}

# Dossiers de sortie Hugo
os.makedirs("content/posts", exist_ok=True)
os.makedirs("content/pages", exist_ok=True)
os.makedirs("content/attachment", exist_ok=True)
os.makedirs("content/nav_menu_item", exist_ok=True)

# Convertisseur HTML -> Markdown
h = html2text.HTML2Text()
h.ignore_links = False
h.body_width = 0  # pas de coupure de ligne automatique

def tx(el):
    return el.text if el is not None and el.text is not None else ""

def safe_slug(s, fallback):
    s = (s or "").strip().lower().replace(" ", "-")
    s = re.sub(r"[^a-z0-9\-._]", "", s)
    return s or fallback

count = 0
for item in root.findall("./channel/item"):
    ptype = tx(item.find("wp:post_type", ns))
    if ptype not in ["post", "page", "attachment", "nav_menu_item"]:
        print(f"⚠️ Ignored item of type '{ptype}'")
        count += 1
        continue
    count += 1
    title = tx(item.find("title"))
    
    pubDate = tx(item.find("pubDate"))
    
    date = tx(item.find("wp:post_date", ns))
    date_gmt = tx(item.find("wp:post_date_gmt", ns))
    
    modified = tx(item.find("wp:post_modified", ns))
    modified_gmt = tx(item.find("wp:post_modified_gmt", ns))

    comment_status = tx(item.find("wp:comment_status", ns))
    ping_status = tx(item.find("wp:ping_status", ns))
    status = tx(item.find("wp:status", ns))
    creator = tx(item.find("dc:creator", ns))
    post_id = tx(item.find("wp:post_id", ns))

    slug_in = tx(item.find("wp:post_name", ns))
    fallback_slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    slug = safe_slug(slug_in, fallback_slug)

    post_parent = tx(item.find("wp:post_parent", ns))
    post_type = tx(item.find("wp:post_type", ns))

    menu_order = tx(item.find("wp:menu_order", ns))

    attachement_url = tx(item.find("wp:attachment_url", ns))

    # Convertir le contenu HTML en Markdown
    content_html = tx(item.find("content:encoded", ns))
    content_md = h.handle(content_html)

    # Catégories
    categories = [c.text for c in item.findall("category") if c.text]

    # Excerpt éventuel (on le met en summary si utile)
    excerpt = item.find("excerpt:encoded", ns)

    # Front matter Hugo
    front_matter = "---\n"
    # front_matter += f'title: "{title.replace("\"", "")}"\n'
    # front_matter += f"date: {date}\n"
    # if categories:
    #     front_matter += "categories:\n"
    #     for c in categories:
    #         front_matter += f" - {c}\n"

    # Catégories / tags
    cats, tags = [], []
    for c in item.findall("category"):
        label = tx(c)
        if not label:
            continue
        dom = c.get("domain")
        if dom == "post_tag":
            tags.append(label)
        else:
            cats.append(label)

    fm = {
        "title": title,
        "slug": slug,
        "date": date or None,
        "date_gmt": date_gmt or None,
        "lastmod": modified or None,
        "lastmod_gmt": modified_gmt or None,
        "pubDate": pubDate or None,
        "draft": (status != "publish"),
        "author": creator or None,
        "post_id": post_id or None,
        "post_parent": post_parent or None,
        "post_type": post_type or None,
        "menu_order": menu_order or None,
        "attachment_url": attachement_url or None,
        "comment_status": comment_status or None,
        "ping_status": ping_status or None,
        "categories": cats if cats else None,
        "tags": tags if tags else None,
        "summary": tx(excerpt) if excerpt is not None else None,
        # "featured_image": featured_image_from_meta(item)
    }


    # Écriture fichier
    match ptype:
        case "post":
            outdir = "content/posts"
        case "page":
            outdir = "content/pages"
        case "attachment":
            outdir = "content/attachment"
        case "nav_menu_item":
            outdir = "content/nav_menu_item"
        case _:
            continue
    filename = os.path.join(outdir, f"{slug}.md")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(yaml.dump(fm, sort_keys=False))
        f.write("---\n\n")
        f.write(content_md)
    

    

def find_items(xPaths):
    for xPath in xPaths:
        print(f"Items for XPath: {xPath}")
        for item in root.findall(xPath, ns):
            term_id = tx(item.find("wp:term_id", ns))
            name = tx(item.find("wp:cat_name", ns)) or tx(item.find("wp:term_name", ns))
            slug = tx(item.find("wp:category_nicename", ns)) or tx(item.find("wp:term_slug", ns))
            parent = tx(item.find("wp:category_parent", ns)) or tx(item.find("wp:term_parent", ns))
            description = tx(item.find("wp:category_description", ns)) or tx(item.find("wp:term_description", ns))
            taxonomy = tx(item.find("wp:term_taxonomy", ns))  # utile pour "term"
            
            print(f"- [{term_id}] {taxonomy or 'category'} (slug: {slug}, parent: {parent}), {name}, ({description})")
		    

find_items([".//wp:category", ".//wp:term"])

    

# def findCat():
#     for cat in root.findall(".//wp:category", ns):
#         term_id = tx(cat.find("wp:term_id", ns))
#         cat_name = tx(cat.find("wp:cat_name", ns))
#         nicename = tx(cat.find("wp:category_nicename", ns))
#         parent = tx(cat.find("wp:category_parent", ns))
#         cat_description = tx(cat.find('wp:category_description', ns))

#         print(f"- [{term_id}] {cat_name} (slug: {nicename}, parent: {parent}), {cat_description}")

# def findTerm():
#     for term in root.findall(".//wp:term", ns):
#         term_id = tx(term.find("wp:term_id", ns))
#         term_taxonomy = tx(term.find("wp:term_taxonomy", ns))
#         term_slug = tx(term.find("wp:term_slug", ns))
#         term_parent = tx(term.find("wp:term_parent", ns))
#         term_name = tx(term.find("wp:term_name", ns))
#         term_description = tx(term.find("wp:term_description", ns))

#         print(f"- [{term_id}] {term_taxonomy} (slug: {term_slug}, parent: {term_parent}), {term_name}, ({term_description})")

# findTerm()
print(f"✅ {count} posts/pages converted to Markdown.")
print("✅ Conversion en Markdown terminée.")

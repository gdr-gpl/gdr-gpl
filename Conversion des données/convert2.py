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
# os.makedirs("content/posts", exist_ok=True)
# os.makedirs("content/pages", exist_ok=True)

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

print(len (root.findall("./channel/item")), "items found in XML.")
count = 0
for item in root.findall("./channel/item"):
    ptype = tx(item.find("wp:post_type", ns))
    if ptype not in ["post", "page"]:
        print(f"⚠️ Ignored item of type '{ptype}'")
        count += 1
        continue
    count += 1
    title = tx(item.find("title"))
    date = tx(item.find("wp:post_date", ns))
    modified = tx(item.find("wp:post_modified", ns))
    status = tx(item.find("wp:status", ns))
    creator = tx(item.find("dc:creator", ns))

    slug_in = tx(item.find("wp:post_name", ns))
    fallback_slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    slug = safe_slug(slug_in, fallback_slug)

    # Convertir le contenu HTML en Markdown
    content_html = tx(item.find("content:encoded", ns))
    content_md = h.handle(content_html)

    # Catégories
    categories = [c.text for c in item.findall("category") if c.text]

    # Excerpt éventuel (on le met en summary si utile)
    excerpt = item.find("excerpt:encoded", ns)

    # Front matter Hugo
    front_matter = "---\n"
    #front_matter += f'title: "{title.replace("\"", "")}"\n'
    #front_matter += f"date: {date}\n"
    #if categories:
    #    front_matter += "categories:\n"
    #    for c in categories:
    #        front_matter += f"  - {c}\n"

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
        "lastmod": modified or None,
        "draft": (status != "publish"),
        "author": creator or None,
        "categories": cats,
        "tags": tags,
        "summary": excerpt or None,
        #"featured_image": featured_image_from_meta(item)
    }
    front_matter += "---\n\n"

    

    # # Écriture fichier
    # outdir = "content/posts" if ptype == "post" else "content/pages"
    # filename = os.path.join(outdir, f"{slug}.md")
    # with open(filename, "w", encoding="utf-8") as f:
    #     f.write("---\n")
    #     f.write(yaml.dump(fm, sort_keys=False))
    #     f.write("---\n\n")
    #     f.write(content_md)

print(f"✅ {count} posts/pages converted to Markdown.")
print("✅ Conversion en Markdown terminée.")

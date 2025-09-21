#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, re, csv
import xml.etree.ElementTree as ET

# ---- À adapter si ton fichier a un autre nom
XML_FILE = "gdrgpl.WordPress.2025-09-03.xml"

CONTENT_DIR_POSTS = "content/posts"
CONTENT_DIR_PAGES = "content/pages"
STATIC_UPLOADS = "static/uploads"

os.makedirs(CONTENT_DIR_POSTS, exist_ok=True)
os.makedirs(CONTENT_DIR_PAGES, exist_ok=True)
os.makedirs(STATIC_UPLOADS, exist_ok=True)

# Namespaces WordPress/WXR
ns = {
    "wp": "http://wordpress.org/export/1.2/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
}

def tx(el):
    return el.text if el is not None and el.text is not None else ""

tree = ET.parse(XML_FILE)
root = tree.getroot()

# 1) On collecte d'abord tous les ATTACHMENTS (médias)
attachments = {}     # id -> {url, file, title}
media_urls = []      # pour media_urls.txt

for item in root.findall("./channel/item"):
    ptype = tx(item.find("wp:post_type", ns))
    if ptype != "attachment":
        continue
    pid = tx(item.find("wp:post_id", ns))
    title = tx(item.find("title"))
    url = tx(item.find("wp:attachment_url", ns))

    file_rel = ""
    for pm in item.findall("wp:postmeta", ns):
        k = tx(pm.find("wp:meta_key", ns))
        if k == "_wp_attached_file":
            file_rel = tx(pm.find("wp:meta_value", ns))
            break

    attachments[pid] = {"url": url, "file": file_rel, "title": title}
    if url:
        media_urls.append(url)

# 2) Helpers
def safe_slug(s, fallback):
    s = (s or "").strip().lower().replace(" ", "-")
    s = re.sub(r"[^a-z0-9\-._]", "", s)
    return s or fallback

def write_md(path, fm, body_html):
    # YAML front matter minimal et robuste (sans dépendances)
    lines = ["---"]
    for k, v in fm.items():
        if v in (None, "", []):
            continue
        if isinstance(v, list):
            lines.append(f"{k}:")
            for it in v:
                # on évite les quotes si pas nécessaires
                if isinstance(it, str) and (":" in it or '"' in it or it.strip()!=it):
                    it = it.replace('"', "")
                    lines.append(f'  - "{it}"')
                else:
                    lines.append(f"  - {it}")
        else:
            if isinstance(v, bool):
                lines.append(f"{k}: {str(v).lower()}")
            elif isinstance(v, str) and (":" in v or '"' in v or v.strip()!=v):
                v = v.replace('"', "")
                lines.append(f'{k}: "{v}"')
            else:
                lines.append(f"{k}: {v}")
    lines.append("---")
    content = "\n".join(lines) + "\n\n" + (body_html or "")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

uploads_url_pattern = re.compile(r"https?://[^/\"']+/wp-content/uploads/")

def featured_image_from_meta(item):
    thumb_id = None
    for pm in item.findall("wp:postmeta", ns):
        k = tx(pm.find("wp:meta_key", ns))
        if k == "_thumbnail_id":
            thumb_id = tx(pm.find("wp:meta_value", ns))
            break
    if thumb_id and thumb_id in attachments:
        a = attachments[thumb_id]
        # Chemin "propre" pour Hugo si on a le file_rel
        if a["file"]:
            return "/uploads/" + a["file"]
        # Sinon tenter de dériver depuis l’URL
        if a["url"]:
            m = re.search(r"/wp-content/uploads/(.*)$", a["url"])
            if m:
                return "/uploads/" + m.group(1)
            return a["url"]
    return None

# 3) Posts & Pages
for item in root.findall("./channel/item"):
    ptype = tx(item.find("wp:post_type", ns))
    if ptype not in ("post", "page"):
        continue

    title = tx(item.find("title")) or "Sans titre"
    date = tx(item.find("wp:post_date", ns))
    modified = tx(item.find("wp:post_modified", ns))
    status = (tx(item.find("wp:status", ns)) or "publish").lower()
    creator = tx(item.find("dc:creator", ns))
    slug_in = tx(item.find("wp:post_name", ns))
    fallback_slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    slug = safe_slug(slug_in, fallback_slug)

    # Corps HTML
    body = tx(item.find("content:encoded", ns))
    # Réécrire les URLs absolues "…/wp-content/uploads/…" vers "/uploads/…"
    if body:
        body = uploads_url_pattern.sub("/uploads/", body)

    # Excerpt éventuel (on le met en summary si utile)
    excerpt = tx(item.find("excerpt:encoded", ns))

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
        "featured_image": featured_image_from_meta(item)
    }

    outdir = CONTENT_DIR_POSTS if ptype == "post" else CONTENT_DIR_PAGES
    path = os.path.join(outdir, f"{slug}.md")
    if os.path.exists(path):
        pid = tx(item.find("wp:post_id", ns)) or "x"
        path = os.path.join(outdir, f"{slug}-{pid}.md")

    write_md(path, fm, body)

# 4) Sorties médias
with open("media_urls.txt", "w", encoding="utf-8") as f:
    for u in sorted({u for u in media_urls if u}):
        f.write(u + "\n")

with open("media.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "title", "url", "file"])
    for pid, a in attachments.items():
        w.writerow([pid, a.get("title",""), a.get("url",""), a.get("file","")])

print("OK.")
print("Markdown : content/posts/ et content/pages/")
print("Liste des médias : media_urls.txt (et détails dans media.csv)")
print('Téléchargement :  wget -i media_urls.txt -P static/uploads/')

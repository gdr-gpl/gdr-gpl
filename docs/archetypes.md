# Archétypes Hugo

*Documentation générée automatiquement*

Les archétypes sont les modèles les contenus.

## news

**Fichier :** `archetypes/news.md`

```toml
+++
title = "{{ replace .Name "-" " " | title }}"
date = "{{ .Date }}"
draft = true
categories = ["news"]
+++

```

**Champs définis :**
- `title`
- `date`
- `draft`
- `categories`

## event

**Fichier :** `archetypes/event.md`

```toml
+++
title = "{{ replace .Name "-" " " | title }}"
date = "{{ .Date }}"
draft = true
type = "page"
+++

```

**Champs définis :**
- `title`
- `date`
- `draft`
- `type`

## archive

**Fichier :** `archetypes/archive.md`

```toml
+++
title = "{{ replace .Name "-" " " | title }}"
date = "{{ .Date }}"
draft = false
type = "archive"
+++

```

**Champs définis :**
- `title`
- `date`
- `draft`
- `type`

## default

**Fichier :** `archetypes/default.md`

```toml
+++
date = '{{ .Date }}'
draft = false
title = '{{ replace .File.ContentBaseName "-" " " | title }}'
type = "page"
+++

```

**Champs définis :**
- `date`
- `draft`
- `title`
- `type`

## group

**Fichier :** `archetypes/group.md`

```toml
+++
title = "{{ replace .Name "-" " " | title }}"
date = "{{ .Date }}"
draft = true
+++

```

**Champs définis :**
- `title`
- `date`
- `draft`


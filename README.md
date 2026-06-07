# 🌿 SekhmetKarnark

**Sagesse Ancienne, Science Moderne** — Plateforme naturopathique haut de gamme.

Apothicairerie moderne dédiée à la naturopathie éditoriale, alliant la précision clinique à l'apothicairerie botanique luxueuse.

---

## 🚀 Stack Technique

| Composant | Technologie |
|---|---|
| **Backend** | Django 5.1 LTS |
| **Base de données** | PostgreSQL (local & Railway) |
| **Cache** | Redis (via django-redis) |
| **Frontend** | Tailwind CSS (CDN local), Design Stitch |
| **Paiement** | Tranzak API |
| **Email** | Brevo (Sendinblue) |
| **Déploiement** | Railway (Docker) |
| **Stockage** | WhiteNoice / Cloudflare R2 |

## 🏗 Structure du Projet

```
sekhmetkarnak/
├── config/              # Configuration Django (settings, URLs, WSGI/ASGI)
├── apps/
│   ├── core/            # Pages statiques, context processors
│   ├── accounts/        # Auth, profils, MFA
│   ├── blog/            # Articles, catégories, tags
│   ├── shop/            # Catalogue produits
│   ├── cart/            # Panier session Redis
│   ├── orders/          # Commandes
│   ├── payments/        # Intégration Tranzak
│   ├── newsletter/      # Abonnés, double opt-in
│   ├── contact/         # Formulaires de contact
│   └── seo/             # Sitemaps, robots, hreflang
├── templates/           # Templates Django (design Stitch)
├── static/              # Assets locaux (fonts, CSS, JS, SVG)
├── requirements/        # Dépendances Python
├── locale/              # Traductions FR/EN
├── Dockerfile           # Déploiement conteneurisé
└── railway.toml         # Configuration Railway
```

## 🚦 Démarrage Local

```bash
# 1. Cloner le projet
git clone <repo-url>
cd sekhmetkarnark

# 2. Créer l'environnement virtuel
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate # Linux/Mac

# 3. Installer les dépendances
pip install -r requirements/local.txt

# 4. Configurer .env (copier depuis .env.example)
cp .env.example .env
# Éditer .env avec vos paramètres PostgreSQL

# 5. Base de données
createdb sekhmetkarnark
python manage.py migrate --settings=config.settings.local

# 6. Lancer le serveur
python manage.py runserver --settings=config.settings.local
```

## 🎨 Design System

Le design des templates **Stitch** est intégré sans modification esthétique :

- **Typographie :** Libre Caslon Text (titres), Literata (corps), Jost (UI)
- **Palette :** Vert forêt profond (#1A3C2E), Ivoire (#F5F0E8), Or botanique (#B8962E)
- **Approche :** Éditorial minimaliste avec espacement généreux (120px+ de padding sections)

## 🔌 API / Webhooks

- **Tranzak Webhook :** `POST /paiements/webhook/tranzak/`
- **Health Check :** `GET /health/`
- **Sitemap :** `GET /sitemap.xml`

## 🌐 Internationalisation

- Français (défaut)
- Anglais
- Commutateur de langue via `{% trans %}` et `i18n_patterns`

## 📦 Déploiement Railway

```bash
# Les GitHub Actions déploient automatiquement sur Railway
# Ou manuellement :
railway up
```

---

*Développé avec une mission : offrir une expérience naturopathique d'exception.*

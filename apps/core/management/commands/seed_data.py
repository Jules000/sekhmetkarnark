"""Seed la base avec des donnees demo correspondant aux templates Stitch."""
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone

User = get_user_model()

SHOP_CATEGORIES = [
    {"name": "Huiles Essentielles", "slug": "huiles-essentielles"},
    {"name": "Gelules Botaniques", "slug": "gelules-botaniques"},
    {"name": "Tisanes & Infusions", "slug": "tisanes-infusions"},
    {"name": "Poudres & Superaliments", "slug": "poudres-superaliments"},
    {"name": "Elixirs Spagyriques", "slug": "elixirs-spagyriques"},
]

BLOG_CATEGORIES = [
    {"name": "Phytotherapie"},
    {"name": "Nutrition"},
    {"name": "Naturopathie Fondamentale"},
    {"name": "Aromatherapie"},
    {"name": "Bien-être & Spiritualité"},
]

TAGS = [
    "Inflammation", "Microbiote", "Sommeil", "Thyroide", "Aromatherapie",
]

FCFA = lambda eur: str(round(float(eur) * 655.957, 0))

PRODUCTS = [
    {
        "category": "Huiles Essentielles",
        "name": "Neroli Imperial",
        "price": FCFA(45),
        "description": "Un elixir de nuit profondement regenerant. Formule avec de l'absolue de Neroli rare et de l'huile de pepin de figue de barbarie.",
        "short_description": "Elixir Botanique",
        "is_featured": True,
        "stock_quantity": 25,
        "benefits": "Le Neroli Imperial agit sur deux fronts : l'equilibre cutane et l'apaisement nerveux.\n\n• Restaure l'eclat des teints fatigues.\n• Diminue visiblement les rougeurs et inflammations.\n• L'olfactotherapie du Neroli favorise l'endormissement.",
        "usage_instructions": "Le soir, sur une peau parfaitement nettoyee et legerement humide :\n\n1. Prelevez 3 a 4 gouttes dans le creux des mains.\n2. Chauffez l'elixir en frottant doucement vos paumes.\n3. Inspirez profondement les effluves de Neroli 3 fois.\n4. Massez le visage et le cou par des mouvements ascendants lents.",
        "composition": "Simmondsia Chinensis (Jojoba) Seed Oil*, Opuntia Ficus-Indica (Prickly Pear) Seed Oil*, Squalane (Olive derived), Citrus Aurantium Amara (Neroli) Flower Oil, Pelargonium Graveolens (Geranium) Oil*, Tocopherol (Vitamin E).\n\n*Ingredients issus de l'agriculture biologique.",
    },
    {
        "category": "Huiles Essentielles",
        "name": "Tea Tree Austral",
        "price": FCFA(28),
        "description": "Huile essentielle de Tea Tree (Melaleuca alternifolia) premium, aux proprietes antiseptiques et immunostimulantes exceptionnelles.",
        "short_description": "Antiseptique Naturel",
        "is_featured": False,
        "stock_quantity": 55,
        "benefits": "• Puissant antiseptique et antifongique naturel\n• Stimule les defenses immunitaires\n• Assainit l'air et les voies respiratoires",
        "usage_instructions": "2 gouttes dans une cuillere de miel 3 fois par jour en cure de 5 jours. Diffusion : 5 gouttes dans un diffuseur.",
        "composition": "100% Melaleuca alternifolia (Tea Tree) huile essentielle* certifiee biologique.",
    },
    {
        "category": "Gelules Botaniques",
        "name": "Ashwagandha Sombre",
        "price": FCFA(38),
        "description": "Extrait racine d'Ashwagandha hautement concentre pour soutenir la gestion du stress chronique et l'equilibre du systeme nerveux.",
        "short_description": "Extrait Racine",
        "is_featured": True,
        "stock_quantity": 50,
        "benefits": "• Regulation de l'axe HPA et du cortisol\n• Soutien a la fonction surrenalienne\n• Amelioration de la resilience au stress",
        "usage_instructions": "2 gelules par jour, de preference le matin avec un grand verre d'eau. Cure recommandee de 3 mois.",
        "composition": "Extrait racine d'Ashwagandha (Withania somnifera) 500mg, Agent d'enrobage : pullule (vegetal).",
    },
    {
        "category": "Tisanes & Infusions",
        "name": "Songe d'Osiris",
        "price": FCFA(22),
        "description": "Infusion botanique aux fleurs de camomille et a la verveine, pour un rituel du soir apaisant et regenerateur.",
        "short_description": "Infusion Botanique",
        "is_featured": False,
        "stock_quantity": 100,
        "benefits": "• Favorise l'endormissement naturel\n• Apaise le systeme nerveux\n• Proprietes digestives douces",
        "usage_instructions": "Infuser 1 cuillere a cafe dans 200ml d'eau a 95°C pendant 5 a 7 minutes. Deguster en fin de journee.",
        "composition": "Camomille matricaire*, Verveine odorante*, Fleur d'oranger*, Tilleul*, *Issus de l'agriculture biologique.",
    },
    {
        "category": "Poudres & Superaliments",
        "name": "Moringa Solaire",
        "price": FCFA(29),
        "description": "Superaliment vert issu du Moringa oleifera, reconnu pour sa densite nutritionnelle exceptionnelle et ses proprietes antioxydantes.",
        "short_description": "Superaliment Vert",
        "is_featured": True,
        "stock_quantity": 75,
        "benefits": "• Richesse en vitamines et mineraux essentiels\n• Soutien immunitaire naturel\n• Energie durable et vitalite",
        "usage_instructions": "1 cuillere a cafe par jour, melangee a un jus, smoothie ou compote. Ne pas depasser 2 cuilleres par jour.",
        "composition": "100% Poudre de feuilles de Moringa oleifera issue de l'agriculture biologique certifiee.",
    },
    {
        "category": "Elixirs Spagyriques",
        "name": "Quintessence d'Hematite",
        "price": FCFA(65),
        "description": "Elixir spagyrique prepare selon les principes de l'alchimie vegetale. Une synergie unique de plantes ferrugineuses et d'oligo-elements.",
        "short_description": "Elixir Spagyrique",
        "is_featured": True,
        "stock_quantity": 15,
        "benefits": "• Revitalisation profonde\n• Soutien a la regeneration cellulaire\n• Reequilibrage energetique",
        "usage_instructions": "5 gouttes sous la langue, matin et soir, en cure de 21 jours.",
        "composition": "Teinture-mere spagyrique d'Ortie, de Pissenlit, de Fucus, oligo-elements naturels, alcool vegetal 35% vol.",
    },
]

ARTICLES = [
    {
        "title": "Le Pouvoir Adaptogene de l'Ashwagandha face au Stress Chronique",
        "excerpt": "Une analyse clinique detaillee de l'impact des plantes adaptogenes sur l'axe HPA et la regulation du cortisol en naturopathie moderne.",
        "content": "<p>Le stress chronique est devenu I'un des principaux defis de sante de notre epoque. Dans la quete de solutions naturelles et efficaces, I'Ashwagandha (Withania somnifera) emerge comme I'un des adaptogenes les plus etudies et les plus prometteurs.</p><h2>Qu'est-ce qu'un adaptogene ?</h2><p>Les adaptogenes sont une classe unique de plantes medicinales qui aident I'organisme a s'adapter au stress, qu'il soit physique, chimique ou biologique. Ils agissent en modulant I'axe hypothalamo-hypophyso-surrenalien (HPA).</p><h2>Mecanismes d'action de I'Ashwagandha</h2><p>Des etudes cliniques recentes demontrent que I'Ashwagandha reduit significativement les niveaux de cortisol, I'hormone primaire du stress, jusqu'a 30% chez les adultes souffrant de stress chronique.</p><h2>Posologie recommandee</h2><p>La dose therapeutique standard se situe entre 300 et 600 mg d'extrait standardise, pris une a deux fois par jour. Une cure de 8 a 12 semaines est generalement recommendee pour des resultats optimaux.</p>",
        "category": "Phytotherapie",
        "reading_time": 8,
        "tags": ["Inflammation", "Sommeil"],
        "is_featured": True,
    },
    {
        "title": "Protocoles de Detoxification Hepatique Douce",
        "excerpt": "Decouvrez les methodes naturelles pour soutenir votre foie dans son travail de filtration quotidien, sans regimes draconiens ni privations.",
        "content": "<p>Le foie est I'organe central de la detoxification. Chaque jour, il filtre plus de 1 500 litres de sang et elimine les toxines endogenes et exogenes. Pour I'aider dans cette tache, la nature nous offre des allies precieux.</p><h2>Les plantes hepatoprotectrices</h2><p>Le chardon-Marie, le desmodium et I'artichaut sont les piliers de toute cure de detoxification hepatique douce. Leurs principes actifs favorisent la regeneration cellulaire et la secretion biliaire.</p><h2>Protocole de 21 jours</h2><p>Notre protocole propose une approche progressive : semaine 1 - preparation et introduction des plantes hepatoprotectrices, semaine 2 - cure intensive, semaine 3 - retour en douceur a I'alimentation normale.</p>",
        "category": "Nutrition",
        "reading_time": 5,
        "tags": ["Microbiote", "Inflammation"],
        "is_featured": False,
    },
    {
        "title": "Microbiote et Axe Intestin-Cerveau",
        "excerpt": "Explorez les connexions fascinantes entre votre microbiote intestinal et votre sante mentale. Un voyage au coeur de la medecine integrative.",
        "content": "<p>L'axe intestin-cerveau represente I'une des frontieres les plus passionnantes de la medecine moderne. Notre deuxieme cerveau, le systeme nerveux enterique, communique en permanence avec notre cerveau central via un reseau complexe de neurones et de neurotransmetteurs.</p><h2>Le microbiote : notre allie invisible</h2><p>Notre intestin heberge plus de 100 000 milliards de micro-organismes qui jouent un role crucial dans notre sante mentale. Ils produisent environ 95% de la serotonine de I'organisme.</p><h2>Alimentation et equilibre du microbiote</h2><p>Les aliments fermentes, les fibres prebiotiques et les polyphénols sont essentiels au maintien d'un microbiote diversifie et resilient.</p>",
        "category": "Nutrition",
        "reading_time": 12,
        "tags": ["Microbiote"],
        "is_featured": False,
    },
    {
        "title": "Les 5 Piliers d'une Digestion Optimale",
        "excerpt": "Decouvrez les fondamentaux d'une digestion saine et harmonieuse, pierre angulaire de la sante globale.",
        "content": "<p>Une digestion optimale est la cle de voûte d'une sante rayonnante. Decouvrez les 5 piliers fondamentaux pour soutenir votre systeme digestif au quotidien.</p>",
        "category": "Naturopathie Fondamentale",
        "reading_time": 7,
        "tags": ["Microbiote"],
        "is_featured": False,
    },
    {
        "title": "Jeune Intermittent : Mythes et Realites Cliniques",
        "excerpt": "Que dit vraiment la science sur le jeune intermittent ? Une analyse objective des bienfaits et des contre-indications.",
        "content": "<p>Le jeune intermittent est devenu une pratique populaire, mais que disent les etudes cliniques ? Cet article fait le point sur les donnees scientifiques actuelles.</p>",
        "category": "Nutrition",
        "reading_time": 10,
        "tags": ["Inflammation"],
        "is_featured": False,
    },
    {
        "title": "Gemmotherapie : Le Pouvoir des Bourgeons",
        "excerpt": "La gemmotherapie utilise les tissus embryonnaires vegetaux pour une action profonde et regulee sur I'organisme.",
        "content": "<p>La gemmotherapie est une branche de la phytotherapie qui utilise les bourgeons et jeunes pousses des arbres et arbustes. Ces tissus en croissance concentrent I'energie vitale de la plante.</p><h2>Les bourgeons les plus utilises</h2><p>Le bourgeon de cassis est le reine des drainants hepatiques. Le figuier est le bourgeon de la serenite. Le tilleul argente est le regulateur du systeme nerveux autonome.</p><h2>Mode de preparation</h2><p>Les macerats de bourgeons sont prepares selon le methode de l'herboristerie traditionnelle. Une maceration dans un melange d'eau, d'alcool vegetal et de glycerine permet d'extraire I'integralite des principes actifs.</p><h2>Posologie recommandee</h2><p>5 a 15 gouttes par jour, en cure de 3 semaines. A prendre de preference loin des repas, en dilution dans un peu d'eau.</p>",
        "category": "Phytotherapie",
        "reading_time": 6,
        "tags": ["Aromatherapie"],
        "is_featured": False,
    },
    {
        "title": "Aromatherapie Scientifique : Les Huiles Essentielles Chimiotypees",
        "excerpt": "Decouvrez comment les huiles essentielles chemiotypees garantissent une efficacite clinique optimale en aromatherapie moderne.",
        "content": "<p>L'aromatherapie scientifique repose sur un principe fondamental : chaque huile essentielle doit etre chemiotypee (HEBBD) pour garantir sa composition biochimique precise et son action therapeutique ciblee.</p><h2>Qu'est-ce qu'un chimiotype ?</h2><p>Le chimiotype designe la composition biochimique specifique d'une huile essentielle en fonction de la variete botanique, du terroir et des conditions de culture. Par exemple, le Thym peut exister sous plusieurs chimiotypes : thym a thymol, a linalol, a carvacrol...</p><h2>Pourquoi c'est important</h2><p>Chaque chimiotype possede des proprietes differentes. Le Thym a thymol est puissamment antiseptique tandis que le Thym a linalol est plus doux et mieux adapte aux enfants.</p><h2>Applications cliniques</h2><p>En pratique clinique, le choix du chimiotype adapte permet de cibler precisement le desequilibre du patient, que ce soit une infection, une inflammation ou un trouble emotionnel.</p>",
        "category": "Aromatherapie",
        "reading_time": 7,
        "tags": ["Aromatherapie"],
        "is_featured": False,
    },
    {
        "title": "Le Rituel du Matin : 5 Pratiques Ayurvediques pour une Journee Vitalisante",
        "excerpt": "Inspirez de la sagesse ayurvedique millenaire, ces 5 rituels matinaux transforment profondement votre bien-etre quotidien.",
        "content": "<p>L'Ayurveda, science de la vie vieille de 5000 ans, nous enseigne que nos rituels matinaux determinent la qualite de notre journee. Voici 5 pratiques essentielles pour commencer chaque jour avec vitalite et clarte.</p><h2>1. Le Lever Avant le Soleil</h2><p>Se lever pendant la phase Vata (avant 6h) permet de capter l'energie subtile de l'aube. C'est le moment ideal pour la meditation et la respiration consciente.</p><h2>2. La Purification de la Langue</h2><p>Le grattoir a langue elimine les toxines accumulees pendant la nuit (ama) et stimule le systeme digestif. Une pratique simple aux benefices profonds.</p><h2>3. L'Huile de Sesame en Oil Pulling</h2><p>Faire circuler une cuillere a soupe d'huile de sesame dans la bouche pendant 15 minutes. Cette technique detoxifie la cavite buccale et renforce les gencives.</p><h2>4. Boire de l'Eau Chaude au Citron</h2><p>Un grand verre d'eau chaude avec du citron frais et une pincee de sel rose de l'Himalaya. Ce breuvage alcalinise, hydrate et stimule le transit.</p><h2>5. La Secousse Corporelle</h2><p>Terminez par 5 minutes de secousses corporelles libres pour eveiller la circulation et liberer les tensions nocturnes. Une pratique joyeuse et liberatrice.</p>",
        "category": "Bien-être & Spiritualité",
        "reading_time": 9,
        "tags": ["Sommeil"],
        "is_featured": True,
    },
]


class Command(BaseCommand):
    help = "Seed la base avec les donnees demo des templates Stitch"

    def handle(self, *args, **options):
        self._create_users()
        self._create_shop_categories()
        self._create_blog_categories()
        self._create_tags()
        self._create_products()
        self._create_articles()
        self._create_hero_slides()
        self.stdout.write(self.style.SUCCESS("Seed termine avec succes !"))

    def _create_users(self):
        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@sekhmetkarnak.com",
                "is_staff": True,
                "is_superuser": True,
                "first_name": "Eleonore",
                "last_name": "Dubois",
                "botanical_points": 140,
                "is_premium": True,
            },
        )
        if created:
            admin.set_password("Admin0002!")
            admin.save()
            self.stdout.write(f"  ✓ Superuser admin cree")
        else:
            self.stdout.write(f"  → Superuser admin existe deja")

        self.author = admin

    def _create_shop_categories(self):
        from apps.shop.models import Category as ShopCategory
        self.shop_categories = {}
        for cat in SHOP_CATEGORIES:
            obj, created = ShopCategory.objects.get_or_create(
                slug=cat["slug"], defaults={"name": cat["name"]}
            )
            self.shop_categories[cat["name"]] = obj
            if created:
                self.stdout.write(f"  ✓ Categorie boutique : {cat['name']}")

    def _create_blog_categories(self):
        from apps.blog.models import Category as BlogCategory
        self.blog_categories = {}
        for cat in BLOG_CATEGORIES:
            slug = slugify(cat["name"])
            obj, created = BlogCategory.objects.get_or_create(
                slug=slug, defaults={"name": cat["name"]}
            )
            self.blog_categories[cat["name"]] = obj
            if created:
                self.stdout.write(f"  ✓ Categorie blog : {cat['name']}")

    def _create_tags(self):
        from apps.blog.models import Tag
        self.tags = {}
        for tag_name in TAGS:
            slug = slugify(tag_name)
            obj, created = Tag.objects.get_or_create(
                slug=slug, defaults={"name": tag_name}
            )
            self.tags[tag_name] = obj
            if created:
                self.stdout.write(f"  ✓ Tag : {tag_name}")

    def _create_products(self):
        from apps.shop.models import Product
        for p in PRODUCTS:
            cat = self.shop_categories.get(p["category"])
            slug = slugify(p["name"])
            obj, created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    "category": cat,
                    "name": p["name"],
                    "description": p["description"],
                    "short_description": p["short_description"],
                    "price": p["price"],
                    "stock_quantity": p["stock_quantity"],
                    "is_active": True,
                    "is_featured": p.get("is_featured", False),
                    "benefits": p.get("benefits", ""),
                    "usage_instructions": p.get("usage_instructions", ""),
                    "composition": p.get("composition", ""),
                },
            )
            if created:
                self.stdout.write(f"  ✓ Produit : {p['name']} ({p['price']} EUR)")

    def _create_hero_slides(self):
        from apps.core.models import HeroSlide
        slides = [
            {
                "page": "home",
                "title": "Sagesse Ancienne,<br>Science Moderne",
                "subtitle": "Découvrez une approche naturopathique éditoriale et haut de gamme. Des remèdes curatifs alliant la précision clinique à l'apothicairerie botanique luxueuse.",
                "cta_text": "Explorer nos remèdes",
                "cta_url": "/boutique/",
                "sort_order": 0,
            },
            {
                "page": "login",
                "title": "Welcome Back",
                "subtitle": "Enter your details to access your sanctuary.",
                "cta_text": "",
                "cta_url": "",
                "sort_order": 0,
            },
            {
                "page": "register",
                "title": "Begin Your Journey",
                "subtitle": "Join our circle of holistic wellness and curated apothecary artifacts.",
                "cta_text": "",
                "cta_url": "",
                "sort_order": 0,
            },
            {
                "page": "forgot_password",
                "title": "",
                "subtitle": "",
                "cta_text": "",
                "cta_url": "",
                "sort_order": 0,
            },
            {
                "page": "otp_verify",
                "title": "",
                "subtitle": "",
                "cta_text": "",
                "cta_url": "",
                "sort_order": 0,
            },
        ]
        for s in slides:
            slug = f"{s['page']}-{s['sort_order']}"
            obj, created = HeroSlide.objects.get_or_create(
                page=s["page"],
                sort_order=s["sort_order"],
                defaults={
                    "title": s["title"],
                    "subtitle": s["subtitle"],
                    "cta_text": s["cta_text"],
                    "cta_url": s["cta_url"],
                    "is_active": True,
                },
            )
            if created:
                self.stdout.write(f"  ✓ Hero slide ({s['page']}) : {s['title'][:30] or 'default'}...")

    def _create_articles(self):
        from apps.blog.models import Article
        for i, a in enumerate(ARTICLES):
            cat = self.blog_categories.get(a["category"])
            slug = slugify(a["title"])[:50]
            pub_date = timezone.now() - timedelta(days=i)
            obj, created = Article.objects.get_or_create(
                slug=slug,
                defaults={
                    "title": a["title"],
                    "excerpt": a["excerpt"],
                    "content": a["content"],
                    "author": self.author,
                    "category": cat,
                    "reading_time": a["reading_time"],
                    "status": "published",
                    "published_at": pub_date,
                },
            )
            if created:
                for tag_name in a["tags"]:
                    tag = self.tags.get(tag_name)
                    if tag:
                        obj.tags.add(tag)
                self.stdout.write(f"  ✓ Article : {a['title'][:50]}...")

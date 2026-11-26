# Thème Shopify gumis

Thème Online Store 2.0 pour **gumis**, marque de gummies vitaminés vendus en France puis dans l'UE.
Basé sur **Dawn 16.2.0** (Shopify, licence MIT, voir `LICENSE.md`). Les produits sont expédiés par **Suplify** :
le thème ne gère que la vitrine.

- Liquid + modèles JSON, tout est modifiable dans l'éditeur de thème (sections, blocs, réglages).
- Français par défaut (`locales/fr.default.json`), anglais en 2ᵉ langue (`locales/en.json`).
- JavaScript natif uniquement (aucun jQuery), mobile-first.
- Polices **Fredoka** (titres) et **Nunito** (texte) auto-hébergées dans `assets/` (licence SIL OFL, voir `docs/licenses/`).
  Aucune police chargée depuis Google Fonts ni depuis le CDN de polices Shopify.
- Aucun handle de produit codé en dur : produits, collections et pages se choisissent dans l'éditeur.

---

## 1. Installation

Prérequis : [Shopify CLI](https://shopify.dev/docs/api/shopify-cli) 3.x, Node 18+, un accès collaborateur ou propriétaire à la boutique.

```bash
git clone <url-du-depot> gumis-theme
```

```bash
cd gumis-theme
```

```bash
shopify theme dev --store <votre-boutique>.myshopify.com
```

Contrôle qualité (Theme Check) :

```bash
shopify theme check
```

Publier une copie non publiée pour relecture :

```bash
shopify theme push --unpublished --store <votre-boutique>.myshopify.com
```

### Paramétrage de la boutique (Admin Shopify)

1. **Paramètres > Marchés / Devise** : EUR comme devise de la boutique.
2. **Paramètres > Taxes et droits** : cochez « Tous les prix incluent les taxes » (prix TTC).
3. **Paramètres > Langues** : français par défaut, ajoutez l'anglais et publiez-le.
4. **Boutique en ligne > Navigation** : créez les menus `main-menu` (en-tête) et `footer` (bloc « La boutique » du pied de page).
5. Créez les **métachamps** (section 2), les **réductions automatiques** (section 3), les **pages** (section 5).
6. **Paramètres > Confidentialité client** : activez la collecte du consentement pour l'UE/EEE et
   **désactivez la bannière Shopify** (le thème fournit la sienne, voir section 8). N'utilisez pas les deux.
7. **Éditeur de thème > Paramètres du thème** :
   - *Gumis — marque* : couleurs, arrondis, logo texte, tagline, nombre de gummies par pot (60).
   - *Gumis — panier & offres* : seuil de livraison offerte, % de remise 2 et 3 pots.
   - *Gumis — cookies & RGPD* : bannière et page « Politique cookies ».
8. Dans l'éditeur, sélectionnez les produits dans **Trio produits**, **Offre multi-pots** (accueil) et éventuellement le **Hero**.

---

## 2. Métachamps produit à créer

**Paramètres > Données personnalisées > Produits > Ajouter une définition.** Espace de noms `custom` pour tous.

| Nom | Clé complète | Type | Contenu |
|---|---|---|---|
| Tagline | `custom.tagline` | Texte sur une ligne | Phrase courte affichée sous le titre et sur les cartes produit. Pas d'allégation santé non autorisée. |
| Bénéfices | `custom.benefits` | Liste de textes sur une ligne | **Allégations autorisées uniquement** (registre UE des allégations de santé), mot pour mot. |
| Ingrédients | `custom.ingredients` | Texte enrichi | Liste des ingrédients par ordre pondéral décroissant, allergènes en gras. |
| Tableau nutritionnel | `custom.nutrition_table` | JSON | Voir format ci-dessous. |
| Conseils d'utilisation | `custom.how_to_use` | Texte enrichi | Mode d'emploi. |
| Précautions | `custom.warnings` | Texte enrichi | Mises en garde. Voir texte par défaut ci-dessous. |
| Couleur d'accent | `custom.accent_color` | Couleur | Sommeil = `#3B0A2A` (Plum), Éclat = `#D6246E` (Berry), Force = `#FF8A3D` (Tangerine). |
| Dose | `custom.serving` | Texte sur une ligne | Ex. « 2 gummies par jour » [À COMPLÉTER selon la formule finale]. |

Cochez « Accès Storefront » si vous utilisez plus tard un front headless (non requis pour ce thème).

### Format de `custom.nutrition_table`

Un tableau de lignes, ou un objet avec `serving` et `rows` :

```json
{
  "serving": "2 gummies",
  "rows": [
    { "label": "Mélatonine", "per_serving": "1 mg", "percent_nrv": "" },
    { "label": "Vitamine B6", "per_serving": "[À COMPLÉTER] mg", "percent_nrv": "[À COMPLÉTER] %" }
  ]
}
```

`percent_nrv` vide affiche « – » (substances sans VNR, comme la mélatonine ou la créatine).
Ces valeurs sont **des exemples de structure** : ne publiez que les doses de la formule finale.

### Texte par défaut de `custom.warnings`

```
Ne pas dépasser la dose journalière recommandée.
Tenir hors de la portée des jeunes enfants.
Les compléments alimentaires ne doivent pas être utilisés comme substituts d'un régime alimentaire varié et équilibré et d'un mode de vie sain.
[À COMPLÉTER : mises en garde propres à la formule (grossesse, allaitement, enfants, interactions, conservation…)]
```

**Garantie du thème :** l'onglet « Précautions » affiche toujours ces 3 mentions obligatoires (textes dans les fichiers de langue,
`gumis.compliance.*`). Si `custom.warnings` les contient déjà, elles ne sont pas dupliquées ; s'il ne les contient pas, le thème les ajoute.

### Allégations de travail (à valider sur la formule finale, NE PAS coder en dur)

À saisir dans `custom.benefits` **uniquement** une fois la formule validée par votre responsable réglementaire :

- **Gumis Sommeil** : « La mélatonine contribue à réduire le temps d'endormissement. »
  Valable uniquement avec **1 mg de mélatonine pris peu avant le coucher**.
- **Gumis Éclat** : « La biotine contribue au maintien de cheveux normaux et d'une peau normale. »
  et « Le zinc contribue au maintien d'ongles normaux. » (quantités significatives requises)
- **Gumis Force** : « La créatine augmente la performance physique lors d'exercices successifs de courte durée et de haute intensité. »
  Valable uniquement avec un **apport journalier de 3 g de créatine**.

Le thème n'affiche **aucune** allégation santé ailleurs que depuis ces métachamps. Les textes par défaut n'emploient jamais
« guérit », « traite », « prévient », « soigne » ni aucun vocabulaire médical.

---

## 3. Réductions automatiques 2 et 3 pots

Le sélecteur 1/2/3 pots règle simplement la **quantité** ajoutée au panier. La remise est appliquée par Shopify.

**Remises > Créer une réduction > Montant de réduction sur les produits > Automatique** :

| Réduction | Condition | Valeur | Combinaisons |
|---|---|---|---|
| `Gumis 2 pots` | Quantité minimum d'articles : **2** | **[À COMPLÉTER] %** | Ne pas combiner avec les autres réductions produit |
| `Gumis 3 pots` | Quantité minimum d'articles : **3** | **[À COMPLÉTER] %** | Ne pas combiner avec les autres réductions produit |

- « S'applique à » : la collection des gummies (ou les 3 produits).
- Quand les deux sont éligibles, Shopify applique la plus avantageuse (celle des 3 pots).
- Puis, dans **Paramètres du thème > Gumis — panier & offres**, saisissez **exactement les mêmes pourcentages**
  (« Remise pour 2 pots », « Remise pour 3 pots »). Ils servent uniquement à **afficher** l'économie
  sur les cartes et l'incitation du panier. À **0 %**, aucune économie n'est affichée : aucun prix n'est inventé.
- Si vous modifiez une réduction dans l'admin, mettez à jour le réglage du thème le même jour.

Le sélecteur suppose un produit à variante unique (un pot de 60 gummies). Pour un produit à plusieurs variantes,
les cartes produit renvoient vers la fiche produit.

---

## 4. Liste des `[À COMPLÉTER]`

Chaque texte provisoire est visible sur le site (surligné en rose) pour ne rien oublier avant le lancement.

### Paramètres du thème
- *Gumis — panier & offres* : seuil de livraison offerte (vide = barre masquée), % remise 2 pots, % remise 3 pots (0 par défaut).

### En-tête / pied de page (Éditeur > En-tête / Pied de page)
- Barre d'annonce : « Livraison offerte dès **[À COMPLÉTER]** € d'achat ».
- Pied de page, bloc « Une question ? » : **[À COMPLÉTER : e-mail du service client]**.

### Accueil (`templates/index.json`)
- Gummies vs gélules : arôme (« Fruité : [À COMPLÉTER arôme] »), format du pot, sucres par portion.
- Comment ça marche, étape 3 : durée d'un pot (« vous accompagne [À COMPLÉTER] jours »).
- FAQ : sucres/édulcorants, vegan/gélatine/pectine/allergènes, enfants et grossesse, délais de livraison, conditions pour les pots ouverts.

### Fiche produit (`templates/product.json`)
- Bloc réassurance : « Livraison offerte dès [À COMPLÉTER] € ».
- Métachamps manquants : l'éditeur affiche « Métachamp custom.xxx à compléter » ; la boutique affiche [À COMPLÉTER] dans les onglets vides.

### Pages
- **Notre histoire** (`page.histoire`) : intro, histoire des fondateurs, 3 engagements.
- **FAQ** (`page.faq`) : moment de prise par formule, sucres, allergènes, lieu de fabrication, enfants/grossesse, conservation, délais.
- **Contact** (`page.contact`) : délai de réponse.
- **Livraison & retours** (`page.livraison`) : résumé, pays, tarifs, seuil, délais, produits descellés, colis abîmé.
- **Pages légales** (CGV, mentions légales, confidentialité, cookies, rétractation) : contenu de la page + « Dernière mise à jour ».
- **Droit de rétractation** : raison sociale, adresse postale, e-mail dans le formulaire type.

### Hors thème (à fournir)
- Photos produits (fond transparent conseillé : elles s'affichent sur la couleur d'accent). En attendant, le thème dessine des pots en CSS.
- Doses, tableau nutritionnel et allégations définitifs pour chaque formule.

---

## 5. Pages à créer (Boutique en ligne > Pages)

| Page | Modèle à choisir | Identifiant (handle) conseillé |
|---|---|---|
| Notre histoire | `page.histoire` | `notre-histoire` |
| FAQ | `page.faq` | `faq` |
| Contact | `page.contact` | `contact` |
| Livraison & retours | `page.livraison` | `livraison-et-retours` |
| CGV | `page.cgv` | `cgv` |
| Mentions légales | `page.mentions-legales` | `mentions-legales` |
| Politique de confidentialité | `page.confidentialite` | `politique-de-confidentialite` |
| Politique cookies | `page.cookies` | `politique-cookies` |
| Droit de rétractation (14 jours) | `page.retractation` | `droit-de-retractation` |

Le bloc « Gumis liens légaux » du pied de page permet de choisir chaque page légale. Si une page n'est pas choisie,
le lien pointe vers `/pages/<handle conseillé>` ci-dessus. Le contenu juridique est rédigé par le propriétaire
(idéalement relu par un juriste) : le thème ne fournit que la mise en page et le **formulaire type de rétractation**
(annexe à l'article R221-1 du Code de la consommation).

Note : pour les compléments alimentaires descellés, l'exception de l'article L221-28 5° du Code de la consommation peut s'appliquer ;
à préciser dans vos CGV.

---

## 6. Connecter les produits Suplify

1. Installez l'application **Suplify** depuis le Shopify App Store et connectez votre compte.
2. Importez ou associez les 3 produits (Sommeil, Éclat, Force) depuis Suplify : l'appli crée les produits et gère stock et expédition.
3. Sur chaque produit Shopify :
   - renseignez les **métachamps** de la section 2 ;
   - ajoutez les photos ;
   - vérifiez prix TTC, poids et SKU synchronisés par Suplify (ne modifiez pas les SKU, ils servent au routage des commandes) ;
   - ajoutez le produit à la collection des gummies.
4. Créez une collection « Tous nos gummies » (manuelle ou automatique) : le modèle `collection` affiche ce titre par défaut.
5. Dans l'éditeur de thème : choisissez les produits dans *Trio produits*, *Offre multi-pots* et, si besoin, *Cross-sell*.
6. Passez une commande test (passerelle de test) et vérifiez qu'elle apparaît dans Suplify.

Le thème ne dépend d'aucun handle : changer le nom ou l'URL d'un produit ne casse rien.

---

## 7. Tracking (Meta, GA4)

**Aucun pixel n'est codé en dur dans le thème.**

- **Meta Pixel + API Conversions** : application **Facebook & Instagram** (Shopify). Partage de données « Maximum » pour activer l'API Conversions.
- **GA4 + Google Ads** : application **Google & YouTube** (Shopify). Liez la propriété GA4 dans l'appli.
- Ces applis utilisent les *Web Pixels* de Shopify, qui respectent automatiquement le consentement enregistré par la bannière du thème.
- Les événements e-commerce (vue produit, ajout au panier, paiement) sont émis par Shopify : rien à ajouter dans le thème.
- Pour un script tiers supplémentaire, utilisez **Paramètres > Événements client > Pixel personnalisé** (soumis au consentement),
  jamais `theme.liquid`.

---

## 8. RGPD et cookies

- `sections/gumis-cookie-banner.liquid` + `assets/gumis-consent.js` utilisent l'**API Customer Privacy** de Shopify
  (`shouldShowBanner`, `currentVisitorConsent`, `setTrackingConsent`).
- Boutons « Tout refuser » et « Tout accepter » de même poids visuel (recommandations CNIL), choix par catégorie
  (préférences, mesure d'audience, publicité), réouverture via « Gérer les cookies » (pied de page et page Politique cookies).
- Le thème ne charge aucun script marketing ; rien n'est déclenché avant consentement.
- Newsletter : activez le double opt-in dans **Paramètres > Notifications clients** et gardez la mention de confidentialité sous le formulaire.

---

## 9. Conformité compléments alimentaires (rappel)

- Allégations santé : uniquement depuis `custom.benefits` / `custom.tagline`, et uniquement les allégations autorisées.
- Les 3 mentions obligatoires sont toujours affichées sur la fiche produit (onglet Précautions) ; la 3ᵉ figure aussi dans le pied de page.
- Aucun avis, note, nombre de clients, statistique, dose ou prix inventé. Les avis passent par une **application d'avis**
  ajoutée en bloc d'appli dans la section « Gumis Avis clients » ; sans appli ou sans avis, la section ne s'affiche pas.
- Déclaration des compléments à la DGAL (TéléIcare) avant mise sur le marché : hors thème, à la charge de la marque.

---

## 10. Structure du thème (ajouts gumis)

| Fichier | Rôle |
|---|---|
| `snippets/gumis-fonts.liquid` | `@font-face` auto-hébergés + jetons CSS `--gumis-*` |
| `snippets/logo.liquid` | Logo « gumis » (Fredoka Bold, ı sans point + gummy orange) |
| `snippets/gumis-icon.liquid` | Icônes SVG au trait (pas d'emoji) |
| `snippets/gumis-product-card.liquid` | Carte produit (accent, nom, bénéfice depuis métachamp, prix, ajout panier) |
| `snippets/gumis-quantity-breaks.liquid` + `assets/gumis-quantity-breaks.js` | Sélecteur 1/2/3 pots |
| `snippets/gumis-product-block.liquid` | Blocs fiche produit : tagline, quantités, bénéfices, onglets, réassurance |
| `snippets/gumis-sticky-atc.liquid` + `assets/gumis-sticky-atc.js` | Barre d'ajout au panier fixe (mobile) |
| `snippets/gumis-cart-extras.liquid` + `assets/gumis-cart.js` | Barre livraison offerte + incitation palier suivant |
| `sections/gumis-*.liquid` | Hero, Trio, Gummies vs gélules, Étapes, Offre multi-pots, Avis, FAQ, Cross-sell, Cookies, Formulaire de rétractation |
| `sections/main-gumis-page.liquid`, `main-gumis-collection.liquid` | Pages (style marque ou légal) et collection |
| `assets/gumis.css`, `assets/gumis-sections.css` | Couche de style gumis par-dessus Dawn |

Fichiers Dawn modifiés : `layout/theme.liquid`, `layout/password.liquid`, `templates/gift_card.liquid` (polices),
`sections/header.liquid` et `main-password-header.liquid` (logo), `sections/footer.liquid` (blocs marque et légal, mention),
`sections/main-product.liquid` (blocs gumis, barre fixe), `snippets/cart-drawer.liquid` (extras panier).
Autres langues de vitrine de Dawn retirées ; pour ajouter l'allemand, l'italien ou l'espagnol, copiez `en.json` en `de.json` etc. et traduisez les clés `gumis.*`.

### Mettre à jour Dawn

```bash
git fetch upstream
```

```bash
git merge upstream/main
```

Résolvez les conflits sur les fichiers Dawn listés ci-dessus.

---

## 11. Performance et accessibilité

- Objectif Lighthouse mobile ≥ 90 (performance et accessibilité) : **à mesurer sur la boutique réelle** avec vos photos
  (`shopify theme dev` ou thème non publié). Gardez des images produit ≤ 2000 px, en PNG/WebP compressé.
- Deux feuilles de style gumis globales (pas de CSS par section), JS différé et chargé seulement par les sections qui en ont besoin,
  2 polices préchargées, `font-display: swap`, image du hero en `fetchpriority="high"`.
- Contrastes WCAG AA vérifiés pour les palettes : blanc sur Berry 4,84:1 ; Plum sur Cream 15,4:1 ; Plum sur Tangerine 7,1:1 ;
  Plum sur Bubblegum 12,4:1. **Berry sur Cream (4,47:1) est réservé aux grands titres**, jamais au texte courant.
- Formes décoratives en `aria-hidden`, animations désactivées avec `prefers-reduced-motion`, tableaux et accordéons sémantiques.

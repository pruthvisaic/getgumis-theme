# gumis Shopify theme (getgumis.com)

Online Store 2.0 theme for **gumis** (getgumis.com), a direct-to-consumer brand of vitamin gummies sold
in France first, then other EU countries. Built on **Dawn 16.2.0** (Shopify, MIT licence, see `LICENSE.md`).
Products are fulfilled by **Suplify**: the theme only handles the storefront.

- **English is the default language** (`locales/en.default.json`), **French** is the second (`locales/fr.json`).
  Every storefront string of the theme lives in those two files, under the `gumis` key.
- Liquid + JSON templates, everything editable in the theme editor (sections, blocks, settings).
- Clean, minimal look: white pages with blush, peach and lilac blocks, Ink buttons with 10px corners, drawn jars
  on a pedestal, a Plum stats band, line-style accordions.
- **Manrope** (headings and text) and **Fredoka** (logo, jar labels) are self-hosted in `assets/` (SIL OFL licence,
  see `docs/licenses/`). No font is loaded from Google Fonts or Shopify's font CDN.
- Vanilla JavaScript only (no jQuery), mobile-first.
- No product handle is hard-coded: products, collections and pages are picked in the editor.
- Store currency EUR, prices shown tax included.

---

## 1. Setup

Requirements: [Shopify CLI](https://shopify.dev/docs/api/shopify-cli) 3.x, Node 18+, staff or owner access to the store.

```bash
git clone <repository-url> gumis-theme
```

```bash
cd gumis-theme
```

```bash
shopify theme dev --store <your-store>.myshopify.com
```

Quality check (Theme Check):

```bash
shopify theme check
```

Push an unpublished copy for review:

```bash
shopify theme push --unpublished --store <your-store>.myshopify.com
```

Without the CLI: zip the folders `assets config layout locales sections snippets templates` and upload the zip in
**Online Store > Themes > Add theme > Upload zip file**.

### Store settings (Shopify admin)

1. **Settings > Store details**: store name `gumis` (or `getgumis`), sender email on your domain, e.g. [TO COMPLETE]@getgumis.com.
2. **Settings > Domains**: connect **getgumis.com** and set it as the primary domain.
3. **Settings > Markets**: EUR as store currency; France first, add other EU countries when ready.
4. **Settings > Taxes and duties**: tick "Include sales tax in product price and shipping rate" (prices tax included).
5. **Settings > Languages**: **English** as default, add **French** and publish it. The EN / FR switcher in the header
   and footer only appears once both languages are published.
6. **Online Store > Navigation**: create the `main-menu` (header) and `footer` (footer "Shop" column) menus.
7. Create the **metafields** (section 2), the **automatic discounts** (section 3) and the **pages** (section 5).
8. **Settings > Customer privacy**: collect consent for the EU/EEA and **turn off Shopify's own banner**
   (the theme ships its own, see section 8). Don't use both.
9. **Theme editor > Theme settings**:
   - *Gumis: brand*: colours, corner radius, text logo, tagline, gummies per jar (60).
   - *Gumis: cart & offers*: free-shipping threshold, 2-jar and 3-jar discount %.
   - *Gumis: cookies & GDPR*: banner on/off and the Cookie policy page.
10. In the editor, pick the products in **Gumis Product trio** and **Gumis Multi-jar offer** (home page), and optionally the **Hero** image.

### French translation of section content

The theme's own strings (buttons, labels, mandatory statements, default headings) are already translated in
`locales/fr.json`. Text typed into sections and blocks (FAQ answers, steps, comparison rows…) is store content:
translate it with Shopify's **Translate & Adapt** app. `docs/fr-section-content.md` lists the French version of
every default text shipped in the templates, ready to paste.

---

## 2. Product metafields to create

**Settings > Custom data > Products > Add definition.** Namespace `custom` for all.

| Name | Full key | Type | Content |
|---|---|---|---|
| Tagline | `custom.tagline` | Single line text | Short line under the title and on product cards. No unauthorised health claim. |
| Benefits | `custom.benefits` | List of single line text | **Authorised claims only** (EU register of health claims), word for word. |
| Ingredients | `custom.ingredients` | Rich text | Ingredients in descending order of weight, allergens in bold. |
| Nutrition table | `custom.nutrition_table` | JSON | See format below. |
| How to use | `custom.how_to_use` | Rich text | Directions for use. |
| Warnings | `custom.warnings` | Rich text | Warnings. See default text below. |
| Accent colour | `custom.accent_color` | Color | Sleep = `#3B0A2A` (Plum), Glow = `#D6246E` (Berry), Power = `#FF8A3D` (Tangerine). |
| Serving | `custom.serving` | Single line text | e.g. "2 gummies a day" [TO COMPLETE for the final formula]. |

Metafield values are translatable too: add the French text in Translate & Adapt.

### `custom.nutrition_table` format

An array of rows, or an object with `serving` and `rows`:

```json
{
  "serving": "2 gummies",
  "rows": [
    { "label": "Melatonin", "per_serving": "1 mg", "percent_nrv": "" },
    { "label": "Vitamin B6", "per_serving": "[TO COMPLETE] mg", "percent_nrv": "[TO COMPLETE] %" }
  ]
}
```

An empty `percent_nrv` shows "–" (substances without an NRV, such as melatonin or creatine).
These values only show the **structure**: publish only the doses of the final formula.

### Default text for `custom.warnings`

```
Do not exceed the recommended daily dose.
Keep out of reach of young children.
Food supplements should not be used as a substitute for a varied and balanced diet and a healthy lifestyle.
[TO COMPLETE: warnings specific to the formula (pregnancy, breastfeeding, children, interactions, storage…)]
```

French version for the translation:

```
Ne pas dépasser la dose journalière recommandée.
Tenir hors de la portée des jeunes enfants.
Les compléments alimentaires ne doivent pas être utilisés comme substituts d'un régime alimentaire varié et équilibré et d'un mode de vie sain.
```

**What the theme guarantees:** the Warnings tab always shows these 3 mandatory statements, in the visitor's language
(`gumis.compliance.*` in the locale files). If `custom.warnings` already contains them, they are not repeated; if not,
the theme adds them. The third statement also appears in the footer.

### Working claims (to check against the final formula, NEVER hard-coded)

Enter them in `custom.benefits` **only** once the formula is approved by your regulatory lead:

- **Gumis Sleep**: "Melatonin contributes to the reduction of time taken to fall asleep."
  (FR: « La mélatonine contribue à réduire le temps d'endormissement. ») Only valid with **1 mg of melatonin
  taken close to bedtime**.
- **Gumis Glow** (hair, skin & nails): "Biotin contributes to the maintenance of normal hair and normal skin." and
  "Zinc contributes to the maintenance of normal nails." (FR: « La biotine contribue au maintien de cheveux normaux
  et d'une peau normale. » / « Le zinc contribue au maintien d'ongles normaux. ») Significant amounts required.
- **Gumis Power** (creatine): "Creatine increases physical performance in successive bursts of short-term,
  high intensity exercise." (FR: « La créatine augmente la performance physique lors d'exercices successifs de
  courte durée et de haute intensité. ») Only valid with a **daily intake of 3 g of creatine**.

The theme shows **no** health claim anywhere except from these metafields. Default copy never uses "cures",
"treats", "prevents", "heals" or any medical wording.

---

## 3. Automatic discounts for 2 and 3 jars

The 1/2/3-jar selector only sets the **quantity** added to the cart. Shopify applies the discount.

**Discounts > Create discount > Amount off products > Automatic discount**:

| Discount | Condition | Value | Combinations |
|---|---|---|---|
| `Gumis 2 jars` | Minimum quantity of items: **2** | **[TO COMPLETE] %** | Don't combine with other product discounts |
| `Gumis 3 jars` | Minimum quantity of items: **3** | **[TO COMPLETE] %** | Don't combine with other product discounts |

- "Applies to": the gummies collection (or the 3 products).
- When both qualify, Shopify applies the better one (the 3-jar discount).
- Then, in **Theme settings > Gumis: cart & offers**, enter **exactly the same percentages**
  ("Discount for 2 jars", "Discount for 3 jars"). They are only used to **display** the saving on the jar cards and in
  the cart upsell. At **0 %** no saving is shown: no price is ever made up.
- If you change a discount in the admin, update the theme setting the same day.

The selector assumes a single-variant product (one jar of 60 gummies). For a product with several variants,
product cards link to the product page instead.

---

## 4. List of `[TO COMPLETE]` placeholders

Every temporary text is visible on the site (highlighted in pink) so nothing is forgotten before launch.
The French file uses `[À COMPLÉTER]`.

### Theme settings
- *Gumis: cart & offers*: free-shipping threshold (empty = bar hidden), 2-jar discount %, 3-jar discount % (0 by default).

### Header and footer (Editor > Header / Footer)
- Announcement bar: "Free shipping on orders over €**[TO COMPLETE]**".
- Footer "Help" block: **[TO COMPLETE: support email, e.g. hello@getgumis.com]**.

### Home page (`templates/index.json`)
- Trust card: free-shipping threshold, payment methods ("Cards, Apple Pay [TO COMPLETE]").
- Stats band: only true figures (3 formulas, 60 gummies per jar, 14-day withdrawal).
- Gummies vs capsules: flavour ("Fruity: [TO COMPLETE flavour]"), jar format, sugar per serving.
- How it works, step 3: how long a jar lasts ("lasts you [TO COMPLETE] days").
- FAQ: sugar/sweeteners, vegan/gelatine/pectin/allergens, children and pregnancy, delivery times, opened jars.

### Product page (`templates/product.json`)
- Reassurance row: "Free over €[TO COMPLETE]".
- Missing metafields: the editor shows "Metafield custom.xxx: [TO COMPLETE]"; the shop shows [TO COMPLETE] in empty tabs.

### Pages
- **Our story** (`page.about`): intro, founders' story, 3 values.
- **FAQ** (`page.faq`): when to take each formula, sugar, allergens, manufacturing site, children/pregnancy, storage, delivery times.
- **Contact** (`page.contact`): response time.
- **Shipping & returns** (`page.shipping`): summary, countries, rates, threshold, delivery times, unsealed products, damaged parcels.
- **Legal pages** (terms, legal notice, privacy, cookies, withdrawal): page content + "Last updated".
- **Right of withdrawal**: company name, postal address and email in the model form.

### Outside the theme (to provide)
- Product photos (transparent background recommended: they sit on the accent colour). Until then the theme draws jars in CSS.
- Final doses, nutrition tables and claims for each formula.

---

## 5. Pages to create (Online Store > Pages)

| Page | Template | Suggested handle |
|---|---|---|
| Our story | `page.about` | `our-story` |
| FAQ | `page.faq` | `faq` |
| Contact | `page.contact` | `contact` |
| Shipping & returns | `page.shipping` | `shipping-and-returns` |
| Terms of sale | `page.terms` | `terms-of-sale` |
| Legal notice | `page.legal-notice` | `legal-notice` |
| Privacy policy | `page.privacy` | `privacy-policy` |
| Cookie policy | `page.cookies` | `cookie-policy` |
| Right of withdrawal (14 days) | `page.withdrawal` | `right-of-withdrawal` |

The footer "Gumis legal links" block lets you pick each legal page. If a page isn't picked, the link points to
`/pages/<suggested handle>` above (the newsletter and contact privacy links also use `/pages/privacy-policy`).
Legal content is written by the owner (ideally reviewed by a lawyer): the theme provides the layout and the
**model withdrawal form** (EU Directive 2011/83/EU, Annex I(B); French Consumer Code, annex to article R221-1), in
English and French.

Note: for food supplements that have been unsealed, the exception of article L221-28 5° of the French Consumer Code
may apply; spell it out in your terms of sale.

---

## 6. Connecting Suplify products

1. Install the **Suplify** app from the Shopify App Store and connect your account.
2. Import or link the 3 products (Gumis Sleep, Gumis Glow, Gumis Power) from Suplify: the app creates the products
   and handles stock and shipping.
3. On each Shopify product:
   - fill in the **metafields** from section 2 (and their French translations);
   - add photos;
   - check the tax-included price, weight and SKU synced by Suplify (don't change SKUs, they route the orders);
   - add the product to the gummies collection.
4. Create an "All our gummies" collection (manual or automated): the `collection` template shows this title by default.
5. In the theme editor: pick the products in *Gumis Product trio*, *Gumis Multi-jar offer* and, if needed, *Gumis Cross-sell*.
6. Place a test order (test payment gateway) and check that it shows up in Suplify.

The theme doesn't depend on any handle: renaming a product or changing its URL breaks nothing.

---

## 7. Tracking (Meta, GA4)

**No pixel is hard-coded in the theme.**

- **Meta Pixel + Conversions API**: Shopify's **Facebook & Instagram** app. Set data sharing to "Maximum" to enable the Conversions API.
- **GA4 + Google Ads**: Shopify's **Google & YouTube** app. Link the GA4 property in the app.
- These apps use Shopify *Web Pixels*, which automatically respect the consent recorded by the theme's banner.
- E-commerce events (product view, add to cart, checkout) are sent by Shopify: nothing to add in the theme.
- For any extra third-party script, use **Settings > Customer events > Custom pixel** (consent-aware), never `theme.liquid`.

---

## 8. GDPR and cookies

- `sections/gumis-cookie-banner.liquid` + `assets/gumis-consent.js` use Shopify's **Customer Privacy API**
  (`shouldShowBanner`, `currentVisitorConsent`, `setTrackingConsent`).
- "Reject all" and "Accept all" carry equal visual weight (CNIL guidance), with per-category choices
  (preferences, analytics, advertising), reopenable via "Manage cookies" (footer and Cookie policy page).
- The theme loads no marketing script; nothing fires before consent.
- Newsletter: turn on double opt-in in **Settings > Customer notifications** and keep the privacy note under the form.

---

## 9. Food-supplement compliance (reminder)

- Health claims: only from `custom.benefits` / `custom.tagline`, and only authorised claims.
- The 3 mandatory statements always show on the product page (Warnings tab), in English or French; the third one also sits in the footer.
- No invented reviews, ratings, customer counts, statistics, doses or prices. Reviews come from a **reviews app**
  added as an app block in the "Gumis Reviews" section; without an app or reviews, the section stays hidden.
- Notify the supplements to the French authorities (DGAL, TéléIcare) before placing them on the market: outside the theme, the brand's responsibility.

---

## 10. Theme structure (gumis additions)

| File | Role |
|---|---|
| `snippets/gumis-fonts.liquid` | Self-hosted `@font-face` + `--gumis-*` CSS tokens |
| `snippets/logo.liquid` | "getgumis" wordmark (Fredoka Bold, "get" in Plum + "gumis" in Berry, dotless ı + orange gummy dot; prefix editable in Theme settings) |
| `snippets/gumis-jar.liquid` | Drawn jar (lid, glass, label in the accent colour), shown until photos exist |
| `snippets/gumis-icon.liquid` | Inline SVG stroke icons (no emoji) |
| `snippets/gumis-language-switcher.liquid` | EN / FR switcher (header and footer), works without JavaScript |
| `snippets/gumis-product-card.liquid` | Product card (pastel tile, name, price, benefit from metafield, add to cart) |
| `snippets/gumis-quantity-breaks.liquid` + `assets/gumis-quantity-breaks.js` | 1/2/3-jar selector |
| `snippets/gumis-product-block.liquid` | Product page blocks: tagline, quantities, benefits, tabs, reassurance |
| `snippets/gumis-sticky-atc.liquid` + `assets/gumis-sticky-atc.js` | Sticky add-to-cart bar (mobile) |
| `snippets/gumis-cart-extras.liquid` + `assets/gumis-cart.js` | Free-shipping bar + next-tier upsell in the cart drawer |
| `sections/gumis-*.liquid` | Hero, Trust card, Product trio, Stats band, Image with text, Gummies vs capsules, How it works, Multi-jar offer, Reviews, FAQ, Newsletter, Cross-sell, Cookies, Withdrawal form |
| `sections/main-gumis-page.liquid`, `main-gumis-collection.liquid` | Pages (brand or legal style) and collection |
| `assets/gumis.css`, `assets/gumis-sections.css` | gumis style layer on top of Dawn |

Dawn files changed: `layout/theme.liquid`, `layout/password.liquid`, `templates/gift_card.liquid` (fonts),
`sections/header.liquid` (logo, language switcher), `main-password-header.liquid` (logo),
`sections/footer.liquid` (brand and legal blocks, statement, language switcher),
`sections/main-product.liquid` (gumis blocks, sticky bar), `snippets/cart-drawer.liquid` (cart extras).
Dawn's other storefront languages were removed; to add German, Italian or Spanish, copy `en.default.json`
to `de.json` etc. and translate the `gumis.*` keys.

### Updating Dawn

```bash
git fetch upstream
```

```bash
git merge upstream/main
```

Resolve conflicts in the Dawn files listed above.

---

## 11. Performance and accessibility

- Target Lighthouse mobile ≥ 90 (performance and accessibility): **measure on the real store** with your photos
  (`shopify theme dev` or an unpublished theme). Keep product images ≤ 2000 px, compressed PNG/WebP.
- Two global gumis stylesheets (no per-section CSS), 2 Manrope fonts preloaded, deferred JavaScript loaded only by
  the sections that need it, `font-display: swap`, hero image with `fetchpriority="high"`.
- WCAG AA contrast checked: Ink on white 18:1; secondary text `#5C4152` 9:1; caption grey `#7A6372` ≥ 4.8:1 on white
  and the 3 pastels; Berry on white 4.84:1; orange figures and pink captions on Plum ≥ 9:1.
- Decorative shapes are `aria-hidden`, animations respect `prefers-reduced-motion`, tables and accordions are semantic.

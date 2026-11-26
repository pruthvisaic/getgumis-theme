/* Gumis — cookie consent banner using Shopify's Customer Privacy API.
   https://shopify.dev/docs/api/customer-privacy
   No tracking script is loaded by the theme; Shopify apps' pixels honour this consent. */
if (!customElements.get('gumis-consent')) {
  customElements.define(
    'gumis-consent',
    class GumisConsent extends HTMLElement {
      connectedCallback() {
        this.prefs = this.querySelector('[data-consent-prefs]');
        this.saveButton = this.querySelector('[data-consent="save"]');
        this.customizeButton = this.querySelector('[data-consent="customize"]');

        this.querySelectorAll('[data-consent]').forEach((button) => {
          button.addEventListener('click', () => this.handle(button.dataset.consent));
        });
        this.addEventListener('keydown', (event) => {
          if (event.key === 'Escape' && this.forced) this.hide();
        });
        document.addEventListener('click', (event) => {
          const opener = event.target.closest('[data-gumis-open-consent]');
          if (!opener) return;
          event.preventDefault();
          this.opener = opener;
          this.show({ customize: true, forced: true });
        });

        if (window.Shopify?.designMode) {
          document.addEventListener('shopify:section:select', (event) => {
            if (event.target.querySelector('gumis-consent') === this) this.show({ forced: true });
          });
          document.addEventListener('shopify:section:deselect', (event) => {
            if (event.target.querySelector('gumis-consent') === this) this.hide();
          });
        }

        this.loadApi().then((api) => {
          if (api && api.shouldShowBanner()) this.show({});
        });
      }

      loadApi() {
        if (this.apiPromise) return this.apiPromise;
        this.apiPromise = new Promise((resolve) => {
          const done = () => resolve(window.Shopify?.customerPrivacy || null);
          if (window.Shopify?.customerPrivacy) return done();
          if (!window.Shopify?.loadFeatures) return resolve(null);
          window.Shopify.loadFeatures([{ name: 'consent-tracking-api', version: '0.1' }], (error) => {
            if (error) {
              console.warn('[gumis] Customer Privacy API unavailable', error);
              return resolve(null);
            }
            done();
          });
        });
        return this.apiPromise;
      }

      show({ customize = false, forced = false }) {
        this.forced = forced;
        this.hidden = false;
        this.syncFromCurrent();
        this.toggleCustomize(customize);
        requestAnimationFrame(() => this.querySelector('[role="dialog"]').focus({ preventScroll: true }));
      }

      hide() {
        this.hidden = true;
        if (this.opener) {
          this.opener.focus();
          this.opener = null;
        }
      }

      toggleCustomize(open) {
        this.prefs.hidden = !open;
        this.saveButton.hidden = !open;
        this.customizeButton.hidden = open;
        this.customizeButton.setAttribute('aria-expanded', String(open));
      }

      syncFromCurrent() {
        const current = window.Shopify?.customerPrivacy?.currentVisitorConsent?.() || {};
        ['analytics', 'marketing', 'preferences'].forEach((key) => {
          const input = this.prefs.querySelector(`[name="${key}"]`);
          if (input) input.checked = current[key] === 'yes';
        });
      }

      handle(action) {
        if (action === 'customize') return this.toggleCustomize(true);
        let consent;
        if (action === 'accept') consent = { analytics: true, marketing: true, preferences: true };
        if (action === 'reject') consent = { analytics: false, marketing: false, preferences: false };
        if (action === 'save') {
          const get = (name) => Boolean(this.prefs.querySelector(`[name="${name}"]`)?.checked);
          consent = { analytics: get('analytics'), marketing: get('marketing'), preferences: get('preferences') };
        }
        if (!consent) return;
        consent.sale_of_data = consent.marketing;

        this.loadApi().then((api) => {
          if (!api) return this.hide();
          api.setTrackingConsent(consent, () => {
            document.dispatchEvent(new CustomEvent('gumis:consent-updated', { detail: consent }));
            this.hide();
          });
        });
      }
    }
  );
}

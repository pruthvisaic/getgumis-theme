/* Gumis — sticky add-to-cart bar (shown on mobile once the main button scrolls out of view). */
if (!customElements.get('gumis-sticky-atc')) {
  customElements.define(
    'gumis-sticky-atc',
    class GumisStickyAtc extends HTMLElement {
      connectedCallback() {
        this.button = this.querySelector('button');
        this.target = document.getElementById(this.dataset.watch);
        if (!this.target || !('IntersectionObserver' in window)) return;

        this.observer = new IntersectionObserver(
          ([entry]) => {
            const passed = !entry.isIntersecting && entry.boundingClientRect.top < 0;
            this.setVisible(passed);
          },
          { threshold: 0 }
        );
        this.observer.observe(this.target);
        this.setVisible(false);
      }

      disconnectedCallback() {
        this.observer?.disconnect();
      }

      setVisible(visible) {
        this.dataset.visible = String(visible);
        this.toggleAttribute('inert', !visible);
        this.setAttribute('aria-hidden', String(!visible));
        if (this.button) this.button.tabIndex = visible ? 0 : -1;
        document.body.classList.toggle('gumis-has-sticky-atc', visible);
      }
    }
  );
}

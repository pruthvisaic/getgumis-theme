/* Gumis — cart drawer upsell: "+1 jar" bumps the most recently added line by one,
   reusing Dawn's cart-drawer-items.updateQuantity so sections re-render as usual. */
if (!customElements.get('gumis-cart-upsell')) {
  customElements.define(
    'gumis-cart-upsell',
    class GumisCartUpsell extends HTMLElement {
      connectedCallback() {
        this.button = this.querySelector('button');
        this.button?.addEventListener('click', (event) => {
          const items = this.closest('cart-drawer-items') || document.querySelector('cart-drawer-items');
          if (!items || typeof items.updateQuantity !== 'function') return;
          this.button.setAttribute('aria-disabled', 'true');
          items.updateQuantity(
            this.button.dataset.line,
            parseInt(this.button.dataset.quantity, 10),
            event,
            null,
            this.button.dataset.variantId
          );
        });
      }
    }
  );
}

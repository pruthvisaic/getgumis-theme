/* Gumis — quantity breaks.
   The radios already submit the right quantity without JS. This script only
   mirrors the selected total on elements that reference the same form:
   [data-gumis-total-for="<form id>"] and the sticky add-to-cart bar. */
if (!customElements.get('gumis-quantity-breaks')) {
  customElements.define(
    'gumis-quantity-breaks',
    class GumisQuantityBreaks extends HTMLElement {
      connectedCallback() {
        this.formId = this.dataset.formId;
        this.addEventListener('change', (event) => {
          if (event.target.matches('input[name="quantity"]')) this.sync(event.target);
        });
        const checked = this.querySelector('input[name="quantity"]:checked');
        if (checked) this.sync(checked);
      }

      sync(input) {
        document.querySelectorAll(`[data-gumis-total-for="${this.formId}"]`).forEach((el) => {
          el.textContent = input.dataset.total;
        });
        document.querySelectorAll(`[data-gumis-compare-for="${this.formId}"]`).forEach((el) => {
          el.textContent = input.dataset.compare || '';
          el.hidden = !input.dataset.compare;
        });
        document.dispatchEvent(
          new CustomEvent('gumis:quantity-change', {
            detail: { formId: this.formId, quantity: parseInt(input.value, 10), total: input.dataset.total },
          })
        );
      }
    }
  );
}

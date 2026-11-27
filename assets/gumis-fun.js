/*
 * gumis playful touches (vanilla JS, no dependencies):
 * 1. Bottles react on hover / tap: the bottle wakes up and smiles (CSS: .is-react).
 * 2. On desktop, open eyes follow the mouse.
 * 3. Gummy pop: on add to cart, a few gummies in the product colour jump from the button to the cart icon.
 * Everything is skipped for visitors who ask for reduced motion.
 */
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  /* ---------- 1. reactions ---------- */
  var timers = new WeakMap();
  function react(bottle, ms) {
    if (!bottle) return;
    clearTimeout(timers.get(bottle));
    if (!bottle.classList.contains('is-react')) {
      bottle.classList.remove('is-react');
      void bottle.offsetWidth; // restart the bounce
      bottle.classList.add('is-react');
    }
    timers.set(bottle, setTimeout(function () { bottle.classList.remove('is-react'); }, ms || 1800));
  }
  function bottleFrom(target) {
    if (!(target instanceof Element)) return null;
    var b = target.closest('.g-bottle');
    if (b) return b;
    var card = target.closest('.g-card, .g-bundle__media, .pv-main-image');
    return card ? card.querySelector('.g-bottle') : null;
  }
  document.addEventListener('pointerover', function (e) {
    if (e.pointerType !== 'mouse') return;
    var b = bottleFrom(e.target);
    var from = bottleFrom(e.relatedTarget);
    if (b && from !== b) react(b, 2200);
  });
  document.addEventListener('pointerdown', function (e) {
    if (e.pointerType === 'mouse') return;
    react(bottleFrom(e.target), 1800);
  }, { passive: true });

  /* ---------- 2. eyes follow the mouse ---------- */
  if (window.matchMedia('(pointer: fine)').matches) {
    var mx = 0, my = 0, queued = false;
    var move = function () {
      queued = false;
      document.querySelectorAll('.g-face .f-pupil').forEach(function (p) {
        var r = p.getBoundingClientRect();
        if (!r.width || r.bottom < 0 || r.top > window.innerHeight) return;
        var dx = mx - (r.left + r.width / 2);
        var dy = my - (r.top + r.height / 2);
        var d = Math.hypot(dx, dy) || 1;
        var k = Math.min(1, d / 300) * 9; // up to 9 face units
        p.style.transform = 'translate(' + ((dx / d) * k).toFixed(1) + 'px,' + ((dy / d) * k).toFixed(1) + 'px)';
      });
    };
    document.addEventListener('pointermove', function (e) {
      mx = e.clientX;
      my = e.clientY;
      if (!queued) {
        queued = true;
        requestAnimationFrame(move);
      }
    }, { passive: true });
  }

  /* ---------- 3. gummy pop on add to cart ---------- */
  var BEAR = '<svg viewBox="0 0 22 26" width="22" height="26" aria-hidden="true"><g fill="currentColor">' +
    '<circle cx="6" cy="4" r="3"/><circle cx="16" cy="4" r="3"/><circle cx="11" cy="8" r="6"/>' +
    '<ellipse cx="11" cy="17.5" rx="7" ry="7.5"/><circle cx="4" cy="14" r="2.6"/><circle cx="18" cy="14" r="2.6"/>' +
    '<circle cx="6.5" cy="23" r="3"/><circle cx="15.5" cy="23" r="3"/></g>' +
    '<circle cx="8.5" cy="7" r="1.6" fill="#fff" opacity=".45"/></svg>';

  function accentFor(el) {
    var c = getComputedStyle(el).getPropertyValue('--accent').trim();
    if (!c) {
      var host = document.querySelector('.gumis-accent-media, [data-gumis-accent]');
      if (host) c = getComputedStyle(host).getPropertyValue('--accent').trim();
    }
    return c || '#12898A';
  }
  function cartTarget() {
    var el = document.querySelector('#cart-icon-bubble, [data-gumis-cart-icon], .header__icon--cart');
    if (el) {
      var r = el.getBoundingClientRect();
      if (r.width) return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
    }
    return { x: window.innerWidth - 40, y: 40 };
  }
  function pop(button) {
    var r = button.getBoundingClientRect();
    var from = { x: r.left + r.width / 2, y: r.top + r.height / 2 };
    var to = cartTarget();
    var color = accentFor(button);
    for (var i = 0; i < 7; i++) {
      (function (i) {
        var g = document.createElement('span');
        g.className = 'g-pop';
        g.innerHTML = BEAR;
        g.style.color = i % 3 === 1 ? '#FF8A3D' : color;
        document.body.appendChild(g);
        var spread = (i - 3) * 26 + (Math.random() - 0.5) * 20;
        var peak = 90 + Math.random() * 70;
        var spin = (Math.random() - 0.5) * 540;
        var sx = from.x - 11, sy = from.y - 13;
        var anim = g.animate([
          { transform: 'translate(' + sx + 'px,' + sy + 'px) scale(.4) rotate(0deg)', opacity: 0 },
          { transform: 'translate(' + (sx + spread) + 'px,' + (sy - peak) + 'px) scale(1.15) rotate(' + spin / 2 + 'deg)', opacity: 1, offset: 0.35 },
          { transform: 'translate(' + (to.x - 11) + 'px,' + (to.y - 13) + 'px) scale(.35) rotate(' + spin + 'deg)', opacity: 0.9 }
        ], { duration: 900 + i * 40, delay: i * 45, easing: 'cubic-bezier(.3,.7,.4,1)', fill: 'forwards' });
        anim.onfinish = function () { g.remove(); };
      })(i);
    }
    var cart = document.querySelector('#cart-icon-bubble, [data-gumis-cart-icon], .header__icon--cart');
    if (cart && cart.animate) {
      cart.animate([{ transform: 'scale(1)' }, { transform: 'scale(1.25)' }, { transform: 'scale(1)' }], { duration: 400, delay: 950, easing: 'ease-out' });
    }
  }
  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (!(form instanceof HTMLFormElement)) return;
    var action = form.getAttribute('action') || '';
    var isAdd = action.indexOf('/cart/add') !== -1 || form.matches('[data-type="add-to-cart-form"], .product-form, #pf') || form.querySelector('input[name="id"]');
    if (!isAdd) return;
    var button = e.submitter || form.querySelector('[type="submit"]') || document.querySelector('button[form="' + form.id + '"]');
    if (button) pop(button);
  }, true);
})();

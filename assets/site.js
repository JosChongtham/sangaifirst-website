// Sangai First Foundation: carousels, slideshows, quiz and year switch.
(function () {
  var reduce = function () {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  };

  // Horizontal carousels: arrow buttons scroll the visible track.
  document.querySelectorAll('[data-carousel]').forEach(function (c) {
    c.querySelectorAll('[data-scroll]').forEach(function (b) {
      b.addEventListener('click', function () {
        var t = c.querySelector('[data-track]:not([hidden])');
        t.scrollBy({ left: Number(b.dataset.scroll) * t.clientWidth * 0.8, behavior: reduce() ? 'auto' : 'smooth' });
      });
    });
  });

  // Slideshows (Home hero, Discover topics): one slide visible at a time.
  document.querySelectorAll('[data-slideshow]').forEach(function (root) {
    var slides = Array.prototype.slice.call(root.querySelectorAll('[data-slide]'));
    var pickers = Array.prototype.slice.call(root.querySelectorAll('[data-go]'));
    var cur = 0;
    function show(i) {
      cur = (i + slides.length) % slides.length;
      slides.forEach(function (s, j) { s.hidden = j !== cur; });
      pickers.forEach(function (p) {
        var on = String(Number(p.dataset.go) === cur);
        p.setAttribute(p.getAttribute('role') === 'tab' ? 'aria-selected' : 'aria-current', on);
      });
    }
    root.querySelector('[data-prev]').addEventListener('click', function () { show(cur - 1); });
    root.querySelector('[data-next]').addEventListener('click', function () { show(cur + 1); });
    pickers.forEach(function (p) {
      p.addEventListener('click', function () { show(Number(p.dataset.go)); });
    });
    root.addEventListener('keydown', function (ev) {
      if (ev.target.closest('a')) return;
      if (ev.key === 'ArrowLeft') { show(cur - 1); }
      else if (ev.key === 'ArrowRight') { show(cur + 1); }
    });
    show(0);
  });

  // Quiz: reveal an answer and move focus to it.
  document.querySelectorAll('[data-reveal]').forEach(function (b) {
    b.addEventListener('click', function () {
      var a = b.parentElement.querySelector('[data-answer]');
      a.hidden = false;
      a.focus();
      b.remove();
    });
  });

  // Programme details dialogs.
  document.querySelectorAll('[data-open]').forEach(function (b) {
    var d = document.getElementById(b.dataset.open);
    if (!d || !d.showModal) return;
    b.addEventListener('click', function () { d.showModal(); });
    d.addEventListener('click', function (ev) { if (ev.target === d) d.close(); });
  });

  // Year switch on Our Work.
  document.querySelectorAll('[data-years]').forEach(function (group) {
    var c = group.closest('[data-carousel]');
    group.querySelectorAll('[data-year]').forEach(function (b) {
      b.addEventListener('click', function () {
        group.querySelectorAll('[data-year]').forEach(function (o) {
          o.setAttribute('aria-pressed', String(o === b));
        });
        c.querySelectorAll('[data-panel]').forEach(function (p) {
          p.hidden = p.dataset.panel !== b.dataset.year;
          p.scrollLeft = 0;
        });
      });
    });
  });
})();

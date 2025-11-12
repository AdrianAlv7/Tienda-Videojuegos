// static/js/cart.js
(() => {
  // ---------- Cache de elementos base ----------
  const panel   = document.getElementById("carrito-panel");
  const overlay = document.getElementById("overlay-carrito");
  const btnOpen = document.getElementById("btn-carrito");
  const btnClose= document.getElementById("cerrar-carrito");
  const itemsEl = document.getElementById("carrito-items");
  const badge   = document.getElementById("cart-badge");

  if (!panel || !overlay || !itemsEl) {
    console.warn("[Cart] Falta el markup del panel/overlay en base.html");
    return;
  }

  // ---------- Utils ----------
  const showOverlay = () => {
    overlay.style.display = "block";
    requestAnimationFrame(() => { overlay.style.opacity = "1"; });
  };
  const hideOverlay = () => {
    overlay.style.opacity = "0";
    setTimeout(() => { overlay.style.display = "none"; }, 300);
  };
  const setBodyLock = (lock) => {
    document.body.style.overflow = lock ? "hidden" : "";
  };

  const actualizarBadge = (count) => {
    if (!badge) return;
    badge.textContent = count;
    badge.style.display = (+count > 0) ? "inline-flex" : "none";
  };

  // ---------- Rutas ----------
  const rutas = {
    ver      : window.__URLS__?.carrito_ver,
    agregar  : window.__URLS__?.carrito_agregar,
    quitar   : window.__URLS__?.carrito_quitar,
    conteo   : window.__URLS__?.carrito_conteo,
    biblioteca: window.__URLS__?.biblioteca,
  };

  // ---------- Funciones base ----------
  const cargarPanel = async () => {
    const res = await fetch(rutas.ver, { headers: {"X-Requested-With":"XMLHttpRequest"} });
    const html = await res.text();
    itemsEl.innerHTML = html;
    inicializarBotonesEliminar();
    actualizarTotalCarrito();
  };

  const open = async () => {
    panel.classList.add("show");
    showOverlay();
    setBodyLock(true);
    await cargarPanel();
  };

  const close = () => {
    panel.classList.remove("show");
    hideOverlay();
    setBodyLock(false);
  };

  const add = async (productId) => {
    const res = await fetch(rutas.agregar, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ id_producto: Number(productId) })
    });
    const data = await res.json();
    if (data?.ok) {
      actualizarBadge(data.count);
      await open(); // abre el panel con el nuevo producto
      const btn = document.querySelector(`[data-product-id="${productId}"]`);
      if (btn) {
        btn.dataset.state = "carrito";
        btn.textContent = "En carrito";
        btn.classList.remove("btn-success", "btn-secondary");
        btn.classList.add("btn-warning");
      }
      mostrarAvisoCarrito("Agregado al carrito 🛒");
    }
  };

  const remove = async (productId) => {
    const res = await fetch(rutas.quitar, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ id_producto: Number(productId) })
    });
    const data = await res.json();
    if (data?.ok) {
      actualizarBadge(data.count ?? 0);
      await cargarPanel();
      const btn = document.querySelector(`[data-product-id="${productId}"]`);
      if (btn) {
        btn.dataset.state = "ninguno";
        btn.textContent = "Agregar al carrito";
        btn.classList.remove("btn-warning", "btn-secondary");
        btn.classList.add("btn-success");
      }
      mostrarAvisoCarrito("Producto eliminado 🗑️");
    }
  };

  const refrescarConteo = async () => {
    try {
      const r = await fetch(rutas.conteo, { cache: "no-store" });
      const j = await r.json();
      actualizarBadge(j.count ?? 0);
    } catch {}
  };

  // ---------- Total dinámico ----------
  function actualizarTotalCarrito() {
    const precios = Array.from(document.querySelectorAll(".carrito-item .precio"))
      .map(p => parseFloat(p.textContent.replace("$", "")) || 0);
    const total = precios.reduce((acc, val) => acc + val, 0);
    const totalEl = document.getElementById("carrito-total");
    if (totalEl) totalEl.textContent = `$${total.toFixed(2)}`;
  }

  // ---------- Inicializa eventos de eliminación ----------
  function inicializarBotonesEliminar() {
    document.querySelectorAll(".btn-eliminar").forEach(btn => {
      btn.addEventListener("click", async () => {
        const item = btn.closest(".carrito-item");
        const idProducto = item?.dataset.id;
        if (!idProducto) return;
        await remove(idProducto);
      });
    });
  }

  // ---------- Delegación global ----------
  document.addEventListener("click", async (e) => {
    const btn = e.target.closest("[data-product-id]");
    if (!btn) return;

    const id = btn.dataset.productId;
    const state = btn.dataset.state;

    if (state === "biblioteca") {
      window.location.href = rutas.biblioteca ?? "#";
      return;
    }

    if (state === "carrito") {
      await open();
      return;
    }

    // Si está en "ninguno"
    await add(id);
  });

  // ---------- Eventos del panel ----------
  if (btnOpen) btnOpen.addEventListener("click", async (e) => { e.preventDefault(); await open(); });
  if (btnClose) btnClose.addEventListener("click", close);
  overlay.addEventListener("click", close);
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") close(); });

  // ---------- Init ----------
  refrescarConteo();

  // ---------- Exponer API global ----------
  window.Cart = { open, close, add, remove, refrescarConteo };
})();


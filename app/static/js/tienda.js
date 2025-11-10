// 🛒 Carrito de compras (usando localStorage para persistir)
let carrito = JSON.parse(localStorage.getItem('carrito')) || [];

// Actualiza la vista del carrito al cargar
window.onload = () => {
    actualizarCarrito();
};

// Agregar producto al carrito
function agregarAlCarrito(id, nombre, precio) {
    // Verificar si ya existe
    if (carrito.find(item => item.id === id)) {
        alert("Este producto ya está en el carrito.");
        return;
    }

    // Agregar producto
    carrito.push({ id, nombre, precio: parseFloat(precio) });
    localStorage.setItem('carrito', JSON.stringify(carrito));
    actualizarCarrito();

    // Desactivar botón
    const boton = document.getElementById(`btn-${id}`);
    if (boton) {
        boton.disabled = true;
        boton.innerText = "En carrito";
    }
}

// Eliminar producto del carrito
function eliminarDelCarrito(id) {
    carrito = carrito.filter(item => item.id !== id);
    localStorage.setItem('carrito', JSON.stringify(carrito));
    actualizarCarrito();

    // Reactivar botón de agregar
    const boton = document.getElementById(`btn-${id}`);
    if (boton) {
        boton.disabled = false;
        boton.innerText = "Agregar al carrito";
    }
}

// Actualizar interfaz del carrito
function actualizarCarrito() {
    const lista = document.getElementById("lista-carrito");
    const totalCarrito = document.getElementById("total-carrito");

    lista.innerHTML = "";

    let total = 0;
    carrito.forEach(item => {
        const li = document.createElement("li");
        li.innerHTML = `
            ${item.nombre} - $${item.precio.toFixed(2)}
            <button onclick="eliminarDelCarrito('${item.id}')" class="btn btn-sm btn-danger ms-2">❌</button>
        `;
        lista.appendChild(li);
        total += item.precio;

        // Marcar botón de producto como deshabilitado
        const boton = document.getElementById(`btn-${item.id}`);
        if (boton) {
            boton.disabled = true;
            boton.innerText = "En carrito 🛒";
        }
    });

    totalCarrito.innerText = `$${total.toFixed(2)}`;
}

// Simular botón de pagar
document.getElementById("btnPagar").addEventListener("click", () => {
    if (carrito.length === 0) {
        alert("El carrito está vacío.");
        return;
    }

    document.getElementById("message").style.display = "block";
    setTimeout(() => {
        alert("¡Compra simulada con éxito!");
        carrito = [];
        localStorage.removeItem('carrito');
        actualizarCarrito();
        document.getElementById("message").style.display = "none";
    }, 2000);
});
async function realizarCompra() {
  if (carrito.length === 0) {
    alert("Tu carrito está vacío.");
    return;
  }

  const total = carrito.reduce((acc, item) => acc + parseFloat(item.precio), 0);

  const response = await fetch("/comprar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ carrito, total }),
  });

  const data = await response.json();

  if (response.ok) {
    alert(data.mensaje);
    carrito = [];
    actualizarCarrito();
  } else {
    alert("Error al realizar la compra: " + data.error);
  }
}

document.getElementById("btnPagar").addEventListener("click", realizarCompra);

   // Obtener datos del carrito almacenado en el localStorage
    let carrito = JSON.parse(localStorage.getItem("carrito")) || [];
    let total = localStorage.getItem("total") || "0.00";

    // Mostrar productos en la lista del carrito
    const listaCarrito = document.getElementById("lista-carrito");
    carrito.forEach(item => {
      const li = document.createElement("li");
      // Crear un elemento de lista con la cantidad, nombre del producto y precio total
      li.innerHTML = `${item.cantidad}x ${item.producto} - $${(item.precio * item.cantidad).toFixed(2)}`;
      listaCarrito.appendChild(li);
    });

    // Mostrar el total en la sección correspondiente
    document.getElementById("total-carrito").textContent = `$${total}`;

    // Función para confirmar la compra
    function confirmarCompra() {
      // Mensaje de confirmación de la compra
      alert("Compra confirmada. ¡Gracias por tu compra!");
      // Limpiar el carrito en el localStorage
      localStorage.removeItem("carrito");
      localStorage.removeItem("total");
      // Redirigir al usuario de vuelta a la tienda
      window.location.href = "Tienda.html"; 
    }
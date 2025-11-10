// Espera a que el contenido del DOM se haya cargado completamente
document.addEventListener('DOMContentLoaded', function() {
  // Agrega un evento de clic al botón de alternar menú
  document.getElementById('menu-toggle').addEventListener('click', function() {
      // Alterna la clase 'toggled' en el elemento 'wrapper'
      document.getElementById('wrapper').classList.toggle('toggled');
  });
});

// Enseñar el mensaje de "Buscando Dispositivos..."
document.getElementById("searchBtn").addEventListener("click", function(event) {
  event.preventDefault(); // Evita que el formulario se envíe
  document.getElementById("message").style.display = "block"; // Muestra el mensaje
});

// Selecciona todos los elementos de la lista que tienen la clase 'list-group-item'
const items = document.querySelectorAll('.list-group-item');

// Añadimos un evento de clic a cada ítem de la lista
items.forEach(item => {
  item.addEventListener('click', function() {
      // Alternar la clase 'checked' para añadir o quitar la palomita
      item.classList.toggle('checked');
  });
});

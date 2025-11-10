// Función para mostrar/ocultar la calculadora
const calculadoraToggle = document.getElementById('calculadora-toggle'); // Elemento del botón para alternar
const calculadora = document.getElementById('calculadora'); // Elemento de la calculadora

// Evento para alternar la visibilidad de la calculadora
calculadoraToggle.addEventListener('click', function() {
    calculadora.classList.toggle('active'); // Alternar la clase 'active' para mostrar/ocultar
});

// Variables para la calculadora
const display = document.querySelector(".display"); // Pantalla de la calculadora
const buttons = document.querySelectorAll("button"); // Todos los botones de la calculadora

let currentInput = ""; // Entrada actual del usuario
let currentOperator = ""; // Operador actual
let shouldClearDisplay = false; // Indicador para limpiar la pantalla

// Evento para cada botón
buttons.forEach((button) => {
    button.addEventListener("click", () => {
        const buttonText = button.textContent; // Texto del botón presionado

        // Manejo de dígitos
        if (buttonText.match(/[0-9]/)) {
            if (shouldClearDisplay) {
                display.textContent = ""; // Limpiar pantalla si es necesario
                shouldClearDisplay = false; // Restablecer indicador
            }
            // Si la pantalla muestra "0", reemplazarlo con el nuevo dígito
            if (display.textContent === "0") {
                display.textContent = buttonText;
            } else {
                display.textContent += buttonText; // Agregar dígito a la pantalla
            }
        } 
        // Manejo del botón "C" para limpiar
        else if (buttonText === "C") {
            display.textContent = "0"; // Reiniciar pantalla
            currentInput = ""; // Reiniciar entrada
            currentOperator = ""; // Reiniciar operador
        } 
        // Manejo del botón "←" para borrar un dígito
        else if (buttonText === "←") {
            if (display.textContent.length > 1) 
                {
                display.textContent = display.textContent.slice(0, -1); // Borrar último dígito
            } else {
                display.textContent = "0"; // Reiniciar a "0" si no hay más dígitos
            }
        } 
        // Manejo del botón "=" para calcular
        else if (buttonText === "=") {
            if (currentOperator && currentInput) {
                const result = calculate(parseFloat(currentInput), currentOperator, parseFloat(display.textContent)); 
                //se utiliza para realizar un cálculo basado en la entrada actual y el operador seleccionado
                display.textContent = result; // Mostrar resultado
                currentInput = result; // Guardar resultado como entrada actual
                currentOperator = ""; // Reiniciar operador
                shouldClearDisplay = true; // Preparar para limpiar pantalla en la próxima entrada
            }
        } 
        // Manejo del botón "√" para calcular la raíz cuadrada
        else if (buttonText === "√") {
            const result = Math.sqrt(parseFloat(display.textContent));
            //calcular la raíz cuadrada de un número ingresado por el usuario
            display.textContent = result; // Mostrar resultado
            currentInput = result; // Guardar resultado como entrada actual
            shouldClearDisplay = true; // Preparar para limpiar pantalla
        } 
        // Manejo del botón "%" para calcular el porcentaje
        else if (buttonText === "%") {
            if (currentInput) {
                const percentage = parseFloat(display.textContent) / 100;
                //calcular el porcentaje de un número ingresado por el usuario
                display.textContent = percentage; // Mostrar porcentaje
                currentInput = percentage; // Guardar resultado como entrada actual
                currentOperator = ""; // Reiniciar operador
                shouldClearDisplay = true; // Preparar para limpiar pantalla
            }
        } 
        // Manejo de operadores
        else {
            currentOperator = buttonText; // Guardar operador actual
            currentInput = display.textContent; // Guardar entrada actual
            shouldClearDisplay = true; // Preparar para limpiar pantalla
        }
    });
});

// Función para calcular
function calculate(num1, operator, num2) {
    switch (operator) {
        case "+":
            return num1 + num2; // Suma
        case "-":
            return num1 - num2; // Resta
        case "*":
            return num1 * num2; // Multiplicación
        case "/":
            return num2 !== 0 ? num1 / num2 : "Error"; // División (manejo de división por cero)
        case "^":
            return Math.pow(num1, num2); // Potencia
        default:
            return num2; // Retornar el segundo número si no es un operador válido
    }
}
 // Objeto para almacenar datos anteriores antes de la edición
    let previousData = {};

    // Función para guardar los datos actuales antes de editar
    function savePreviousData() {
        previousData.username = document.getElementById('username').innerText;
        previousData.email = document.getElementById('email').innerText.replace('Correo: ', '');
        previousData.age = document.getElementById('age').innerText;
        previousData.height = document.getElementById('height').innerText;
        previousData.weight = document.getElementById('weight').innerText;
        previousData.goal = document.getElementById('goal').innerText;
    }

    // Evento para el botón de editar/guardar
    document.getElementById('edit-button').addEventListener('click', function() {
        const username = document.getElementById('username');
        const email = document.getElementById('email');
        const age = document.getElementById('age');
        const height = document.getElementById('height');
        const weight = document.getElementById('weight');
        const goal = document.getElementById('goal');

        if (this.innerText === 'Editar') {
            // Guardar datos anteriores antes de editar
            savePreviousData();

            // Crear campos de entrada para editar la información
            username.innerHTML = `<input type="text" value="${username.innerText}">`;
            email.innerHTML = `Correo: <input type="text" value="${email.innerText.replace('Correo: ', '')}">`;
            age.innerHTML = `<input type="number" value="${age.innerText}">`;
            height.innerHTML = `<input type="number" step="0.01" value="${height.innerText}">`;
            weight.innerHTML = `<input type="number" value="${weight.innerText}">`;
            goal.innerHTML = `<input type="text" value="${goal.innerText}">`;

            // Cambiar el texto del botón a "Guardar"
            this.innerText = 'Guardar';
            document.getElementById('restore-button').style.display = 'inline-block';
        } else {
            // Guardar los cambios realizados
            username.innerText = username.querySelector('input').value;
            email.innerText = `Correo: ${email.querySelector('input').value}`;
            age.innerText = age.querySelector('input').value;
            height.innerText = height.querySelector('input').value;
            weight.innerText = weight.querySelector('input').value;
            goal.innerText = goal.querySelector('input').value;

            // Cambiar el texto del botón de vuelta a "Editar"
            this.innerText = 'Editar';
            document.getElementById('restore-button').style.display = 'none';
        }
    });

    // Evento para el botón de restaurar
    document.getElementById('restore-button').addEventListener('click', function() {
        // Restaurar los datos anteriores
        document.getElementById('username').innerText = previousData.username;
        document.getElementById('email').innerText = `Correo: ${previousData.email}`;
        document.getElementById('age').innerText = previousData.age;
        document.getElementById('height').innerText = previousData.height;
        document.getElementById('weight').innerText = previousData.weight;
        document.getElementById('goal').innerText = previousData.goal;

        // Ocultar el botón de restaurar
        this.style.display = 'none';
        document.getElementById('edit-button').innerText = 'Editar';
    });
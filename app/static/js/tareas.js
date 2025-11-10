    // Evento para mostrar/ocultar el menú lateral
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });

    // Evento para mostrar el formulario de nueva tarea al hacer clic en el botón
    $("#new-task-button").click(function() {
        $("#new-task-form").toggle();
    });

    // Evento para guardar la nueva tarea
    $("#save-button").click(function() {
        const title = $("#task-title").val(); // Obtener el título de la tarea
        const description = $("#task-description").val(); // Obtener la descripción de la tarea

        // Verificar que ambos campos no estén vacíos
        if (title && description) {
            // Crear el HTML para la nueva tarea
            const newTaskHtml = `
                <div class="col-md-6">
                    <h2>${title}</h2>
                    <p>${description}</p>
                    <button class="btn btn-primary">Completar</button>
                </div>
            `;
            // Añadir la nueva tarea a la lista de tareas
            $("#task-list").append(newTaskHtml);

            // Limpiar el formulario
            $("#task-title").val('');
            $("#task-description").val('');
            $("#new-task-form").hide(); // Ocultar el formulario después de guardar
        } else {
            alert("Por favor, completa todos los campos."); // Mensaje de alerta si faltan campos
        }
    });
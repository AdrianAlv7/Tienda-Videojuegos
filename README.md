# ActiveLife – Sistema de Gestión Deportiva y Bienestar

Proyecto final de Backend y Bases de Datos  
Autor: Adrian Alvarez Ochoa y  Kevin Eduardo López Magaña
Correo: a21490519@itmexicali.edu.mx     a22490076@itmexicali.edu.mx

---

## Descripción

ActiveLife es una aplicación web desarrollada con Flask y MySQL para gestionar usuarios con diferentes roles (admin, editor, cliente), administrar productos, realizar ventas, visualizar historiales de compras y editar el perfil. Incluye autenticación segura, control de acceso por roles, y un diseño responsivo.

---

## Requisitos de la aplicación

- Python 3.10 o superior
- MySQL Server 8.x
- Pip (gestor de paquetes Python)

---

## Instalación

1. **Clona el repositorio:**
    ```sh
    git clone https://github.com/TU-USUARIO/activelife.git
    cd activelife
    ```

2. **Configura la base de datos:**
    - Abre MySQL y ejecuta el script `/database/scripts.sql` para crear la base y los datos iniciales.
    - Ajusta tu usuario y contraseña de MySQL en `config.py`.

3. **Instala las dependencias:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Inicia la aplicación:**
    ```sh
    python run.py
    ```

5. **Abre el navegador:**  
    [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Instrucciones de uso

- **Usuarios predefinidos:**
    - Admin:  
      Usuario: `admin`  
      Contraseña:  `admin123`
    - Los clientes pueden registrarse desde la página de login.
---

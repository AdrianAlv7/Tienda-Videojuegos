from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import mysql
from app.utils.decorators import roles_required
from werkzeug.utils import secure_filename
import os


# ==============================
# 📦 CONFIGURACIÓN DEL BLUEPRINT
# ==============================
productos_bp = Blueprint('productos', __name__)

# === 📂 RUTAS DE IMÁGENES ===
BASE_IMG_PATH = os.path.join('app', 'static', 'IMG')
# 📂 Rutas de imágenes
UPLOADS_PRODUCTOS = os.path.join('app', 'static', 'IMG', 'productos')
os.makedirs(UPLOADS_PRODUCTOS, exist_ok=True)



# === Extensiones permitidas ===
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# ==============================
# 🔹 FUNCIONES AUXILIARES
# ==============================
def allowed_file(filename):
    """Verifica si el archivo tiene una extensión válida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def guardar_imagen(imagen, carpeta):
    """Guarda una imagen en la carpeta indicada y devuelve el nombre seguro."""
    if imagen and allowed_file(imagen.filename):
        filename = secure_filename(imagen.filename)
        imagen.save(os.path.join(carpeta, filename))
        return filename
    return None

# 🧾 Mostrar lista de productos
@productos_bp.route('/productos')
@login_required
@roles_required(['admin', 'editor'])
def lista_productos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, descripcion, precio, imagen FROM productos")
    productos = cur.fetchall()
    cur.close()
    return render_template('productos/lista.html', productos=productos)

# ➕ Agregar nuevo producto
@productos_bp.route('/productos/agregar', methods=['GET', 'POST'])
@login_required
@roles_required(['admin', 'editor'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']

        # Imagen principal
        imagen = request.files.get('imagen')
        imagen_nombre = guardar_imagen(imagen, UPLOADS_PRODUCTOS)

        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO productos (nombre, descripcion, imagen, precio) VALUES (%s, %s, %s, %s)',
            (nombre, descripcion, imagen_nombre, precio)
        )
        producto_id = cur.lastrowid

        # Imágenes adicionales
        imagenes_extra = request.files.getlist('imagenes_extra')
        for img in imagenes_extra:
            filename = guardar_imagen(img, UPLOADS_PRODUCTOS)
            if filename:
                cur.execute(
                    "INSERT INTO imagenes_producto (producto_id, nombre_imagen) VALUES (%s, %s)",
                    (producto_id, filename)
                )

        mysql.connection.commit()
        cur.close()

        flash('Producto agregado correctamente.', 'success')
        return redirect(url_for('productos.lista_productos'))

    return render_template('productos/formulario.html', accion='Agregar')

# ✏️ Editar producto existente
@productos_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_required(['admin', 'editor'])
def editar_producto(id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        imagen = request.files.get('imagen')
        eliminar_imagen = 'eliminar_imagen' in request.form

        # CASO 1: Eliminar imagen
        if eliminar_imagen:
            cur.execute("""
                UPDATE productos SET nombre=%s, descripcion=%s, imagen=NULL, precio=%s WHERE id=%s
            """, (nombre, descripcion, precio, id))

        # CASO 2: Subir nueva imagen
        elif imagen and allowed_file(imagen.filename):
            filename = guardar_imagen(imagen, UPLOADS_PRODUCTOS)
            cur.execute("""
                UPDATE productos SET nombre=%s, descripcion=%s, imagen=%s, precio=%s WHERE id=%s
            """, (nombre, descripcion, filename, precio, id))

        # CASO 3: Mantener imagen
        else:
            cur.execute("""
                UPDATE productos SET nombre=%s, descripcion=%s, precio=%s WHERE id=%s
            """, (nombre, descripcion, precio, id))

        # Guardar imágenes adicionales
        imagenes_extra = request.files.getlist('imagenes_extra')
        for img in imagenes_extra:
            filename = guardar_imagen(img, UPLOADS_PRODUCTOS)
            if filename:
                cur.execute("""
                    INSERT INTO imagenes_producto (producto_id, nombre_imagen)
                    VALUES (%s, %s)
                """, (id, filename))

        mysql.connection.commit()
        cur.close()

        flash('Producto actualizado correctamente ✅', 'success')
        return redirect(url_for('productos.lista_productos'))

    # Si es GET → mostrar datos actuales
    cur.execute("SELECT * FROM productos WHERE id = %s", (id,))
    producto = cur.fetchone()
    cur.close()

    return render_template('productos/formulario.html', accion='Editar', producto=producto)

# ❌ Eliminar producto
@productos_bp.route('/productos/eliminar/<int:id>', methods=['POST', 'GET'])
@login_required
@roles_required(['admin'])
def eliminar_producto(id):
    cur = mysql.connection.cursor()
    
    try:
        # 🧹 Primero eliminamos las referencias al producto en otras tablas
        cur.execute("DELETE FROM biblioteca WHERE id_producto = %s", (id,))
        cur.execute("DELETE FROM detalle_ventas WHERE producto_id = %s", (id,))
        cur.execute("DELETE FROM imagenes_producto WHERE producto_id = %s", (id,))

        # 🗑️ Luego eliminamos el producto en sí
        cur.execute("DELETE FROM productos WHERE id = %s", (id,))

        mysql.connection.commit()
        flash('Producto eliminado correctamente.', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al eliminar el producto: {e}', 'danger')
    finally:
        cur.close()

    return redirect(url_for('productos.lista_productos'))

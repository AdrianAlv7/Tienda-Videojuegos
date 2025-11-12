from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_required, current_user
from app import mysql
from datetime import datetime
from flask import Blueprint
from werkzeug.utils import secure_filename
import os

# === CONFIGURACIÓN DE RUTAS E IMÁGENES ===
main_bp = Blueprint('main', __name__)

# Ruta base donde se guardan las imágenes
BASE_IMG_PATH = os.path.join('app', 'static', 'IMG')

# Subcarpetas específicas para distintos tipos de archivos
UPLOADS_PERFIL = os.path.join(BASE_IMG_PATH, 'perfiles')
UPLOADS_PRODUCTOS = os.path.join(BASE_IMG_PATH, 'productos')

# Crear las carpetas si no existen
os.makedirs(UPLOADS_PERFIL, exist_ok=True)
os.makedirs(UPLOADS_PRODUCTOS, exist_ok=True)

# === FUNCIÓN AUXILIAR PARA GUARDAR IMÁGENES ===
def guardar_imagen(archivo, carpeta):
    """Guarda una imagen de forma segura en la carpeta especificada."""
    if archivo and archivo.filename:
        filename = secure_filename(archivo.filename)
        ruta_guardado = os.path.join(carpeta, filename)
        archivo.save(ruta_guardado)
        return filename
    return None


# ======================================================
# 🏠 PÁGINA PRINCIPAL
# ======================================================
@main_bp.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, descripcion, precio, imagen FROM productos ORDER BY id DESC LIMIT 10")
    juegos = [
        {'id': r[0], 'nombre': r[1], 'descripcion': r[2], 'precio': r[3], 'imagen': r[4]}
        for r in cur.fetchall()
    ]
    cur.close()
    return render_template('index.html', juegos=juegos, active_page='index')




# ======================================================
# 👤 PERFIL DE USUARIO
# ======================================================
@main_bp.route('/perfil')
@login_required
def perfil():
    cur = mysql.connection.cursor()

    # Datos del usuario
    cur.execute("""
        SELECT username, email, descripcion, foto_perfil, banner
        FROM usuarios WHERE id = %s
    """, (current_user.id,))
    user = cur.fetchone()

    # Juegos de la biblioteca del usuario
    cur.execute("""
        SELECT p.nombre, p.imagen, b.fecha_adquirido
        FROM biblioteca b
        JOIN productos p ON b.id_producto = p.id
        WHERE b.id_usuario = %s
        ORDER BY b.fecha_adquirido DESC
    """, (current_user.id,))
    juegos = cur.fetchall()

    cur.close()

    return render_template('perfil.html', user=user, juegos=juegos, active_page='perfil')


# ======================================================
# ✏️ EDITAR PERFIL
# ======================================================
@main_bp.route('/perfil/editar', methods=['POST'])
@login_required
def editar_perfil_usuario():
    username = request.form.get('username')
    descripcion = request.form.get('descripcion')
    foto = request.files.get('foto_perfil')
    banner = request.files.get('banner')

    foto_nombre = guardar_imagen(foto, UPLOADS_PERFIL)
    banner_nombre = guardar_imagen(banner, UPLOADS_PERFIL)


    cur = mysql.connection.cursor()

    # Actualizar foto de perfil
    if foto and foto.filename:
        foto_nombre = secure_filename(foto.filename)
        foto.save(os.path.join('app/static/IMG', foto_nombre))
        cur.execute("UPDATE usuarios SET foto_perfil = %s WHERE id = %s", (foto_nombre, current_user.id))

    # Actualizar banner
    if banner and banner.filename:
        banner_nombre = secure_filename(banner.filename)
        banner.save(os.path.join('app/static/IMG', banner_nombre))
        cur.execute("UPDATE usuarios SET banner = %s WHERE id = %s", (banner_nombre, current_user.id))

    # Actualizar nombre y descripción
    cur.execute("""
        UPDATE usuarios
        SET username = %s, descripcion = %s
        WHERE id = %s
    """, (username, descripcion, current_user.id))

    mysql.connection.commit()
    cur.close()

    flash("Perfil actualizado correctamente.", "success")
    return redirect(url_for('main.perfil'))


# ======================================================
# 🎮 BIBLIOTECA
# ======================================================
@main_bp.route('/biblioteca')
@login_required
def biblioteca():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.id, p.nombre, p.descripcion, p.imagen, b.fecha_adquirido
        FROM biblioteca b
        JOIN productos p ON b.id_producto = p.id
        WHERE b.id_usuario = %s
        ORDER BY b.fecha_adquirido DESC
    """, (current_user.id,))
    resultados = cur.fetchall()
    cur.close()

    juegos = [
        {
            'id': r[0],
            'nombre': r[1],
            'descripcion': r[2],
            'imagen': r[3],
            'fecha_adquirido': r[4].strftime("%d/%m/%Y")
        }
        for r in resultados
    ]

    return render_template('biblioteca.html', juegos=juegos, active_page='biblioteca')


# ======================================================
# ✅ COMPRAR (CARRITO)
# ======================================================
@main_bp.route('/comprar', methods=['POST'])
@login_required
def comprar():
    data = request.get_json()
    carrito = data.get('carrito', [])
    total = data.get('total', 0)

    if not carrito:
        return jsonify({'error': 'El carrito está vacío.'}), 400

    cur = mysql.connection.cursor()

    # Crear la venta
    cur.execute("INSERT INTO ventas (usuario_id, total) VALUES (%s, %s)", (current_user.id, total))
    venta_id = cur.lastrowid

    # Registrar detalles y biblioteca
    for item in carrito:
        producto_id = item['id']
        precio = item['precio']

        cur.execute("""
            INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal)
            VALUES (%s, %s, 1, %s, %s)
        """, (venta_id, producto_id, precio, precio))

        cur.execute("""
            INSERT INTO biblioteca (id_usuario, id_producto)
            VALUES (%s, %s)
        """, (current_user.id, producto_id))

    mysql.connection.commit()
    cur.close()

    return jsonify({'mensaje': 'Compra registrada con éxito.'}), 200


# ======================================================
# 🕹️ TIENDA
# ======================================================
@main_bp.route('/tienda')
@login_required
def tienda():
    cur = mysql.connection.cursor()

    # 🕹️ Obtener productos
    cur.execute("SELECT id, nombre, descripcion, precio, imagen FROM productos")
    productos = cur.fetchall()

    # 🎮 Juegos que el usuario ya tiene en la biblioteca
    cur.execute("SELECT id_producto FROM biblioteca WHERE id_usuario = %s", (current_user.id,))
    juegos_biblioteca = [r[0] for r in cur.fetchall()]

    # 🛒 Juegos que el usuario tiene en el carrito
    cur.execute("SELECT id_producto FROM carrito WHERE id_usuario = %s", (current_user.id,))
    juegos_carrito = [r[0] for r in cur.fetchall()]

    cur.close()

    # 🎨 Estructurar lista con estados
    juegos = []
    for p in productos:
        estado = "ninguno"
        if p[0] in juegos_biblioteca:
            estado = "biblioteca"
        elif p[0] in juegos_carrito:
            estado = "carrito"

        juegos.append({
            'id': p[0],
            'nombre': p[1],
            'descripcion': p[2],
            'precio': p[3],
            'imagen': p[4],
            'estado': estado
        })

    return render_template('tienda.html', juegos=juegos, active_page='tienda')



# ======================================================
# 💳 PROCESAR COMPRA
# ======================================================
@main_bp.route('/procesar_compra', methods=['POST'])
@login_required
def procesar_compra():
    try:
        data = request.get_json()
        juegos = data.get('juegos')
        total = data.get('total')

        id_usuario = current_user.id
        cur = mysql.connection.cursor()

        # Registrar venta
        cur.execute("""
            INSERT INTO ventas (id_usuario, total)
            VALUES (%s, %s)
        """, (id_usuario, total))
        venta_id = cur.lastrowid

        # Registrar detalle y biblioteca
        for j in juegos:
            cur.execute("""
                INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                VALUES (%s, %s, 1, 0, 0)
            """, (venta_id, j['id']))  # 👈 usa 'venta_id' como en la base

            cur.execute("""
                INSERT IGNORE INTO biblioteca (id_usuario, id_producto)
                VALUES (%s, %s)
            """, (id_usuario, j['id']))

        mysql.connection.commit()
        cur.close()

        return jsonify({'success': True})

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500



# ======================================================
# 🔙 DETALLE DEL JUEGO
# ======================================================
@main_bp.route('/juego/<int:id>')
@login_required
def juego_detalle(id):
    origen = request.args.get('origen')
    back_url = (
        url_for('main.tienda') if origen == 'tienda' else
        url_for('main.biblioteca') if origen == 'biblioteca' else
        request.referrer or url_for('main.tienda')
    )

    cur = mysql.connection.cursor()
    # Obtener información del juego
    cur.execute("SELECT id, nombre, descripcion, precio, imagen FROM productos WHERE id = %s", (id,))
    fila = cur.fetchone()

    if not fila:
        cur.close()
        flash("Juego no encontrado", "warning")
        return redirect(back_url)

    # ✅ Verificar si el usuario ya lo tiene
    cur.execute("SELECT 1 FROM biblioteca WHERE id_usuario = %s AND id_producto = %s", (current_user.id, id))
    tiene_juego = cur.fetchone() is not None

    # Galería de imágenes
    cur.execute("SELECT nombre_imagen FROM imagenes_producto WHERE producto_id = %s", (id,))
    imagenes = [r[0] for r in cur.fetchall()]
    cur.close()

    juego = {
        'id': fila[0],
        'nombre': fila[1],
        'descripcion': fila[2],
        'precio': fila[3],
        'imagen': fila[4],
        'galeria': imagenes,
        'en_biblioteca': tiene_juego  # 👈 importante
    }
    
    if not juego['imagen']:
        juego['imagen'] = 'default.png'

    return render_template('juego_detalle.html', juego=juego, back_url=back_url)


# ======================================================
# ℹ️ ACERCA DE
# ======================================================
@main_bp.route('/acerca')
def acerca():
    return render_template('AcercaDe.html', active_page='acerca')

from flask import send_from_directory
from flask import send_from_directory

from flask import send_from_directory, abort
import urllib.parse


@main_bp.route('/descargar_imagen/<path:filename>')
@login_required
def descargar_imagen(filename):
    try:
        # Decodificar espacios y paréntesis
        filename = urllib.parse.unquote(filename)

        ruta = os.path.join('app', 'static', 'IMG')

        # Verificar si existe
        file_path = os.path.join(ruta, filename)
        if not os.path.exists(file_path):
            print(f"Archivo no encontrado: {file_path}")
            abort(404, description="Archivo no encontrado")

        return send_from_directory(ruta, filename, as_attachment=True)
    except Exception as e:
        print("Error al descargar imagen:", e)
        abort(500, description=str(e))

from flask import send_file, abort
from werkzeug.utils import safe_join
import os

from flask import send_from_directory, abort
import os

@main_bp.route('/descargar/<nombre_imagen>/<nombre_juego>')
@login_required
def descargar_juego_imagen(nombre_imagen, nombre_juego):
    try:
        carpeta = os.path.join(os.getcwd(), 'app', 'static', 'IMG', 'productos')
        ruta_archivo = os.path.join(carpeta, nombre_imagen)

        if not os.path.exists(ruta_archivo):
            abort(404, description="Archivo no encontrado")

        # Le cambiamos el nombre del archivo al descargarse
        extension = os.path.splitext(nombre_imagen)[1]
        nuevo_nombre = f"{nombre_juego}{extension}"

        return send_from_directory(
            carpeta,
            nombre_imagen,
            as_attachment=True,
            download_name=nuevo_nombre  # 👈 Aquí le das el nuevo nombre
        )

    except Exception as e:
        print("Error al descargar:", e)
        abort(500, description=f"Error al descargar: {e}")


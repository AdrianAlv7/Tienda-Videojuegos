
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app import mysql

# ✅ Cambiamos el nombre del blueprint a 'carrito'
carrito_bp = Blueprint('carrito', __name__)

# =====================================================
# 🛒 AGREGAR AL CARRITO
# =====================================================
@carrito_bp.route('/carrito/agregar', methods=['POST'])
@login_required
def carrito_agregar():
    try:
        data = request.get_json() or request.form
        id_producto = data.get('id_producto')
        cantidad = data.get('cantidad', 1)

        # Validación de datos
        if not id_producto:
            return jsonify({'ok': False, 'error': 'ID de producto faltante'}), 400

        id_producto = int(id_producto)
        cantidad = int(cantidad)

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO carrito (id_usuario, id_producto, cantidad)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE cantidad = VALUES(cantidad)
        """, (current_user.id, id_producto, cantidad))
        mysql.connection.commit()

        # Obtener nuevo total de items
        cur.execute("SELECT COALESCE(SUM(cantidad), 0) FROM carrito WHERE id_usuario = %s", (current_user.id,))
        count = cur.fetchone()[0]
        cur.close()

        return jsonify({'ok': True, 'count': count})

    except Exception as e:
        print("⚠️ Error en carrito_agregar:", e)
        return jsonify({'ok': False, 'error': str(e)}), 500



# =====================================================
# 🗑️ QUITAR DEL CARRITO
# =====================================================
@carrito_bp.route('/carrito/quitar', methods=['POST'])
@login_required
def carrito_quitar():
    data = request.get_json() or request.form
    id_producto = int(data.get('id_producto'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM carrito WHERE id_usuario = %s AND id_producto = %s", (current_user.id, id_producto))
    mysql.connection.commit()

    cur.execute("""
        SELECT COALESCE(SUM(c.cantidad * p.precio),0)
        FROM carrito c JOIN productos p ON p.id = c.id_producto
        WHERE c.id_usuario = %s
    """, (current_user.id,))
    total = float(cur.fetchone()[0])

    cur.execute("SELECT COALESCE(SUM(cantidad),0) FROM carrito WHERE id_usuario = %s", (current_user.id,))
    count = cur.fetchone()[0]
    cur.close()

    return jsonify({'ok': True, 'total': total, 'count': count})


# =====================================================
# 🔁 ACTUALIZAR CANTIDAD
# =====================================================
@carrito_bp.route('/carrito/actualizar', methods=['POST'])
@login_required
def carrito_actualizar():
    data = request.get_json() or request.form
    id_producto = int(data.get('id_producto'))
    cantidad = int(data.get('cantidad', 1))
    if cantidad < 1:
        cantidad = 1

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE carrito SET cantidad = %s
        WHERE id_usuario = %s AND id_producto = %s
    """, (cantidad, current_user.id, id_producto))
    mysql.connection.commit()

    cur.execute("SELECT precio FROM productos WHERE id = %s", (id_producto,))
    precio = float(cur.fetchone()[0]) if cur.rowcount else 0.0
    subtotal = round(precio * cantidad, 2)

    cur.execute("""
        SELECT COALESCE(SUM(c.cantidad * p.precio),0)
        FROM carrito c JOIN productos p ON p.id = c.id_producto
        WHERE c.id_usuario = %s
    """, (current_user.id,))
    total = float(cur.fetchone()[0])
    cur.close()

    return jsonify({'ok': True, 'subtotal': subtotal, 'total': total})


# =====================================================
# 👀 VER CARRITO (página dedicada)
# =====================================================
@carrito_bp.route("/carrito/ver", methods=["GET"])
@login_required
def carrito_ver():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.id, p.nombre, p.descripcion, p.precio, p.imagen, c.cantidad
        FROM carrito c
        JOIN productos p ON p.id = c.id_producto
        WHERE c.id_usuario = %s
    """, (current_user.id,))
    items = cur.fetchall()
    cur.close()

    total = sum(float(item[3]) * int(item[5]) for item in items)

    # Si viene desde AJAX, devolvemos solo el panel parcial
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render_template("partials/carrito_panel.html", items=items, total=total)

    # Si no, renderiza la página completa del carrito
    return render_template("ventas/carrito.html", items=items, total=total, active_page='carrito')





# =====================================================
# 🧹 VACIAR CARRITO
# =====================================================
@carrito_bp.route('/carrito/vaciar', methods=['POST'])
@login_required
def carrito_vaciar():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM carrito WHERE id_usuario = %s", (current_user.id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'ok': True})


# =====================================================
# 💳 CHECKOUT (pasa de carrito -> ventas, detalle_ventas y biblioteca)
# =====================================================
@carrito_bp.route('/carrito/checkout', methods=['GET', 'POST'])
@login_required
def carrito_checkout():
    cur = mysql.connection.cursor()

    # 🛍️ Obtener los productos del carrito
    cur.execute("""
        SELECT p.id, p.precio, c.cantidad
        FROM carrito c 
        JOIN productos p ON p.id = c.id_producto
        WHERE c.id_usuario = %s
    """, (current_user.id,))
    rows = cur.fetchall()

    if not rows:
        cur.close()
        return render_template("ventas/compra_exito.html", total=0, cantidad=0)

    total = sum(float(r[1]) * int(r[2]) for r in rows)
    cantidad = len(rows)

    cur.execute("INSERT INTO ventas (id_usuario, total) VALUES (%s, %s)", (current_user.id, total))
    venta_id = cur.lastrowid

    for (id_producto, precio, cantidad_item) in rows:
        cur.execute("""
            INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """, (venta_id, id_producto, cantidad_item, precio, float(precio) * int(cantidad_item)))

        cur.execute("""
            INSERT IGNORE INTO biblioteca (id_usuario, id_producto)
            VALUES (%s, %s)
        """, (current_user.id, id_producto))

    cur.execute("DELETE FROM carrito WHERE id_usuario = %s", (current_user.id,))
    mysql.connection.commit()
    cur.close()

    return render_template("ventas/compra_exito.html", total=total, cantidad=cantidad)




# =====================================================
# 🧮 CONTEO DE ITEMS EN EL CARRITO
# =====================================================
@carrito_bp.route("/carrito/conteo")
@login_required
def carrito_conteo():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM carrito WHERE id_usuario = %s", (current_user.id,))
    count = cur.fetchone()[0]
    cur.close()
    return jsonify({'count': count})




@carrito_bp.route("/carrito/eliminar", methods=["POST"])
@login_required
def carrito_eliminar():
    data = request.get_json()
    id_producto = data.get("id_producto")

    if not id_producto:
        return jsonify({"ok": False, "msg": "Producto no especificado"}), 400

    cur = mysql.connection.cursor()
    cur.execute("""
        DELETE FROM carrito
        WHERE id_usuario = %s AND id_producto = %s
    """, (current_user.id, id_producto))
    mysql.connection.commit()
    cur.close()

    # Calcular nuevo conteo
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM carrito WHERE id_usuario = %s", (current_user.id,))
    count = cur.fetchone()[0]
    cur.close()

    return jsonify({"ok": True, "count": count})


@carrito_bp.route('/carrito/compra_exitosa')
@login_required
def compra_exitosa():
    return render_template("ventas/compra_exito.html")

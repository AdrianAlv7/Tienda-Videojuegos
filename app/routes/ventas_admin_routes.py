# app/routes/ventas_admin_routes.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.utils.decorators import roles_required
from app import mysql

ventas_admin_bp = Blueprint('ventas_admin', __name__)

# =====================================================
# 👤 HISTORIAL DE COMPRAS PERSONALES (USUARIO NORMAL)
# =====================================================
@ventas_admin_bp.route('/mis_compras')
@login_required
def mis_compras():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT 
            v.id,
            v.fecha,
            v.total,
            GROUP_CONCAT(CONCAT(p.nombre, ' (', dv.cantidad, ')') SEPARATOR ', ') AS productos
        FROM ventas v
        JOIN detalle_ventas dv ON v.id = dv.venta_id
        JOIN productos p ON p.id = dv.producto_id
        WHERE v.id_usuario = %s
        GROUP BY v.id
        ORDER BY v.fecha DESC;
    """, (current_user.id,))
    ventas = cur.fetchall()
    cur.close()
    return render_template('ventas/mis_compras.html', ventas=ventas, active_page='mis_compras')



# =====================================================
# 🧾 LISTA DE TODAS LAS VENTAS (ADMIN / EDITOR)
# =====================================================
@ventas_admin_bp.route('/ventas', methods=['GET'])
@login_required
@roles_required(['admin', 'editor'])
def lista_ventas():
    cur = mysql.connection.cursor()
    cur.execute("""
    SELECT 
        v.id, 
        v.fecha, 
        v.total, 
        u.username,
        GROUP_CONCAT(CONCAT(p.nombre, ' (', dv.cantidad, ')') SEPARATOR ', ') AS productos
    FROM ventas v
    JOIN usuarios u ON v.id_usuario = u.id  -- 👈 aquí el cambio
    JOIN detalle_ventas dv ON dv.venta_id = v.id
    JOIN productos p ON p.id = dv.producto_id
    GROUP BY v.id
    ORDER BY v.fecha DESC;
""")

    ventas = cur.fetchall()
    cur.close()

    return render_template('ventas/lista.html', ventas=ventas)


# =====================================================
# 📊 HISTORIAL AGRUPADO POR PRODUCTO (ADMIN / EDITOR)
# =====================================================
@ventas_admin_bp.route('/historial', methods=['GET'])
@login_required
@roles_required(['admin', 'editor'])
def historial_ventas():
    cur = mysql.connection.cursor()
    cur.execute("""
    SELECT 
        v.id, 
        v.fecha, 
        v.total, 
        u.username,
        GROUP_CONCAT(CONCAT(p.nombre, ' (', dv.cantidad, ')') SEPARATOR ', ') AS productos
    FROM ventas v
    JOIN usuarios u ON v.id_usuario = u.id  -- 👈 aquí el cambio
    JOIN detalle_ventas dv ON dv.venta_id = v.id
    JOIN productos p ON p.id = dv.producto_id
    GROUP BY v.id
    ORDER BY v.fecha DESC;
""")

    resumen = cur.fetchall()
    cur.close()

    return render_template('ventas/historial.html', ventas=resumen)


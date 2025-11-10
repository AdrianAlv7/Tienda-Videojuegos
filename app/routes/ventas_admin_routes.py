from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.utils.decorators import roles_required
from app import mysql

ventas_admin_bp = Blueprint('ventas_admin', __name__)

@ventas_admin_bp.route('/ventas', methods=['GET'])
@login_required
@roles_required(['admin', 'editor'])
def lista_ventas():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT v.id, v.fecha, v.total, u.username,
               GROUP_CONCAT(CONCAT(p.nombre, ' (', dv.cantidad, ')') SEPARATOR ', ') AS productos
        FROM ventas v
        JOIN usuarios u ON v.usuario_id = u.id
        JOIN detalle_ventas dv ON dv.venta_id = v.id
        JOIN productos p ON p.id = dv.producto_id
        GROUP BY v.id
        ORDER BY v.fecha DESC
    """)
    ventas = cur.fetchall()
    cur.close()
    return render_template('ventas/lista.html', ventas=ventas)

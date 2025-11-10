from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app import mysql
from flask import session, url_for

ventas_bp = Blueprint('ventas', __name__)
ventas_admin_bp = Blueprint('ventas_admin', __name__)


@ventas_bp.route('/comprar', methods=['POST'])
@login_required
def comprar():
    data = request.get_json()
    carrito = data.get('carrito', [])
    total = data.get('total', 0.0)
    usuario_id = current_user.id  # O ajústalo según tu modelo de usuario

    if not carrito or float(total) <= 0:
        return jsonify({'success': False, 'error': 'Carrito vacío o total inválido'}), 400

    try:

        cur = mysql.connection.cursor()
        # 1. Insertar venta
        cur.execute('INSERT INTO ventas (usuario_id, total) VALUES (%s, %s)', (usuario_id, total))
        venta_id = cur.lastrowid

        # 2. Insertar detalles y actualizar stock
        for item in carrito:
            nombre_producto = item['producto']
            cantidad = int(item['cantidad'])
            # Buscar producto y precio en BD (¡importante para evitar fraudes!)
            cur.execute('SELECT id, stock, precio FROM productos WHERE nombre = %s', (nombre_producto,))
            prod = cur.fetchone()
            if not prod:
                raise Exception(f"Producto no encontrado: {nombre_producto}")
            producto_id, stock_actual, precio = prod
            if cantidad > stock_actual:
                raise Exception(f"Stock insuficiente para {nombre_producto}")

            # Calcular subtotal
            subtotal = cantidad * precio

            # Registrar detalle con subtotal
            cur.execute(
                'INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal) VALUES (%s, %s, %s, %s, %s)',
                (venta_id, producto_id, cantidad, precio, subtotal)
            )
            # Actualizar stock
            cur.execute('UPDATE productos SET stock = stock - %s WHERE id = %s', (cantidad, producto_id))

        mysql.connection.commit()
        session['last_venta_id'] = venta_id
        return jsonify({'success': True, 'redirect_url': url_for('main.pago')})
        cur.close()
        return jsonify({'success': True})
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@ventas_bp.route('/mis_compras')
@login_required
def mis_compras():
    cur = mysql.connection.cursor()
    # Consulta ventas de este usuario
    cur.execute("""
        SELECT v.id, v.fecha, v.total
        FROM ventas v
        WHERE v.usuario_id = %s
        ORDER BY v.fecha DESC
    """, (current_user.id,))
    ventas = cur.fetchall()

    

    # Para cada venta, consulta sus detalles
    compras = []
    for v in ventas:
        venta_id, fecha, total = v
        cur.execute("""
            SELECT p.nombre, d.cantidad, d.precio_unitario
            FROM detalle_ventas d
            JOIN productos p ON d.producto_id = p.id
            WHERE d.venta_id = %s
        """, (venta_id,))
        detalles = cur.fetchall()
        compras.append({
            'id': venta_id,
            'fecha': fecha,
            'total': total,
            'detalles': detalles
        })
    cur.close()
    return render_template('ventas/mis_compras.html', compras=compras)

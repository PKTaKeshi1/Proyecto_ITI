from datetime import datetime
from database.conexion import create_connection

class VentaModel:

    def obtener_venta_por_id(self, id_venta):
        conn = create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT 
                v.id_venta, 
                CONCAT(c.nombres, ' ', c.apellidos) AS cliente,
                CONCAT(ve.nombre_vendedor, ' ', ve.apellido_vendedor) AS vendedor,
                m.simbolo,
                v.total,
                v.fecha_venta,
                CONCAT(u.nombres, ' ', u.apellidos) AS usuario,
                v.id_cliente,
                v.id_moneda
            FROM trs_venta v
            JOIN mae_cliente c ON v.id_cliente = c.id_cliente
            JOIN mae_vendedor ve ON v.id_vendedor = ve.id_vendedor
            JOIN mae_moneda m ON v.id_moneda = m.id_moneda
            JOIN mae_usuario u ON v.id_usuario = u.id_usuario
            WHERE v.id_venta = %s
        """, (id_venta,))
            return cursor.fetchone()
        finally:
            conn.close()


    def listar_ventas(self):
        conn = create_connection()
        if conn is None:
            raise Exception("Error al conectar a la base de datos.")
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    v.id_venta, 
                    CONCAT(c.nombres, ' ', c.apellidos) AS cliente,
                    CONCAT(vend.nombre_vendedor, ' ', vend.apellido_vendedor) AS vendedor,
                    m.simbolo,
                    v.total,
                    v.fecha_venta,
                    CONCAT(u.nombres, ' ', u.apellidos) AS usuario
                FROM trs_venta v
                JOIN mae_cliente c ON v.id_cliente = c.id_cliente
                JOIN mae_vendedor vend ON v.id_vendedor = vend.id_vendedor
                JOIN mae_moneda m ON v.id_moneda = m.id_moneda
                JOIN mae_usuario u ON v.id_usuario = u.id_usuario
                WHERE v.estado = 1
                ORDER BY v.id_venta DESC
            """)
            return cursor.fetchall()
        finally:
            conn.close()

    def obtener_detalle_venta(self, id_venta):
        conn = create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    p.nombre,                    -- 0
                    d.cantidad,                 -- 1
                    d.precio_unitario,          -- 2
                    d.subtotal                  -- 3
                FROM trs_detalle_venta d
                JOIN mae_producto p ON d.id_producto = p.id_producto
                WHERE d.id_venta = %s
            """, (id_venta,))
            filas = cursor.fetchall()

            # Convertimos correctamente a tipos numéricos
            detalle = []
            for fila in filas:
                nombre = fila[0]
                cantidad = int(fila[1])
                precio_unitario = float(fila[2])
                subtotal = float(fila[3])
                detalle.append((nombre, cantidad, precio_unitario, subtotal))
            return detalle
        finally:
            conn.close()

    def obtener_moneda_por_id(self, id_moneda):
        conn = create_connection()
        if conn is None:
            raise Exception("Error al conectar a la base de datos.")
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT simbolo, cambio_actual FROM mae_moneda WHERE id_moneda = %s", (id_moneda,))
            return cursor.fetchone()
        finally:
            conn.close()

    def registrar_venta(self, id_cliente, id_vendedor, id_usuario, detalles, id_moneda):
        conn = create_connection()
        if conn is None:
            raise Exception("No se pudo conectar a la base de datos.")
        try:
            cursor = conn.cursor()
            total = 0

            for detalle in detalles:
                cantidad = int(detalle['cantidad'])
                precio_unitario = float(detalle['precio_unitario'])
                subtotal = cantidad * precio_unitario
                detalle['subtotal'] = subtotal
                total += subtotal

            fecha_venta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
                INSERT INTO trs_venta (id_vendedor, id_cliente, id_usuario, id_moneda, fecha_venta, total, estado)
                VALUES (%s, %s, %s, %s, %s, %s, 1)
            """, (id_vendedor, id_cliente, id_usuario, id_moneda, fecha_venta, total))
            conn.commit()
            id_venta = cursor.lastrowid

            for detalle in detalles:
                cursor.execute("""
                    INSERT INTO trs_detalle_venta (id_venta, id_producto, cantidad, precio_unitario, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    id_venta,
                    int(detalle['id_producto']),
                    int(detalle['cantidad']),
                    float(detalle['precio_unitario']),
                    float(detalle['subtotal'])
                ))

                cursor.execute("""
                    UPDATE mae_producto 
                    SET stock = stock - %s 
                    WHERE id_producto = %s AND stock >= %s
                """, (
                    int(detalle['cantidad']),
                    int(detalle['id_producto']),
                    int(detalle['cantidad'])
                ))

                if cursor.rowcount == 0:
                    raise Exception(f"No hay suficiente stock para el producto ID {detalle['id_producto']}.")

            moneda = self.obtener_moneda_por_id(id_moneda)
            conn.commit()

            return {
                "id_venta": id_venta,
                "total": total,
                "simbolo_moneda": moneda[0] if moneda else '',
                "cambio": moneda[1] if moneda else 1.0
            }

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al registrar venta: {str(e)}")
        finally:
            conn.close()

    

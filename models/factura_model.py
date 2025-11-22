from database.conexion import create_connection
from datetime import datetime

class FacturaModel:
    def obtener_cliente_de_factura(self, id_factura):
        conn = create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.id_cliente, CONCAT(c.nombres, ' ', c.apellidos) AS nombre_completo
                FROM trs_factura f
                JOIN trs_venta v ON f.id_venta = v.id_venta
                JOIN mae_cliente c ON v.id_cliente = c.id_cliente
                WHERE f.id_factura = %s
            """, (id_factura,))
            return cursor.fetchone()
        finally:
            conn.close()

    def obtener_factura_por_id(self, id_factura):
        conn = create_connection()
        try:
            cursor = conn.cursor()
            
            # Obtener datos principales de la factura
            cursor.execute("""
                SELECT 
                    f.id_factura, f.serie, f.numero, f.monto_total,
                    f.tipo_comprobante, m.simbolo, u.usuario,
                    v.id_venta, v.id_cliente, f.subtotal, f.igv,
                    f.fecha_emision, m.nombre_moneda
                FROM trs_factura f
                JOIN trs_venta v ON f.id_venta = v.id_venta
                JOIN mae_usuario u ON f.id_usuario = u.id_usuario
                JOIN mae_moneda m ON f.id_moneda = m.id_moneda
                WHERE f.id_factura = %s
            """, (id_factura,))
            row = cursor.fetchone()
            if not row:
                return None

            # Obtener nombre y RUC del cliente
            cursor.execute("""
                SELECT CONCAT(nombres, ' ', apellidos), dni_ruc
                FROM mae_cliente
                WHERE id_cliente = %s
            """, (row[8],))
            cliente = cursor.fetchone()
            cliente_nombre = cliente[0] if cliente else 'Cliente desconocido'
            cliente_ruc = cliente[1] if cliente else '-'

            return (
                row[0],        # id_factura
                row[1],        # serie
                row[2],        # numero
                row[11],       # fecha_emision
                float(row[9]), # subtotal
                float(row[10]),# igv
                float(row[3]), # total
                row[7],        # id_venta
                row[5],        # símbolo de moneda
                0.00,          # monto pagado (opcional, no usado aquí)
                cliente_nombre,
                cliente_ruc,
                row[12],       # nombre moneda
                row[8],  # id_cliente
                '--------'     # monto en letras, puede ser generado si usas un generador
            )
        finally:
            conn.close()


    def listar_facturas(self):
        conn = create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    f.id_factura,
                    f.serie,
                    f.numero,
                    f.fecha_emision,
                    f.subtotal,
                    f.igv,
                    f.monto_total,
                    f.tipo_comprobante,
                    m.simbolo,
                    IFNULL((
                        SELECT SUM(c.monto_pago)
                        FROM trs_cobranza c
                        WHERE c.id_factura = f.id_factura AND c.estado = 1
                    ), 0) AS monto_pagado
                FROM trs_factura f
                JOIN mae_moneda m ON f.id_moneda = m.id_moneda
                ORDER BY f.id_factura DESC
            """)
            return cursor.fetchall()
        finally:
            conn.close()


    def emitir_factura(self, id_venta, id_usuario, id_moneda, tipo_comprobante, serie, numero):
        conn = create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT total FROM trs_venta WHERE id_venta = %s", (id_venta,))
            venta = cursor.fetchone()
            if not venta:
                raise Exception("La venta no existe.")

            total = float(venta[0])
            subtotal = round(total / 1.18, 2)
            igv = round(total - subtotal, 2)
            fecha_emision = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
                INSERT INTO trs_factura (
                    id_venta, id_usuario, id_moneda, tipo_comprobante,
                    serie, numero, fecha_emision, monto_total, subtotal, igv, estado
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
            """, (id_venta, id_usuario, id_moneda, tipo_comprobante, serie, numero,
                   fecha_emision, total, subtotal, igv))

            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise Exception("Error al emitir factura: " + str(e))
        finally:
            conn.close()

    def existe_factura_para_venta(self, id_venta):
        conn = create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM trs_factura WHERE id_venta = %s AND estado = 1", (id_venta,))
            return cursor.fetchone() is not None
        finally:
            conn.close()

    def existe_factura_por_serie_numero(self, serie, numero):
        conn = create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 1 FROM trs_factura
                WHERE serie = %s AND numero = %s AND estado = 1
            """, (serie, numero))
            return cursor.fetchone() is not None
        finally:
            conn.close()

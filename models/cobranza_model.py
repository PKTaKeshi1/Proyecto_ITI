from database.conexion import create_connection

class CobranzaModel:

    def obtener_total_pagado(self, id_factura):
        conn = create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COALESCE(SUM(monto_pago), 0)
                FROM trs_cobranza
                WHERE id_factura = %s AND estado = 1
            """, (id_factura,))
            resultado = cursor.fetchone()
            return float(resultado[0]) if resultado else 0.0
        finally:
            conn.close()
    
    def registrar_cobranza(self, id_factura, id_cliente, monto_pago, fecha_pago, id_usuario):
        conn = create_connection()
        try:
            cursor = conn.cursor()

            # 1. Obtener el total de la factura
            cursor.execute("SELECT monto_total FROM trs_factura WHERE id_factura = %s", (id_factura,))
            factura = cursor.fetchone()
            if not factura:
                raise Exception("La factura no existe.")

            total_factura = float(factura[0])

            # 2. Obtener monto ya pagado
            cursor.execute("""
                SELECT IFNULL(SUM(monto_pago), 0) 
                FROM trs_cobranza 
                WHERE id_factura = %s AND estado = 1
            """, (id_factura,))
            monto_pagado_actual = float(cursor.fetchone()[0])

            # 3. Calcular cuánto falta
            monto_restante = round(total_factura - monto_pagado_actual, 2)

            if monto_pago > monto_restante:
                raise Exception(f"El monto ingresado ({monto_pago}) excede el saldo pendiente ({monto_restante}).")

            # 4. Registrar cobranza si todo está OK (ahora incluyendo id_cliente)
            cursor.execute("""
                INSERT INTO trs_cobranza (id_factura, id_cliente, monto_pago, fecha_pago, id_usuario, estado)
                VALUES (%s, %s, %s, %s, %s, 1)
            """, (id_factura, id_cliente, monto_pago, fecha_pago, id_usuario))

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al registrar la cobranza: {str(e)}")
        finally:
            conn.close()



    def listar_cobranzas(self):
        conn = create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    c.id_cobranza,
                    f.serie,
                    f.numero,
                    CONCAT(cl.nombres, ' ', cl.apellidos) AS cliente,
                    c.fecha_pago,
                    c.monto_pago,
                    u.usuario,
                    c.estado
                FROM trs_cobranza c
                JOIN trs_factura f ON c.id_factura = f.id_factura
                JOIN trs_venta v ON f.id_venta = v.id_venta
                JOIN mae_cliente cl ON v.id_cliente = cl.id_cliente
                JOIN mae_usuario u ON c.id_usuario = u.id_usuario
                ORDER BY c.id_cobranza DESC
            """)
            return cursor.fetchall()
        except Exception as e:
            raise Exception("Error al listar las cobranzas: " + str(e))
        finally:
            conn.close()


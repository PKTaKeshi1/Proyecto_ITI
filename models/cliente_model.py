from database.conexion import create_connection

class ClienteModel:

    @staticmethod
    def listar_clientes():
        connect = create_connection()
        try:
            cursor = connect.cursor()
            cursor.execute("""
                SELECT 
                    id_cliente, nombres, apellidos, razon_social, tipo_doc, dni_ruc,
                    direccion, telefono, email
                FROM mae_cliente
                WHERE estado = 1
            """)
            return cursor.fetchall()
        finally:
            connect.close()

    @staticmethod
    def listar_clientes_activos():
        connect = create_connection()
        try:
            cursor = connect.cursor()
            cursor.execute("""
                SELECT id_cliente, CONCAT(nombres, ' ', apellidos) AS nombre_completo
                FROM mae_cliente
                WHERE estado = 1
            """)
            return cursor.fetchall()
        finally:
            connect.close()

    @staticmethod
    def insertar_cliente(nombres, apellidos, razon_social, tipo_doc, dni_ruc, direccion, telefono, email, id_usuario):
        conexion = create_connection()
        try:
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO mae_cliente (
                    id_usuario, nombres, apellidos, razon_social,
                    tipo_doc, dni_ruc, direccion, telefono, email, estado
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
            """, (id_usuario, nombres, apellidos, razon_social, tipo_doc, dni_ruc, direccion, telefono, email))
            conexion.commit()
        finally:
            conexion.close()

    @staticmethod
    def obtener_cliente_por_id(id_cliente):
        conexion = create_connection()
        try:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT id_cliente, nombres, apellidos, razon_social, tipo_doc, dni_ruc, direccion, telefono, email
                FROM mae_cliente
                WHERE id_cliente = %s
            """, (id_cliente,))
            return cursor.fetchone()
        finally:
            conexion.close()

    @staticmethod
    def actualizar_cliente(id_cliente, nombres, apellidos, razon_social, tipo_doc, dni_ruc, direccion, telefono, email):
        conexion = create_connection()
        try:
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE mae_cliente
                SET nombres = %s, apellidos = %s, razon_social = %s,
                    tipo_doc = %s, dni_ruc = %s, direccion = %s, telefono = %s, email = %s
                WHERE id_cliente = %s
            """, (nombres, apellidos, razon_social, tipo_doc, dni_ruc, direccion, telefono, email, id_cliente))
            conexion.commit()
        finally:
            conexion.close()

    @staticmethod
    def eliminar_cliente(id_cliente):
        conexion = create_connection()
        try:
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE mae_cliente SET estado = 0 WHERE id_cliente = %s
            """, (id_cliente,))
            conexion.commit()
        finally:
            conexion.close()

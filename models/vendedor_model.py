from database.conexion import create_connection

class VendedorModel:

    @staticmethod
    def listar_vendedores():
        conexion = create_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id_vendedor, nombre_vendedor, apellido_vendedor, celular, correo 
            FROM mae_vendedor
            WHERE estado = 1
        """)
        vendedores = cursor.fetchall()
        conexion.close()
        return vendedores

    @staticmethod
    def listar_vendedores_activos():
        conexion = create_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id_vendedor, CONCAT(nombre_vendedor, ' ', apellido_vendedor) AS nombre_completo
            FROM mae_vendedor
            WHERE estado = 1
        """)
        vendedores = cursor.fetchall()
        conexion.close()
        return vendedores

    @staticmethod
    def insertar_vendedor(nombre, apellido, celular, correo, id_usuario):
        conexion = create_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO mae_vendedor (
                id_usuario, nombre_vendedor, apellido_vendedor, celular, correo, estado
            ) VALUES (%s, %s, %s, %s, %s, 1)
        """, (id_usuario, nombre, apellido, celular, correo))
        conexion.commit()
        conexion.close()

    @staticmethod
    def obtener_por_id(id_vendedor):
        conexion = create_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id_vendedor, nombre_vendedor, apellido_vendedor, celular, correo 
            FROM mae_vendedor 
            WHERE id_vendedor = %s
        """, (id_vendedor,))
        vendedor = cursor.fetchone()
        conexion.close()
        return vendedor

    @staticmethod
    def actualizar_vendedor(id_vendedor, nombre, apellido, celular, correo):
        conexion = create_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE mae_vendedor
            SET nombre_vendedor = %s, apellido_vendedor = %s, celular = %s, correo = %s
            WHERE id_vendedor = %s
        """, (nombre, apellido, celular, correo, id_vendedor))
        conexion.commit()
        conexion.close()

    @staticmethod
    def eliminar_vendedor(id_vendedor):
        conexion = create_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE mae_vendedor SET estado = 0 WHERE id_vendedor = %s
        """, (id_vendedor,))
        conexion.commit()
        conexion.close()

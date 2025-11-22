from database.conexion import create_connection

class ProductoModel:

    @staticmethod
    def listar_productos():
        connect = create_connection()
        try:
            cursor = connect.cursor()
            cursor.execute("""
                SELECT id_producto, nombre, descripcion, precio_unitario, stock 
                FROM mae_producto 
                WHERE estado = 1
            """)
            productos = cursor.fetchall()
            return productos
        finally:
            connect.close()

    @staticmethod
    def listar_productos_activos():
        connect = create_connection()
        try:
            cursor = connect.cursor()
            cursor.execute("""
                SELECT id_producto, nombre, descripcion, precio_unitario, stock
                FROM mae_producto
                WHERE estado = 1
            """)
            return cursor.fetchall()
        finally:
            connect.close()


    @staticmethod
    def insertar_producto(nombre, descripcion, precio_unitario, stock, id_usuario):
        connect = create_connection()
        try:
            cursor = connect.cursor()
            cursor.execute("""
                INSERT INTO mae_producto (nombre, descripcion, precio_unitario, stock, id_usuario, estado)
                VALUES (%s, %s, %s, %s, %s, 1)
            """, (nombre, descripcion, float(precio_unitario), int(stock), int(id_usuario)))
            connect.commit()
        finally:
            connect.close()

    @staticmethod
    def obtener_producto_por_id(id_producto):
        connect = create_connection()
        try:
            cursor = connect.cursor()
            cursor.execute("""
                SELECT id_producto, nombre, descripcion, precio_unitario, stock 
                FROM mae_producto 
                WHERE id_producto = %s
            """, (id_producto,))
            return cursor.fetchone()
        finally:
            connect.close()

    @staticmethod
    def actualizar_producto(id_producto, nombre, descripcion, precio_unitario, stock):
        connect = create_connection()
        try:
            cursor = connect.cursor()
            cursor.execute("""
                UPDATE mae_producto 
                SET nombre = %s, descripcion = %s, precio_unitario = %s, stock = %s
                WHERE id_producto = %s
            """, (nombre, descripcion, float(precio_unitario), int(stock), id_producto))
            connect.commit()
        finally:
            connect.close()

    @staticmethod
    def eliminar_producto(id_producto):
        connect = create_connection()
        try:
            cursor = connect.cursor()
            cursor.execute("""
                UPDATE mae_producto SET estado = 0 WHERE id_producto = %s
            """, (id_producto,))
            connect.commit()
        finally:
            connect.close()

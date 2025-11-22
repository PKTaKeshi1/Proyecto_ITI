from database.conexion import create_connection

class MonedaModel:

    @staticmethod
    def listar_monedas():
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_moneda, nombre_moneda, simbolo, cambio_actual, fecha_actualizacion, subunidad FROM mae_moneda")
        resultados = cursor.fetchall()
        conn.close()
        return resultados

    @staticmethod
    def listar_monedas_activas():
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_moneda, nombre_moneda, simbolo FROM mae_moneda")
        resultados = cursor.fetchall()
        conn.close()
        return resultados

    @staticmethod
    def crear_moneda(id_moneda, nombre, simbolo, cambio, fecha, subunidad):
        conn = create_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO mae_moneda (
                id_moneda, nombre_moneda, simbolo, cambio_actual, 
                fecha_actualizacion, subunidad
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (id_moneda, nombre, simbolo, cambio, fecha, subunidad))
        conn.commit()
        conn.close()

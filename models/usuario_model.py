from database.conexion import create_connection
from exceptions.mis_excepciones import (
    ConexionBDException, ErrorInsercionException,
    ErrorConsultaException, ErrorActualizacionException,
    ErrorEliminacionException
)

class UsuarioModel:
    def crear_usuario(self, nombres, apellidos, usuario, contraseña, usuario_creacion):
        conexion = create_connection()
        if not conexion:
            raise ConexionBDException("Error al conectar con la base de datos.")
        try:
            cursor = conexion.cursor()
            sql = """
                INSERT INTO mae_usuario (
                    nombres, apellidos, usuario, contraseña, estado, 
                    fecha_creacion, usuario_creacion
                ) VALUES (%s, %s, %s, %s, 1, NOW(), %s)
            """
            datos = (nombres, apellidos, usuario, contraseña, usuario_creacion)
            cursor.execute(sql, datos)
            conexion.commit()
        except Exception as e:
            raise ErrorInsercionException(f"Error al insertar usuario: {e}")
        finally:
            conexion.close()

    def listar_usuarios(self):
        conexion = create_connection()
        if not conexion:
            raise ConexionBDException("Error al conectar con la base de datos.")
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM mae_usuario")
            return cursor.fetchall()
        except Exception as e:
            raise ErrorConsultaException(f"Error al listar usuarios: {e}")
        finally:
            conexion.close()

    def actualizar_usuario(self, id_usuario, nombres, apellidos, usuario_modificacion):
        conexion = create_connection()
        if not conexion:
            raise ConexionBDException("Error al conectar con la base de datos.")
        try:
            cursor = conexion.cursor()
            sql = """
                UPDATE mae_usuario 
                SET nombres = %s, apellidos = %s, 
                    fecha_modificacion = NOW(), usuario_modificacion = %s 
                WHERE id_usuario = %s
            """
            datos = (nombres, apellidos, usuario_modificacion, id_usuario)
            cursor.execute(sql, datos)
            conexion.commit()
        except Exception as e:
            raise ErrorActualizacionException(f"Error al actualizar usuario: {e}")
        finally:
            conexion.close()

    def eliminar_usuario(self, id_usuario):
        conexion = create_connection()
        if not conexion:
            raise ConexionBDException("Error al conectar con la base de datos.")
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM mae_usuario WHERE id_usuario = %s"
            cursor.execute(sql, (id_usuario,))
            conexion.commit()
        except Exception as e:
            raise ErrorEliminacionException(f"Error al eliminar usuario: {e}")
        finally:
            conexion.close()

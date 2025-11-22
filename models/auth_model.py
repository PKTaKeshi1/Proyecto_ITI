from database.conexion import create_connection
from exceptions.autenticacion_excepcion import AutenticacionException
from werkzeug.security import check_password_hash

class AuthModel:
    def validar_usuario(self, usuario, contraseña):
        if len(usuario) < 5:
            raise AutenticacionException("El nombre de usuario debe tener al menos 5 caracteres")

        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM mae_usuario WHERE usuario = %s AND estado = 1"
        cursor.execute(sql, (usuario,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            if check_password_hash(resultado['contraseña'], contraseña):
                return resultado
            else:
                raise AutenticacionException("Contraseña incorrecta")
        else:
            raise AutenticacionException("Usuario no encontrado o inactivo")

from db.conexion import obtener_conexion

class ClienteModel:

    @staticmethod
    def guardar(documento, nombre, telefonos):
        conn = obtener_conexion()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO clientes (documento, nombre, telefonos)
            VALUES (%s, %s, %s)
            ON CONFLICT (documento)
            DO UPDATE SET nombre=%s, telefonos=%s
        """, (documento, nombre, telefonos, nombre, telefonos))

        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def eliminar(documento):
        conn = obtener_conexion()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM clientes WHERE documento = %s",
            (documento,)
        )

        conn.commit()
        cur.close()
        conn.close()

import sqlite3 as sl
def Abrir_bd():
    base = sl.connect("Base_datos.db")
    bd = base.cursor()
    bd.execute("PRAGMA foreign_keys=on")
    return base, bd

def Crear_tablas():
    base, bd = Abrir_bd()
    bd.execute("CREATE TABLE user ("
               "usuario VARCHAR(20),"
               "email VARCHAR(20),"
               "nombre VARCHAR(20),"
               "apellido VARCHAR(20),"
               "telefono INT(9), "
               "contraseña VARCHAR(30),"
               "salt BIT(16),"
               "PRIMARY KEY(usuario))")

    bd.execute( "CREATE TABLE restaurante ("
                "localizacion VARCHAR(20),"
                "telefono INT(9),"
                "valoracion INT(1),"
                "horario_apertura INT(2),"
                "horario_cerrar INT(2),"
                "aforo INT(3),"
                "PRIMARY KEY(localizacion))")

    bd.execute("CREATE TABLE reservas("
               "usuario VARCHAR(20),"
               "localizacion VARCHAR(20),"
               "hora int(2),"
               "fecha date,"
               "personas int(2),"
               "PRIMARY KEY(usuario, hora, fecha),"
               "FOREIGN KEY(usuario) REFERENCES user(usuario),"
               "FOREIGN KEY(localizacion) REFERENCES restaurante (localizacion))")

    bd.execute("CREATE TABLE aforo("
               "localizacion VARCHAR(20),"
               "fecha date, "
               "hora int(2),"
               "ocupacion int(3),"
               "PRIMARY KEY(localizacion, fecha, hora),"
               "FOREIGN KEY(localizacion) REFERENCES restaurante (localizacion))")
    base.close()

def borrar_tablas():
    base, bd = Abrir_bd()
    bd.execute("DROP TABLE aforo")
    bd.execute("DROP TABLE reservas")
    bd.execute("DROP TABLE user")
    bd.execute("DROP TABLE restaurante")


    base.close()



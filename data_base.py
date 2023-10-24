import sqlite3 as sl


#Archivo con los métodos de creación de las bases de datos

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
               "salt_contr VARCHAR(50),"
               "salt_clave VARCHAR(50),"
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
               "non_hora VARCHAR(20),"
               "fecha date,"
               "non_fecha VARCHAR(20),"
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

def insertar_restaurantes():
    base, bd = Abrir_bd()
    bd.execute("""INSERT INTO restaurante VALUES("Madrid, Calle Mayor, 5", 346898789, 3.5, 10,24 , 30)""")
    bd.execute("""INSERT INTO restaurante VALUES("Leganes, Calle Sabatini, 10", 276598961, 4, 10,12, 30)""")
    base.commit()
    base.close()



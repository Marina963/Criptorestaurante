import sqlite3 as sl


base = sl.connect("Base_datos.db")

bd = base.cursor()
bd.execute("PRAGMA foreign_keys=on")

#bd.execute("DROP TABLE user")
#bd.execute("DROP TABLE restaurante")
#bd.execute("DROP TABLE reservas")
'''
bd.execute("CREATE TABLE user (usuario, email, nombre, apellido, telefono, contraseña,"
           "PRIMARY KEY (usuario) )")
bd.execute("CREATE TABLE restaurante (localizacion, telefono, valoracion, horario, aforo,"
           "PRIMARY KEY (localizacion))")
bd.execute("CREATE TABLE reservas (usuarios, localizacions, hora,  dia, personas,"
           "FOREIGN KEY (usuarios) REFERENCES user (usuario),"
           "FOREIGN KEY (localizacions) REFERENCES restaurante (localizacion))")
'''
#bd.execute("""INSERT INTO user VALUES("Marina_9", "ddfr@gmail.com","Marina", "Perez",6102914517, 1234 )""")

bd.execute("""INSERT INTO restaurante VALUES("Madrid, Calle Mayor, 5", "346898789", "3,5", "10:00 - 12:00", "30")""")
bd.execute("""INSERT INTO restaurante VALUES("Leganes, Calle Sabatini, 10", "276598961", "4", "10:00 - 12:00", "30")""")

#bd.execute(""" INSERT INTO reservas VALUES("Marina_9","grinon", '12:00', '12/09/23', 2)""")
#bd.execute(""" INSERT INTO reservas VALUES("Marina","griñon", '12:00', '12/09/23', 2)""")
base.commit()

for row in bd.execute("SELECT * FROM user"):
    print(row)

for row in bd.execute("SELECT * FROM restaurante"):
    print(row)

for row in bd.execute("SELECT * FROM reservas"):
    print(row)

base.close()

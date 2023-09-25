import pick
import sqlite3 as sl
import time
import re

base = sl.connect("Base_datos.db")
bd = base.cursor()
bd.execute("PRAGMA foreign_keys=on")

registro = ['Crear cuenta', 'Iniciar sesion']
opcion, llave = pick.pick(registro, "¿Que desea hacer?: ", indicator="=>")

iniciado, create, redirige, reservado, disponible = False, False, False, False, False

if opcion == 'Crear cuenta':
    while not create:
        usuario = input('Introduce su nuevo nombre de usuario:')
        bd.execute("SELECT usuario FROM user WHERE usuario=?", (usuario,))
        usua = bd.fetchall()
        if len(usua) > 0:
            print("Usuario ya existe")
        else:
            correo = input('Introduce correo electronico:')

            c = re.compile(r'^[a-z0-9]+@[a-z]+\.[a-z]{3}$').match(correo)
            # Con una expresión regular comprobamos la sintaxis del fichero.
            if c is None:
                print( "Formato de datos incorrecto")
            else:
                nombre = input('Introduce nombre:')
                apellido = input('Introduce apellido:')
                if not isinstance( nombre,str)  or not  isinstance( apellido,str) :
                    print("Nombre u apellido no valido")
                else:
                    telefono = input('Introduce telefono:')
                    numero = re.compile(r'^[0-9]{9}$').match( telefono)

                    if numero is None:
                        print("Telefono no valido")
                    else:
                        contrasena = input('Introduzca su contraseña:')
                        conf_contrasena = input('Confirme su contraseña:')
                        if contrasena == conf_contrasena:
                            bd.execute("INSERT INTO user VALUES(?,?,?,?,?,?)", (usuario, correo, nombre, apellido, int(telefono), contrasena))
                            create = True
                            base.commit()
                            for row in bd.execute("SELECT * FROM user"):
                                print(row)
                        else:
                            print("las contraseñas no coinciden")
else:
    while not iniciado:
        usuario = input('Introduzca su usuario:')
        contrasena = input('Introduce su contraseña:')
        bd.execute("SELECT contraseña FROM user WHERE usuario=?", (usuario,))
        true_cont = bd.fetchall()
        if len(true_cont) == 0:
            print("Usuario no existe")
        elif true_cont[0][0] == str(contrasena):
            print("bienvenido")
            iniciado = True
        else:
            print("Contraseña incorrecta")

if iniciado or create:
    while not redirige:
        restaurante = ['Madrid, Calle Mayor, 5', 'Leganes, Calle Sabatini, 10']
        rest_opcion, llave = pick.pick(restaurante, "¿Que restaurnate desea visitar?: ", indicator="=>")
        bd.execute("SELECT telefono, valoracion, horario_apertura, horario_cerrar FROM restaurante WHERE localizacion=?", (rest_opcion,))
        datos = bd.fetchall()
        tel, val, hor_i, hor_c = datos[0][0], datos[0][1], datos[0][2],datos[0][3]
        print(tel, val, hor_i, hor_c)
        time.sleep(5)
        reserva = ['Si', 'No']
        res_opcion, llave2 = pick.pick(reserva, "¿Desea hacer una reserva?: ", indicator="=>")

        if res_opcion == 'Si':
            redirige = True
            print("redirige pag reserva")
if redirige:
    while not reservado:
        dias = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
        meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        anyo = 2023
        horas = [10, 11, 12]
        personas = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        pers_opcion, llave5 = pick.pick(meses, "¿Para cuantas personas es la reserva?: ", indicator="=>")
        mes_opcion, llave2 = pick.pick(meses, "Seleccione un mes: ", indicator="=>")
        dia_opcion, llave = pick.pick(dias, "Seleccione un dia: ", indicator="=>")
        hora_opcion, llave4 = pick.pick(horas, "Seleccione una hora: ", indicator="=>")
        fecha = (str(anyo),  '/', str(mes_opcion), '/',str(dia_opcion))
        fecha = "".join(fecha)
        bd.execute("SELECT ocupacion FROM aforo WHERE localizacion=? and hora = ? and fecha= ?", (rest_opcion, hora_opcion, fecha))
        aforo = bd.fetchall()
        if len(aforo) == 0 :
            bd.execute("SELECT aforo FROM restaurante WHERE localizacion=?", (rest_opcion,))
            aforo_r = bd.fetchall()
            if aforo_r[0][0] < pers_opcion:
                print("Aforo completo")
            else:
                n_per = aforo_r[0][0] - pers_opcion
                bd.execute("INSERT INTO aforo VALUES(?,?,?,?)",(rest_opcion, fecha, hora_opcion, n_per))
                disponible = True

        elif aforo[0][0] <= 0:
            print("Aforo completo")
        else:
            n_per = aforo[0][0] - pers_opcion
            if n_per < 0:
                print("Aforo insuficiente")
            else:
                bd.execute(
                    "UPDATE aforo set AFORO = ? WHERE localizacion=? and hora = ? and fecha= ?", (
                n_per, rest_opcion, hora_opcion, fecha))
                disponible = True

        if disponible:
            print("La fecha seria: ", str(dia_opcion), "/", str(mes_opcion), "/", str(anyo), "a las", hora_opcion,
                  "para", pers_opcion, "personas")
            time.sleep(2)

            reserva = ['Confirmar', 'Cambiar seleccion']

            res_opcion, llave3 = pick.pick(reserva, "Confirma tu reserva: ", indicator="=>")
            if res_opcion == 'Confirmar':
                print("Reserva confirmada")
                reservado = True
                bd.execute("INSERT INTO reservas VALUES(?,?,?,?,?)", (usuario, rest_opcion, hora_opcion, fecha, pers_opcion))
                base.commit()
for row in bd.execute("SELECT * FROM reservas"):
    print(row)
base.close()

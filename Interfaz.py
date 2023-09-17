import sqlite3 as sl
import time
import re
import streamlit as st



base = sl.connect("Base_datos.db")
bd = base.cursor()
bd.execute("PRAGMA foreign_keys=on")

opcion = False
iniciado, create, redirige, reservado, disponible = False, False, False, False, False


opcion = st.sidebar.radio("¿Que desea hacer?:", ['Crear cuenta', 'Iniciar sesion', 'Reservar'] )

if opcion == 'Crear cuenta':

    usuario = st.text_input('Introduce su nuevo nombre de usuario:')
    st.write(usuario)
    bd.execute("SELECT usuario FROM user WHERE usuario=?", (usuario,))
    usua = bd.fetchall()
    if len(usua) > 0:
        st.write("Usuario ya existe")
    else:
        correo = st.text_input('Introduce correo electronico:')

        c = re.compile(r'^[a-z0-9]+@[a-z]+\.[a-z]{3}$').match(correo)

        if c is None:
            st.write( "Formato de datos incorrecto")
        else:
            nombre = st.text_input('Introduce nombre:')
            apellido = st.text_input('Introduce apellido:')
            if not isinstance( nombre,str)  or not  isinstance( apellido,str) :
                st.write("Nombre u apellido no valido")
            else:
                telefono = st.text_input('Introduce telefono:')
                numero = re.compile(r'^[0-9]{9}$').match( telefono)

                if numero is None:
                    st.write("Telefono no valido")
                else:
                    contrasena = st.text_input('Introduzca su contraseña:')
                    conf_contrasena = st.text_input('Confirme su contraseña:')
                    if contrasena == conf_contrasena:
                        bd.execute("INSERT INTO user VALUES(?,?,?,?,?,?)", (usuario, correo, nombre, apellido, int(telefono), contrasena))
                        create = True
                        base.commit()
                        for row in bd.execute("SELECT * FROM user"):
                            st.write(row)
                    else:
                        st.write("las contraseñas no coinciden")
else:

    usuari = st.text_input('Introduzca su usuario:')
    contrasena = st.text_input('Introduce su contraseña:')
    bd.execute("SELECT contraseña FROM user WHERE usuario=?", (usuari,))
    true_cont = bd.fetchall()
    if len(true_cont) == 0:
        st.write("Usuario no existe")
    elif true_cont[0][0] == str(contrasena):
        st.write("bienvenido")
        iniciado = True
    else:
        st.write("Contraseña incorrecta")

if (iniciado or create) :


    restaurante = ['Madrid, Calle Mayor, 5', 'Leganes, Calle Sabatini, 10']
    rest_opcion = st.selectbox("¿Que restaurnate desea visitar?: ", restaurante)
    #rest_opcion, llave = pick.pick(restaurante, "¿Que restaurnate desea visitar?: ", indicator="=>")
    bd.execute("SELECT telefono, valoracion, horario_apertura, horario_cerrar FROM restaurante WHERE localizacion=?", (rest_opcion,))
    datos = bd.fetchall()
    tel, val, hor_i, hor_c = datos[0][0], datos[0][1], datos[0][2],datos[0][3]
    st.write(tel, val, hor_i, hor_c)
    time.sleep(5)
    reserva = ['Si', 'No']
    #res_opcion, llave2 = pick.pick(reserva, "¿Desea hacer una reserva?: ", indicator="=>")
    res_opcion = st.selectbox("¿Desea hacer una reserva?: ", reserva)

    if res_opcion == 'Si':
        redirige = True
        st.write("redirige pag reserva")

base.close()




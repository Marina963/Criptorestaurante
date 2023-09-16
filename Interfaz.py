import sqlite3 as sl
import time
import re
import streamlit as st



base = sl.connect("Base_datos.db")
bd = base.cursor()
bd.execute("PRAGMA foreign_keys=on")
opcion = False
iniciado, create, redirige, reservado, disponible = False, False, False, False, False
while opcion == False:
    opcion = st.sidebar.radio("¿Que desea hacer?:", ['Crear cuenta', 'Iniciar sesion'] )
    o = st.button("Enter")

if opcion == 'Crear cuenta' and o == True:
    while not create:
        usuario = st.text_input('Introduce su nuevo nombre de usuario:')
        bd.execute("SELECT usuario FROM user WHERE usuario=?", (usuario,))
        usua = bd.fetchall()
        if len(usua) > 0:
            print("Usuario ya existe")
        else:
            correo =  st.text_input('Introduce correo electronico:')

            c = re.compile(r'^[a-z0-9]+@[a-z]+\.[a-z]{3}$').match(correo)
            # Con una expresión regular comprobamos la sintaxis del fichero.
            if c is None:
                print( "Formato de datos incorrecto")
            else:
                nombre =  st.text_input('Introduce nombre:')
                apellido =  st.text_input('Introduce apellido:')
                if not isinstance( nombre,str)  or not  isinstance( apellido,str) :
                    print("Nombre u apellido no valido")
                else:
                    telefono =  st.text_input('Introduce telefono:')
                    numero = re.compile(r'^[0-9]{9}$').match( telefono)

                    if numero is None:
                        print("Telefono no valido")
                    else:
                        contrasena = st.text_input('Introduzca su contraseña:')
                        conf_contrasena =  st.text_input('Confirme su contraseña:')
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




base.close()




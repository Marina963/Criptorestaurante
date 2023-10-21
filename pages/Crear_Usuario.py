import re
from  Inicio_Sesion import  *
import os

#Archivo para crear el usuario

def Crear_Usuario():
    base, bd = Abrir_bd()

    #Usuario introduce su nombre
    usuario = st.text_input('Introduce su nuevo nombre de usuario:')

    #Se busca en la base de datos para ver si ya existe en nombre de usuario que ha puesto
    bd.execute("SELECT usuario FROM user WHERE usuario=?", (usuario,))
    usua = bd.fetchall()

    if len(usua) > 0:
        st.write("Usuario ya existe")

    else:
        #Si no existe se pide que introduzca su correo electrónico
        correo = st.text_input('Introduce correo electronico:')

        #Se comprueba que la contraseña tiene el formato correcto
        c = re.compile(r'^[a-z0-9]+@[a-z]+\.[a-z]{3}$').match(correo)

        if c is None:
            st.write("Formato de datos incorrecto")
        else:

            #Si el correo es correcto se pide nombre y apellido del usuario
            nombre = st.text_input('Introduce nombre:')
            apellido = st.text_input('Introduce apellido:')

            if not isinstance(nombre, str) or not isinstance(apellido, str):
                st.write("Nombre u apellido no valido")
            else:

                # Si es correcto se pide el número de teléfono y se comprueba que sean 9 números
                telefono = st.text_input('Introduce telefono:')
                numero = re.compile(r'^[0-9]{9}$').match(telefono)

                if numero is None:
                    st.write("Teléfono no valido")
                else:
                    #Si es válido se pide dos veces la contraseña para comprobar que sean iguales
                    contrasena = st.text_input('Introduzca su contraseña:', type="password")
                    conf_contrasena = st.text_input('Confirme su contraseña:', type="password")

                    if contrasena == conf_contrasena:
                        reg = st.button("Crear cuenta")
                        if reg:
                            #Autentificacion de contraseñas por scrypt

                            #Se crea un salt que se usa en la función scrypt y después se deriva la contraseña
                            # Se crea el token y se guarda en la base de datos
                            salt = os.urandom(16)
                            kdf = kdf_crear(salt)
                            key = kdf.derive(contrasena.encode('ascii'))

                            #Se codifican los datos para guardarlos en la base de datos
                            key = codificar(key)
                            salt = codificar(salt)


                            #Cifrado - autentificado

                            #Se genera un salt nuevo para poder cifrar los datos
                            salt_clave = os.urandom(16)
                            salt_clave = codificar(salt_clave)


                            #Se guardan todos los datos del usuario en la base de datos
                            bd.execute("INSERT INTO user VALUES(?,?,?,?,?,?,?,?)",
                                       (usuario, correo, nombre, apellido, int(telefono), key, salt, salt_clave))
                            st.session_state["usuario"] = usuario
                            base.commit()
                            switch_page("Inicio_Sesion")

                    else:
                        st.write("las contraseñas no coinciden")
    base.close()




if __name__ == "__main__":
    Crear_Usuario()
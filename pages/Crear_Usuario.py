import re
from  Inicio_Sesion import  *
import os

def Crear_Usuario():
    base, bd = Abrir_bd()
    usuario = st.text_input('Introduce su nuevo nombre de usuario:')
    bd.execute("SELECT usuario FROM user WHERE usuario=?", (usuario,))
    usua = bd.fetchall()
    if len(usua) > 0:
        st.write("Usuario ya existe")
    else:
        correo = st.text_input('Introduce correo electronico:')

        c = re.compile(r'^[a-z0-9]+@[a-z]+\.[a-z]{3}$').match(correo)

        if c is None:
            st.write("Formato de datos incorrecto")
        else:
            nombre = st.text_input('Introduce nombre:')
            apellido = st.text_input('Introduce apellido:')
            if not isinstance(nombre, str) or not isinstance(apellido, str):
                st.write("Nombre u apellido no valido")
            else:
                telefono = st.text_input('Introduce telefono:')
                numero = re.compile(r'^[0-9]{9}$').match(telefono)

                if numero is None:
                    st.write("Telefono no valido")
                else:
                    contrasena = st.text_input('Introduzca su contraseña:', type="password")
                    conf_contrasena = st.text_input('Confirme su contraseña:', type="password")
                    if contrasena == conf_contrasena:
                        reg = st.button("Crear cuenta")
                        if reg:
                            #Autentificacion de contraseñas
                            salt = os.urandom(16)
                            kdf = kdf_crear(salt)
                            key = kdf.derive(contrasena.encode('ascii'))
                            key = codificar(key)
                            salt = codificar(salt)

                            #Cifrado - autentificado
                            salt_clave = os.urandom(16)
                            salt_clave = codificar(salt_clave)


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
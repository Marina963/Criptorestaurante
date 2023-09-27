import re
from  Inicio_Sesion import  *


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
                        bd.execute("INSERT INTO user VALUES(?,?,?,?,?,?)",
                                   (usuario, correo, nombre, apellido, int(telefono), contrasena))
                        st.session_state["create"]=True
                        st.session_state["usuario"] = usuario
                        reg = st.button("Crear cuenta")
                        if reg:
                            # Crear token
                            base.commit()
                            switch_page("Info_Restaurantes")
                    else:
                        st.write("las contraseñas no coinciden")
    base.close()

if __name__ == "__main__":
    Crear_Usuario()
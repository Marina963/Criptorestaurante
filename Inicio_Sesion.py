from data_base import  *
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import base64

def Inicio_Sesion():
    base, bd = Abrir_bd()
    usuario = st.text_input('Introduzca su usuario:')
    contrasena = st.text_input('Introduce su contraseña:', type="password")
    bd.execute("SELECT contraseña, salt FROM user WHERE usuario=?", (usuario,))
    true_cont = bd.fetchall()
    login = st.button("Inicio Sesion")
    crear_usuario = st.button("Crea tu cuenta")
    if crear_usuario:
        switch_page("Crear_Usuario")
    if login:
        if len(true_cont) == 0:
            st.write("Usuario no existe")
        else:
            key, salt = true_cont[0][0], true_cont[0][1]
            kdf = Scrypt(
                salt=salt,
                length=32,
                n=2 ** 14,
                r=8,
                p=1,
            )
            key = bytes(key,'ascii')
            key = base64.b64decode(key)

            try :
                kdf.verify(bytes(contrasena, 'ascii'), key)
            except:
                st.write("Contraseña incorrecta")
                return

            st.session_state["iniciado"] = True
            st.session_state["usuario"] = usuario
            switch_page("Info_Restaurantes")


    base.close()


if __name__ == "__main__":
    st.session_state["iniciado"] = False
    st.session_state["create"] = False
    st.session_state["usuario"] = None
    st.session_state["restaurante"] = None
    #borrar_tablas()
    #Crear_tablas()
    #insertar_restaurantes()
    Inicio_Sesion()







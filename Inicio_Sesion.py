from data_base import  *
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from criptografia import  *
from pem import *
from certificado import  *

#Archivo donde se inicia el programa. Módulo de inicio de sesión
def Inicio_Sesion():
    base, bd = Abrir_bd()

    #Input para que el usuario introduzca su nombre usuario y su contraseña
    usuario = st.text_input('Introduzca su usuario:')
    contrasena = st.text_input('Introduce su contraseña:', type="password")

    #Botones para iniciar sesión o ir a crear una cuenta
    login = st.button("Inicio Sesion")
    crear_usuario = st.button("Crea tu cuenta")

    if crear_usuario:
        switch_page("Crear_Usuario")
    if login:
        # En la base de datos se busca por el nombre de usuario para obtener el token y los salts
        bd.execute("SELECT contraseña, salt_contr, salt_clave FROM user WHERE usuario=?",
                   (usuario,))
        true_cont = bd.fetchall()

        #Se cumepra si el usuairio esta registrado
        if len(true_cont) == 0:
            st.write("Usuario no existe")
        else:
            key, salt, salt_clave = true_cont[0][0], true_cont[0][1],true_cont[0][2]

            # Autentificación de contraseñas por scrypt

            #Se decodifican los datos obtenidos de la base de datos
            salt = decodificar(salt)
            key = decodificar(key)
            salt_clave = decodificar(salt_clave)

            # Se usa el algoritmo scrypt para comprobar si la contraseña es igual a la dada
            kdf = kdf_crear(salt)
            try :
                kdf.verify(bytes(contrasena, 'ascii'), key)
            except:
                st.write("Contraseña incorrecta")
                return


            # Se guarda en las variables de sesión el usuario y la contraseña derivada para poder
            # cifrar en los siguientes pasos
            st.session_state["iniciado"] = True
            st.session_state["usuario"] = usuario
            st.session_state["contrasena"] = key_derive(contrasena, salt_clave)
            switch_page("Info_Restaurantes")

    base.close()


if __name__ == "__main__":
     #Variables de sesión (datos que solo se usan mientras la sesión está activa)
    st.session_state["iniciado"] = False
    st.session_state["usuario"] = None
    st.session_state["restaurante"] = None
    st.session_state["contrasena"] = None

    #Metodos para crear de nuevo las bases de datos
    #borrar_tablas()
    #Crear_tablas()
    #insertar_restaurantes()

    #Inicio del programa
    Inicio_Sesion()







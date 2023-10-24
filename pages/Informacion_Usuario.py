from  Inicio_Sesion import  *

#Página donde aparecen todas reservas del usuario y da la opción de cerrar sesión

def Inf_Res():
    #Solo se pude acceder si se ha iniciado sesión.
    #Si no es asi, se da la opción de iniciar sesión o registrarse
    if not st.session_state["iniciado"] :
        i_s = st.button("Inicio Sesion")
        reg = st.button("Registrarse")
        if i_s:
            switch_page("Inicio_Sesion")
        if reg:
            switch_page("Crear_Usuario")
    else:
        #Si se ha iniciado sesión se buscan en la base de datos las reservas del usuario
        base, bd = Abrir_bd()
        bd.execute("SELECT localizacion, fecha, hora, non_fecha, non_hora FROM reservas WHERE  usuario = ? ", (st.session_state["usuario"],))
        datos = bd.fetchall()

        # Cifrado - Autenticado

        #Se utiliza el algoritmo ChaCha20Poly1305 con la clave derivada
        #Esto crea un objeto chacha que se usará para descifrar y autentificar
        chacha = ChaCha20Poly1305(st.session_state["contrasena"])
        st.write("Reservas: ")

        for i in range (len(datos)):
            restaurante = datos[i][0]
            fecha = datos[i][1]
            hora =  datos[i][2]
            non_f = datos[i][3]
            non_h = datos[i][4]

            #Se decodifican los datos
            fecha =decodificar(fecha)
            hora = decodificar(hora)
            non_h = decodificar(non_h)
            non_f = decodificar(non_f)

            #Se descifran los datos y se comprueba la etiqueta de autentificación
            fecha = chacha.decrypt(non_f, fecha, None)
            hora = chacha.decrypt(non_h, hora, None)

            st.write("Tiene una reserva en el restaurante :", restaurante,", el dia", fecha,"a la hora ", str(hora))
        Cerrar_Sesion()
        base.close()

def Cerrar_Sesion():
    #Se cierra la sesión y se borran los datos de sesión.
    cerrar = st.button("Cerrar sesion")
    if cerrar:
        st.session_state["iniciado"] = False
        st.session_state["usuario"] = None
        st.session_state["restaurante"] = None
        st.session_state["contrasena"] = None
        switch_page("Info_Restaurantes")


if __name__ == "__main__":
    Inf_Res()

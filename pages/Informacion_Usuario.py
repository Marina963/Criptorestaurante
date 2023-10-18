from  Inicio_Sesion import  *

def Inf_Res():
    if not st.session_state["iniciado"] :
        i_s = st.button("Inicio Sesion")
        reg = st.button("Registrarse")
        if i_s:
            switch_page("Inicio_Sesion")
        if reg:
            switch_page("Crear_Usuario")
    else:
        base, bd = Abrir_bd()
        bd.execute("SELECT localizacion, fecha, hora, non_fecha, non_hora FROM reservas WHERE  usuario = ? ", (st.session_state["usuario"],))
        datos = bd.fetchall()

        chacha = ChaCha20Poly1305(st.session_state["contrasena"])
        st.write("Reservas: ")

        for i in range (len(datos)):
            restaurante = datos[i][0]
            fecha = datos[i][1]
            hora =  datos[i][2]
            non_f = datos[i][3]
            non_h = datos[i][4]

            fecha =decodificar(fecha)
            hora = decodificar(hora)
            non_h = decodificar(non_h)
            non_f = decodificar(non_f)

            fecha = chacha.decrypt(non_f, fecha, None)
            hora = chacha.decrypt(non_h, hora, None)

            st.write("Tiene una reserva en el restaurante :", restaurante,", el dia", fecha,"a la hora ", str(hora))
        Cerrar_Sesion()
        base.close()

def Cerrar_Sesion():
    cerrar = st.button("Cerrar sesion")
    if cerrar:
        st.session_state["iniciado"] = False
        st.session_state["create"] = False
        switch_page("Info_Restaurantes")


if __name__ == "__main__":
    Inf_Res()

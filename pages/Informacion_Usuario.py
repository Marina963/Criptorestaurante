from  Inicio_Sesion import  *
def Inf_Res():
    if not st.session_state["iniciado"] and not st.session_state["create"]:
        i_s = st.button("Inicio Sesion")
        reg = st.button("Registrarse")
        if i_s:
            switch_page("Inicio_Sesion")
        if reg:
            switch_page("Crear_Usuario")
    else:
        base, bd = Abrir_bd()
        bd.execute("SELECT localizacion, fecha, hora FROM reservas WHERE  usuario = ? ", (st.session_state["usuario"],))
        datos = bd.fetchall()
        st.write("Reservas: ")
        for i in range (len(datos)):
            restaurante = datos[i][0]
            fecha = datos[i][1]
            hora =  datos[i][2]
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

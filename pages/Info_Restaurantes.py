from Inicio_Sesion import  *

def info_restaurante():
    base, bd = Abrir_bd()
    st.title("Página de información")


    bd.execute("SELECT localizacion FROM restaurante")
    restaurant = bd.fetchall()
    lista_rest = []
    for i in range(len(restaurant)):
        lista_rest.append(restaurant[i][0])
    rest_elegido = st.selectbox("¿Que restaurnate desea visitar?: ", lista_rest)
    bd.execute(
        "SELECT telefono, valoracion, horario_apertura, horario_cerrar FROM restaurante WHERE localizacion=?",
        (rest_elegido,))
    datos = bd.fetchall()
    tel, val, hor_i, hor_c = datos[0][0], datos[0][1], datos[0][2], datos[0][3]
    st.write("Telefono:", str(tel))
    st.write("Valoracion: ", str(val))
    st.write("Hora de apertura: ", str(hor_i))
    st.write("Hora de cierre: ", str(hor_c))
    reserva = st.button("Reservar")
    if reserva:
        st.session_state["restaurante"] = rest_elegido
        switch_page("Reserva")
    base.close()




if __name__ == "__main__":
    info_restaurante()




from Inicio_Sesion import *
import datetime


def reserva():
    base, bd = Abrir_bd()

    disponible = False
    if not st.session_state["iniciado"] and not st.session_state["create"]:
        i_s = st.button("Inicio Sesion")
        reg = st.button("Registrarse")
        if i_s:
            switch_page("Inicio_Sesion")
        if reg:
            switch_page("Crear_Usuario")
    else:
        st.write("Esta haciendo una resevapa para el restaurante: ",st.session_state["restaurante"])
        today = datetime.datetime.today()
        fecha = st.date_input(label="Elige una fecha", min_value=today)
        st.write(fecha)
        bd.execute("SELECT horario_apertura, horario_cerrar FROM restaurante WHERE localizacion=?",
                   (st.session_state["restaurante"],))
        ho = bd.fetchall()
        hora_a = ho[0][0]
        hora_c = ho[0][1]
        horas = []
        while hora_a <= hora_c:
            horas.append(str(hora_a) + ":00")
            hora_a += 1
        personas = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        pers_opcion = st.selectbox("¿Para cuantas personas es la reserva?: ", personas)
        hora_opcion = st.selectbox("eleccione una hora: ", horas)

        hora_opcion = int(hora_opcion[0:2])

        bd.execute("SELECT ocupacion FROM aforo WHERE localizacion=? and hora = ? and fecha= ?",
                   (st.session_state["restaurante"], hora_opcion, fecha))
        aforo = bd.fetchall()
        if len(aforo) == 0:
            bd.execute("SELECT aforo FROM restaurante WHERE localizacion=?",
                       (st.session_state["restaurante"],))
            aforo_r = bd.fetchall()
            if aforo_r[0][0] < pers_opcion:
                st.write("Aforo completo")
            else:
                n_per = aforo_r[0][0] - pers_opcion
                bd.execute("INSERT INTO aforo VALUES(?,?,?,?)",
                           (st.session_state["restaurante"], fecha, hora_opcion, n_per))
                disponible = True

        elif aforo[0][0] <= 0:
            st.write("Aforo completo")
        else:
            n_per = aforo[0][0] - pers_opcion
            if n_per < 0:
                st.write("Aforo insuficiente")
            else:
                bd.execute(
                    "UPDATE aforo set AFORO = ? WHERE localizacion=? and hora = ? and fecha= ?", (
                        n_per, st.session_state["restaurante"], hora_opcion, fecha))
                disponible = True

        if disponible:
            st.write("La fecha seria: ", str(fecha), "a las", str(hora_opcion) + ":00 ", "para", str(pers_opcion), "personas")

            res_opcion = st.button("Confirma tu reserva: ")

            if res_opcion:
                st.write("Reserva confirmada")
                bd.execute("INSERT INTO reservas VALUES(?,?,?,?,?)",
                           (st.session_state["usuario"], st.session_state["restaurante"],
                            hora_opcion, fecha, pers_opcion))

                base.commit()
                switch_page("Info_Restaurantes")
    base.close()

if __name__ == "__main__":
    reserva()

import streamlit as st
import sqlite3 as sl
import Interfaz as interfaz
import pages.informacion as informacion

base = sl.connect("Base_datos.db")
bd = base.cursor()
bd.execute("PRAGMA foreign_keys=on")


dias = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
anyo = 2023
horas = [10, 11, 12]
personas = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
pers_opcion = st.selectbox("¿Para cuantas personas es la reserva?: ", personas)
mes_opcion = st.selectbox("Seleccione un mes: ", meses)
dia_opcion = st.selectbox("Seleccione un dia: ", dias)
hora_opcion = st.selectbox("eleccione una hora: ", horas)
#pers_opcion, llave5 = pick.pick(meses, "¿Para cuantas personas es la reserva?: ", indicator="=>")
#mes_opcion, llave2 = pick.pick(meses, "Seleccione un mes: ", indicator="=>")
#dia_opcion, llave = pick.pick(dias, "Seleccione un dia: ", indicator="=>")
#hora_opcion, llave4 = pick.pick(horas, "Seleccione una hora: ", indicator="=>")
fecha = (str(anyo),  '/', str(mes_opcion), '/',str(dia_opcion))
fecha = "".join(fecha)
bd.execute("SELECT ocupacion FROM aforo WHERE localizacion=? and hora = ? and fecha= ?", (informacion.rest_opcion, hora_opcion, fecha))
aforo = bd.fetchall()
if len(aforo) == 0 :
    bd.execute("SELECT aforo FROM restaurante WHERE localizacion=?", (informacion.rest_opcion,))
    aforo_r = bd.fetchall()
    if aforo_r[0][0] < pers_opcion:
        st.write("Aforo completo")
    else:
        n_per = aforo_r[0][0] - pers_opcion
        bd.execute("INSERT INTO aforo VALUES(?,?,?,?)",(informacion.rest_opcion, fecha, hora_opcion, n_per))
        disponible = True

elif aforo[0][0] <= 0:
    st.write("Aforo completo")
else:
    n_per = aforo[0][0] - pers_opcion
    if n_per < 0:
        st.write("Aforo insuficiente")
    else:
        bd.execute("UPDATE aforo set AFORO = ? WHERE localizacion=? and hora = ? and fecha= ?", (
        n_per, informacion.rest_opcion, hora_opcion, fecha))
        disponible = True

if disponible:
    st.write("La fecha seria: ", str(dia_opcion), "/", str(mes_opcion), "/", str(anyo), "a las", hora_opcion,
          "para", pers_opcion, "personas")

    #reserva = ['Confirmar', 'Cambiar seleccion']
    res_opcion = st.button("Confirma tu reserva: ")
    #res_opcion, llave3 = pick.pick(reserva, "Confirma tu reserva: ", indicator="=>")
    if res_opcion == True:
        st.write("Reserva confirmada")
        reservado = True
        bd.execute("INSERT INTO reservas VALUES(?,?,?,?,?)", (interfaz.usuario, informacion.rest_opcion, hora_opcion, fecha, pers_opcion))

        base.commit()

base.close()
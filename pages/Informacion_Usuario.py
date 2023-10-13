from  Inicio_Sesion import  *
import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
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
        bd.execute("SELECT localizacion, fecha, hora,non_loc, non_fecha, non_hora FROM reservas WHERE  usuario = ? ", (st.session_state["usuario"],))
        datos = bd.fetchall()



        aad = None






        st.write("Reservas: ")
        for i in range (len(datos)):
            restaurante = datos[i][0]
            fecha = datos[i][1]
            hora =  datos[i][2]
            non_r = datos[i][3]
            non_f = datos[i][4]
            non_h = datos[i][5]

            non_h = bytes(non_h, 'ascii')
            non_h = base64.b64decode(non_h)
            non_r = bytes(non_r, 'ascii')
            non_r = base64.b64decode(non_r)
            non_f = bytes(non_f, 'ascii')
            non_f = base64.b64decode(non_f)

            key = ChaCha20Poly1305.generate_key()
            chacha = ChaCha20Poly1305(key)
            restaurante = chacha.decrypt(non_r, restaurante, aad)

            key = ChaCha20Poly1305.generate_key()
            chacha = ChaCha20Poly1305(key)
            fecha = chacha.decrypt(non_f, fecha, aad)

            key = ChaCha20Poly1305.generate_key()
            chacha = ChaCha20Poly1305(key)
            hora = chacha.decrypt(non_h, hora, aad)
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

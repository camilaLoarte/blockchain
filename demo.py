"""
Demo end-to-end de la DAO Estudiantil (prototipo Fase III)
=============================================================
Simula el ciclo de vida completo de una decisión dentro de la DAO:
1. Registro de identidades (estudiantes, facultades, consejo)
2. Creación de una propuesta
3. Validación / endoso multi-organización (2 de 3 facultades)
4. Apertura de votación
5. Emisión de votos (pseudónimos)
6. Cierre y conteo automático
7. Consulta pública de resultados
8. Verificación de integridad del ledger (+ intento de manipulación)
"""
from chaincode import DAOChaincode


def main():
    dao = DAOChaincode()

    print("\n--- 1. REGISTRO DE IDENTIDADES ---")
    dao.registro_identidad("tais.carreno", "estudiante", "Ingenieria", "tais@uide.edu.ec")
    dao.registro_identidad("camila.loarte", "estudiante", "Ingenieria", "camila@uide.edu.ec")
    dao.registro_identidad("luis.perez", "estudiante", "Administracion", "luis@uide.edu.ec")
    dao.registro_identidad("fac.ingenieria", "facultad", "Ingenieria")
    dao.registro_identidad("fac.administracion", "facultad", "Administracion")
    dao.registro_identidad("consejo.universitario", "consejo", "Rectorado")

    print("\n--- 2. CREACION DE PROPUESTA ---")
    propuesta = dao.crear_propuesta(
        autor="tais.carreno",
        titulo="Presupuesto para el Club de Robotica",
        texto="Solicitud de $1500 para materiales de competencia...",
    )

    print("\n--- 3. VALIDACION / ENDOSO (2 de 3 organizaciones) ---")
    dao.validar(propuesta.id, "fac.ingenieria", "facultad")
    dao.validar(propuesta.id, "fac.administracion", "facultad")

    print("\n--- 4. APERTURA DE VOTACION ---")
    dao.abrir_votacion(propuesta.id, quorum=2, admin="consejo.universitario")

    print("\n--- 5. EMISION DE VOTOS ---")
    dao.emitir_voto(propuesta.id, "tais.carreno", "a_favor")
    dao.emitir_voto(propuesta.id, "camila.loarte", "a_favor")
    dao.emitir_voto(propuesta.id, "luis.perez", "en_contra")

    print("\n--- 6. CIERRE Y CONTEO ---")
    dao.cerrar_y_contar(propuesta.id)

    print("\n--- 7. CONSULTA DE RESULTADOS ---")
    print(dao.consultar_resultados(propuesta.id))

    print("\n--- 8. VERIFICACION DE INTEGRIDAD DEL LEDGER ---")
    print(f"Ledger íntegro: {dao.ledger.verificar_integridad()}")
    dao.ledger.imprimir()

    print("\n--- 9. INTENTO DE VOTO DUPLICADO (debe fallar) ---")
    try:
        dao.emitir_voto(propuesta.id, "tais.carreno", "a_favor")
    except Exception as e:
        print(f"[ESPERADO] {type(e).__name__}: {e}")

    print("\n--- 10. PRUEBA DE INMUTABILIDAD: manipular un bloque a la fuerza ---")
    dao.ledger.cadena[3].transacciones[0]["opcion"] = "en_contra"   # alteración maliciosa
    print(f"Ledger íntegro tras manipulación: {dao.ledger.verificar_integridad()}"
          "  <-- debe salir False, demostrando que la alteración es detectable")


if __name__ == "__main__":
    main()

import json
import os

ARCHIVO = "turnos.json"


def cargar_turnos():
    if not os.path.exists(ARCHIVO):
        return []
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def guardar_turnos(turnos):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(turnos, f, indent=4, ensure_ascii=False)


def agregar_turno():
    turnos = cargar_turnos()

    cliente = input("Nombre del cliente: ").strip()
    fecha = input("Fecha (YYYY-MM-DD): ").strip()
    hora = input("Hora (HH:MM): ").strip()

    # Validación simple: evitar duplicados
    for t in turnos:
        if t["fecha"] == fecha and t["hora"] == hora:
            print("⚠️ Ya existe un turno en ese horario.")
            return

    nuevo_turno = {
        "cliente": cliente,
        "fecha": fecha,
        "hora": hora
    }

    turnos.append(nuevo_turno)
    guardar_turnos(turnos)

    print("✅ Turno guardado correctamente.")


def ver_turnos():
    turnos = cargar_turnos()

    if not turnos:
        print("No hay turnos cargados.")
        return

    # Ordenar por fecha y hora
    turnos_ordenados = sorted(turnos, key=lambda x: (x["fecha"], x["hora"]))

    print("\n📅 Lista de turnos:")
    for i, t in enumerate(turnos_ordenados, start=1):
        print(f"{i}. {t['fecha']} {t['hora']} - {t['cliente']}")


def eliminar_turno():
    turnos = cargar_turnos()

    if not turnos:
        print("No hay turnos para eliminar.")
        return

    ver_turnos()
    try:
        indice = int(input("Número de turno a eliminar: ")) - 1
        if 0 <= indice < len(turnos):
            eliminado = turnos.pop(indice)
            guardar_turnos(turnos)
            print(f"🗑️ Turno eliminado: {eliminado['cliente']}")
        else:
            print("Índice inválido.")
    except ValueError:
        print("Ingresá un número válido.")


def menu():
    while True:
        print("\n--- SISTEMA DE TURNOS ---")
        print("1. Agregar turno")
        print("2. Ver turnos")
        print("3. Eliminar turno")
        print("4. Salir")

        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            agregar_turno()
        elif opcion == "2":
            ver_turnos()
        elif opcion == "3":
            eliminar_turno()
        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()
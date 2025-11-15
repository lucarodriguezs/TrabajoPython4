###Imports 
import csv
import os
from datetime import datetime

###Variables

reservas = {}
contador_id=0
cabanas = {
    'C1': {'nombre': 'Cabaña Familiar Grande', 'capacidad': 8},
    'C2': {'nombre': 'Cabaña Familiar Mediana', 'capacidad': 6},
    'C3': {'nombre': 'Cabaña Familiar Pequeña', 'capacidad': 4},
    'C4': {'nombre': 'Cabaña Romántica', 'capacidad': 2},
    'C5': {'nombre': 'Cabaña Aventura', 'capacidad': 5}
}
ARCHIVO_CSV = 'reservas.csv'
### Validaciones
def validar_rut(rut):
    rut = rut.strip().upper()
    if not rut:
        return False
    rut = rut.replace('.', '').replace('-', '')
    if len(rut) < 8 or len(rut) > 9:
        return False
    return rut[:-1].isdigit() # .isdigit Sirve para revisar si es un digito (Devuelve True/False)

def formatear_rut(rut):
    rut = rut.strip().upper().replace('.', '').replace('-', '')
    return f"{rut[:-1]}-{rut[-1]}"

def validar_fecha(fecha_str):
    try:
        datetime.strptime(fecha_str, '%d/%m/%Y')
        return True
    except ValueError:
        return False

### Sistemas

def crear_reserva():
    id_reserva = str(len(reservas) + 1)
    while True:
        rut = input("\nRUT del cliente (ej: 12345678-9): ").strip()
        if validar_rut(rut):
            rut = formatear_rut(rut)
            break
        print(" RUT inválido. Intente nuevamente.")
    nombre=input("Nombre completo del cliente")
    for cod, info in cabanas.items():
        print(f"{cod}: {info['nombre']} (Capacidad: {info['capacidad']} personas)")
    while True:
        cod_cabana = input("\nCódigo de cabaña: ").strip().upper()
        if cod_cabana in cabanas:
            break
        print("Código de cabaña inválido.")
    while True:
        fecha_entrada = input("Fecha de entrada (DD/MM/AAAA): ").strip()
        if validar_fecha(fecha_entrada):
            break
        print("Formato de fecha inválido.")
    
    while True:
        fecha_salida = input("Fecha de salida (DD/MM/AAAA): ").strip()
        if validar_fecha(fecha_salida):
            entrada = datetime.strptime(fecha_entrada, '%d/%m/%Y')
            salida = datetime.strptime(fecha_salida, '%d/%m/%Y')
            if salida > entrada:
                    break
            print("La fecha de salida no puede ser antes de la de entrada.")
        else:
                print("Formato de fecha inválido.")
    while True:
        num_personas = input(f"Número de personas (máx {cabanas[cod_cabana]['capacidad']}): ").strip()
        num_personas = int(num_personas)
        if num_personas <= cabanas[cod_cabana]['capacidad']:
            break
        print(f"Excede la capacidad de la cabaña ({cabanas[cod_cabana]['capacidad']} personas).")
        1
    reservas[id_reserva] = {
        'rut': rut,
        'nombre': nombre,
        'cod_cabana': cod_cabana,
        'nombre_cabana': cabanas[cod_cabana]['nombre'],
        'fecha_entrada': fecha_entrada,
        'fecha_salida': fecha_salida,
        'num_personas': num_personas,
        'estado': 'Activa'
    }
    
    print(f" Reserva {id_reserva} creada exitosamente")
    print(f"Cliente: {nombre} - Cabaña: {cabanas[cod_cabana]['nombre']}")

def listar_reservas():
    if not reservas:
        print("No hay reservas registradas.")
        return
    print("LISTADO DE RESERVAS")
    for id_res, datos in reservas.items():
        print(f"{id_res:} {datos['rut']} {datos['nombre']} {datos['nombre_cabana']} "
              f"{datos['fecha_entrada']} {datos['fecha_salida']} {datos['num_personas']} {datos['estado']}")
    print(f"Total de reservas: {len(reservas)}")
def buscar_por_rut():
    print("BUSCAR RESERVAS POR RUT")
    rut = input("\nIngrese RUT a buscar: ").strip()
    if not validar_rut(rut):
        print("RUT inválido.")
        return
    
    rut = formatear_rut(rut)
    encontradas = {}
    for k, v in reservas.items():
        if v["rut"] == rut:
            encontradas[k] = v
    
    if not encontradas:
        print(f"No se encontraron reservas para el RUT {rut}")
        return
    
    print(f"Se encontraron {len(encontradas)} reserva(s):")
    print(f"{'ID':<8} {'Cliente':<20} {'Cabaña':<25} {'Entrada':<12} {'Salida':<12} {'Estado':<10}")
    
    for id_res, datos in encontradas.items():
        print(f"{id_res:<8} {datos['nombre']:<20} {datos['nombre_cabana']:<25} "
              f"{datos['fecha_entrada']:<12} {datos['fecha_salida']:<12} {datos['estado']:<10}")
        
def actualizar_reserva():
    if not reservas:
        print("No hay reservas para actualizar.")
        return
    print("          ACTUALIZAR RESERVA")
    id_reserva = input("\nIngrese ID de la reserva: ").strip().upper()
    
    if id_reserva not in reservas:
        print("Reserva no encontrada.")
        return
    
    reserva = reservas[id_reserva]
    print(f"\nReserva actual:")
    print(f"Cliente: {reserva['nombre']} (RUT: {reserva['rut']})")
    print(f"Cabaña: {reserva['nombre_cabana']}")
    print(f"Entrada: {reserva['fecha_entrada']} | Salida: {reserva['fecha_salida']}")
    print(f"Personas: {reserva['num_personas']} | Estado: {reserva['estado']}")
    
    print("\n¿Qué desea actualizar?")
    print("1. Fechas")
    print("2. Número de personas")
    print("3. Estado (Activa/Cancelada)")
    print("4. Volver")
    
    opcion = input("\nSeleccione opción: ").strip()
    
    if opcion == '1':
        while True:
            fecha_entrada = input("Nueva fecha de entrada (DD/MM/AAAA): ").strip()
            if validar_fecha(fecha_entrada):
                break
            print("Ingrese el formato correcto")
        
        while True:
            fecha_salida = input("Nueva fecha de salida (DD/MM/AAAA): ").strip()
            if validar_fecha(fecha_salida):
                entrada = datetime.strptime(fecha_entrada, '%d/%m/%Y')
                salida = datetime.strptime(fecha_salida, '%d/%m/%Y')
                if salida > entrada:
                    break
                print("La fecha de salida no puede ser antes de la de entrada.")
            else:
                print("Ingrese el formato correcto")
        
        reservas[id_reserva]['fecha_entrada'] = fecha_entrada
        reservas[id_reserva]['fecha_salida'] = fecha_salida
        print("Fechas actualizadas.")
        
    elif opcion == '2':
        capacidad = cabanas[reserva['cod_cabana']]['capacidad']
        while True:
            num = input(f"Nuevo número de personas (máx {capacidad}): ").strip()
            num = int(num)
            if num <= capacidad:
                reservas[id_reserva]['num_personas'] = num
                print("Número de personas actualizado.")
                break
            print(f"Excede la capacidad ({capacidad} personas).")
            
                
    elif opcion == '3':
        print("1. Activa")
        print("2. Cancelada")
        estado = input("Seleccione estado: ").strip()
        if estado == '1':
            reservas[id_reserva]['estado'] = 'Activa'
            print("Estado actualizado a Activa.")
        elif estado == '2':
            reservas[id_reserva]['estado'] = 'Cancelada'
            print("Estado actualizado a Cancelada.")
        else:
            print("Opción inválida.")

def eliminar_reserva():
    if not reservas:
        print("  No hay reservas para eliminar.")
        return
    print("ELIMINAR RESERVA")
    id_reserva = input("\nIngrese ID de la reserva: ").strip().upper()
    
    if id_reserva not in reservas:
        print("Reserva no encontrada.")
        return
    
    reserva = reservas[id_reserva]
    print(f"\nReserva a eliminar:")
    print(f"ID: {id_reserva}")
    print(f"Cliente: {reserva['nombre']}")
    print(f"Cabaña: {reserva['nombre_cabana']}")
    print(f"Fechas: {reserva['fecha_entrada']} - {reserva['fecha_salida']}")
    
    confirmacion = input("\n¿Está seguro de eliminar esta reserva? (S/N): ").strip().upper()
    
    if confirmacion == 'S':
        del reservas[id_reserva]
        print("Reserva eliminada exitosamente.")
    else:
        print("Operación cancelada.")

def reporte_ocupacion():

    print("REPORTE DE OCUPACIÓN")

    
    if not reservas:
        print("\nNo hay reservas para generar reporte.")
        return
    ocupacion = {}
    for cod in cabanas.keys():
        ocupacion[cod] = 0
    
    for datos in reservas.values():
        if datos['estado'] == 'Activa':
            ocupacion[datos['cod_cabana']] += 1
    
    print(f"\n{'Código':<8} {'Cabaña':<30} {'Capacidad':<10} {'Reservas Activas'}:<18")
    
    for cod, info in cabanas.items():
        print(f"{cod:<8} {info['nombre']:<30} {info['capacidad']:<10} {ocupacion[cod]:<18}")
    total_reservas = len(reservas)
    activas = sum(1 for r in reservas.values() if r['estado'] == 'Activa')
    canceladas = total_reservas - activas
    
    print(f"\nTotal de reservas: {total_reservas}")
    print(f"Reservas activas: {activas}")
    print(f"Reservas canceladas: {canceladas}")

def exportar_csv():
    if not reservas:
        print("No hay reservas para exportar.")
        return
    
    try:
        with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as archivo:
            campos = ['id_reserva', 'rut', 'nombre', 'cod_cabana', 'nombre_cabana', 
                     'fecha_entrada', 'fecha_salida', 'num_personas', 'estado']
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            
            escritor.writeheader()
            
            for id_res, datos in reservas.items():
                fila = {'id_reserva': id_res}
                fila.update(datos)
                escritor.writerow(fila)
        
        print(f"Reservas exportadas exitosamente a '{ARCHIVO_CSV}'")
        print(f"Total de registros exportados: {len(reservas)}")
    except Exception as e:
        print("Error al exportar")

def importar_csv():
    if not os.path.exists(ARCHIVO_CSV):
        print(f"Archivo '{ARCHIVO_CSV}' no encontrado.")
        return
    
    try:
        with open(ARCHIVO_CSV, 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            contador = 0
            
            for fila in lector:
                id_res = fila['id_reserva']
                reservas[id_res] = {
                    'rut': fila['rut'],
                    'nombre': fila['nombre'],
                    'cod_cabana': fila['cod_cabana'],
                    'nombre_cabana': fila['nombre_cabana'],
                    'fecha_entrada': fila['fecha_entrada'],
                    'fecha_salida': fila['fecha_salida'],
                    'num_personas': int(fila['num_personas']),
                    'estado': fila['estado']
                }
                contador += 1
        
        print(f" Reservas importadas exitosamente desde '{ARCHIVO_CSV}'")
        print(f"Total de registros importados: {contador}")
    except Exception as e:
        print("Error al importar")

##Menu
def menu():
    print("\n REFUGIO ANDINO")
    print("\n1.  Crear nueva reserva")
    print("2.  Listar todas las reservas")
    print("3.  Buscar reservas por RUT")
    print("4.  Actualizar reserva")
    print("5.  Eliminar reserva")
    print("6.  Reporte de ocupación")
    print("7.  Exportar reservas a CSV")
    print("8.  Importar reservas desde CSV")
    print("9.  Salir")

def main():
    print("Bienvenido al sistema de gestion de registro de Refugio Andino")

    if os.path.exists(ARCHIVO_CSV):
        print(f"\n📂 Archivo '{ARCHIVO_CSV}' detectado.")
        cargar = input("¿Desea cargar las reservas existentes? (S/N): ").strip().upper()
        if cargar == 'S':
            importar_csv()

    while True:
        menu()
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == '1':
            crear_reserva()
        elif opcion == '2':
            listar_reservas()
        elif opcion == '3':
            buscar_por_rut()
        elif opcion == '4':
            actualizar_reserva()
        elif opcion == '5':
            eliminar_reserva()
        elif opcion == '6':
            reporte_ocupacion()
        elif opcion == '7':
            exportar_csv()
        elif opcion == '8':
            importar_csv()
        elif opcion == '9':
            
            print("\n" + "="*60)
            if reservas:
                guardar = input("¿Desea guardar los cambios antes de salir? (S/N): ").strip().upper()
                if guardar == 'S':
                    exportar_csv()
            
            print("Programa terminado")
            break
        else:
            print("Ingrese una opción valida")
        input("Aprete enter para continuar")


if __name__ == "__main__":
    main()
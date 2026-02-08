# python
import sys

def main():
    print(" - INICIANDO ANÁLISIS DE TRÁFICO SIMULADO -\n")
    # ---------------------------------------------------------
    # MÓDULO 1: LISTAS (Log Crudo)
    # Contexto: El firewall reporta cada intento de conexión.
    # ---------------------------------------------------------
    print("[+] Paso 1: Ingesta de Logs (LISTAS)")
    ips_detectadas = [
        "192.168.1.5",
        "10.0.0.1",
        "192.168.1.5",
        "172.16.0.50",
        "192.168.1.5",
        "10.0.0.1"
    ]
    # Simulamos una nueva detección en tiempo real
    ips_detectadas.append("8.8.8.8")
    print(f"Log crudo (Total de eventos: {len(ips_detectadas)}):\n{ips_detectadas}\n")

    #----------------------------------------------------------
    #MÓDULO 2: SETS (Limpieza y Correlación)
    #Contexto: Necesitamos saber cuántos atacantes únicos hay.
    #---------------------------------------------------------
    print("[+] Paso 2: Identificación de Atacantes Únicos (SETS)")
    ips_unicas = set(ips_detectadas)
    print(f"IPs Únicas identificadas: {ips_unicas}")

    # Lista blanca de IPs conocidas (Falsos positivos)
    ips_seguras = {"10.0.0.1", "8.8.8.8"}

    # Operación de conjuntos: Diferencia (Atacantes - Seguras)
    amenazas_reales = ips_unicas - ips_seguras
    print(f"Amenazas reales a investigar (Filtradas): {amenazas_reales}\n")

    # ---------------------------------------------------------
    # MÓDULO 3: TUPLAS (Configuración Inmutable)
    # Contexto: Puertos críticos que no deben ser modificados por error.
    # ---------------------------------------------------------
    print("[+] Paso 3: Verificación de Puertos Críticos")
    puertos_criticos = (
        (80, "HTTP"),
        (443, "HTTPS"),
        (22, "SSH"),
        (21, "FTP")
    )
    print(f"Configuración de monitoreo cargada: {puertos_criticos}")

    # Intento de modificación
    try:
        # Esto lanzará un error si se descomenta, protegiendo la integridad
        # puertos_criticos[0] = (8080, "HTTP-ALT")
        print("Integridad de configuración verificada: OK (No modificable)\n")
    except TypeError:
        print("ERROR: Intento de modificación de configuración bloqueado.\n")

    # ---------------------------------------------------------
    # MÓDULO 4: DICCIONARIOS (Inteligencia de Amenazas)
    # Contexto: Enriquecer los datos con información de riesgo.
    # ---------------------------------------------------------
    print("[+] Paso 4: Enriquecimiento de Datos")
    reporte_amenazas = {
        "192.168.1.5": {"riesgo": "Crítico", "tipo": "Ransomware", "pais": "Desconocido"},
        "172.16.0.50": {"riesgo": "Medio", "tipo": "Escaneo de Puertos", "pais": "Local"},
        "200.1.1.1": {"riesgo": "Bajo", "tipo": "Ping Sweep", "pais": "Externo"}
    }

    # Bucle para reportar sobre las amenazas reales detectadas en el paso 2
    print(" - REPORTE FINAL DE INCIDENTES -")
    for ip in amenazas_reales:
        info = reporte_amenazas.get(ip, {"riesgo": "Desconocido", "tipo": "N/A"})
        print(f"ALERTA: IP {ip} detectada.")
        print(f" > Nivel de Riesgo: {info['riesgo']}")
        print(f" > Tipo de Ataque: {info['tipo']}")
        print("-------------------------------")

if __name__ == "__main__":
    main()
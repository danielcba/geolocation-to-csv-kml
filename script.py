import pandas as pd
import csv
import ipinfo
import simplekml  # Importamos la librería 'simplekml'

# Función para obtener ubicación con 'ipinfo'


def get_ubicacion_ipinfo(direccion_ip, handler):
    details = handler.getDetails(direccion_ip)
    return pd.DataFrame({
        'Ciudad': [details.city],
        'Región': [details.region],
        'País': [details.country],
        'Latitud': [details.latitude],
        'Longitud': [details.longitude],
        'ASN': [details.org],
        'Direccion_ip': [direccion_ip]
    })


# Inicializamos el DataFrames vacío
df_ipinfo = pd.DataFrame(
    columns=['Ciudad', 'Región', 'País', 'Latitud', 'Longitud', 'ASN', 'Direccion_ip'])

# Token para 'ipinfo'
access_token = 'you_token'
handler = ipinfo.getHandler(access_token)

# Crear un objeto KML
kml = simplekml.Kml()

# Leer el archivo CSV
with open('geo.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        direccion_ip = row['direcciones']
        print(f"Consultando IP: {direccion_ip}")

        # Obtener ubicación con 'ipinfo' y agregar al DataFrame
        ubicacion_ipinfo = get_ubicacion_ipinfo(direccion_ip, handler)
        df_ipinfo = pd.concat([df_ipinfo, ubicacion_ipinfo], ignore_index=True)

        # Obtener las coordenadas para el KML
        latitud = ubicacion_ipinfo['Latitud'].iloc[0]
        longitud = ubicacion_ipinfo['Longitud'].iloc[0]
        ciudad = ubicacion_ipinfo['Ciudad'].iloc[0]

        # Agregar el punto al archivo KML
        kml.newpoint(name=ciudad, coords=[(longitud, latitud)])

# Guardar el DataFrames en archivo CSV
df_ipinfo.to_csv(ipinfo_resultados.csv', index=False)

# Guardar el archivo KML
kml.save("resultados.kml")

print("Archivos CSV y KML guardados exitosamente.")
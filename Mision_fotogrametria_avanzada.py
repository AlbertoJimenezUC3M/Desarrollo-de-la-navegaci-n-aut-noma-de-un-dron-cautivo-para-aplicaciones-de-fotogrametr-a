#!/usr/bin/env python3

import asyncio

from mavsdk import System
from mavsdk.mission import (MissionItem, MissionPlan)


async def run():
    drone = System()  #Creaión de un sistema denominado drone
    await drone.connect(system_address="udp://:14540")  #Dirección de conexión con el dron

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():  #Bucle de espera hasta la conexión con el dron
        if state.is_connected:
            print("Drone discovered!")
            break

    print_mission_progress_task = asyncio.ensure_future(  #Órdenes para mostrar en pantalla el progreso de la misión
        print_mission_progress(drone))

    running_tasks = [print_mission_progress_task]
    termination_task = asyncio.ensure_future(
        observe_is_in_air(drone, running_tasks))

    latitude=0.0 #Definir variable float: latitude
    longitude=0.0 #Definir variable float: longitude
    print("Fetching home location coordinates...")
    async for terrain_info in drone.telemetry.home(): #Bucle de espera hasta la geolocalización del dron
        latitude = terrain_info.latitude_deg #Almacenar la latitud de las coordenadas del dron en la variable latitude
        longitude = terrain_info.longitude_deg #Almacenar la longitud de las coordenadas del dron en la variable longitude
        break

    await asyncio.sleep(1)
    print("Latitud")
    print(latitude) #Mostrar en pantalla la latitud de la geoposición del dron

    print("Longitud")
    print(longitude)  #Mostrar en pantalla la longitud de la geoposición del dron
    await asyncio.sleep(1)

    lat_home = latitude  #Almacenar en la variable lat_home la latitud de las coordenadas de despegue
    lon_home = longitude #Almacenar en la variable lon_home la longitud de las coordenadas de despegue

    num_lat = latitude - 0.000035 #Incremento de posición en latitud
    num_lon = longitude - 0.00005 #Incremento de posición en longitud

    mission_items = []  #Especificar los waypoints de la misión y sus parámetros
    mission_items.append(MissionItem(lat_home, #Latitud del waypoint en grados
                                     lon_home,  #Longitud del waypoint en grados
                                     2,  #Altitud relativa en metros
                                     0.5,  #Velocidad de salida del waypoint en m/s
                                     False, #Detención del dron en cada waypoint
                                     float('nan'), #Inclinación del cardán
                                     float('nan'), #Orientación del cardán
                                     MissionItem.CameraAction.TAKE_PHOTO, #Disparo de cámara en el waypoint
                                     1, #Tiempo de espera en el punto, en segundos
                                     float('nan'), #Radio para completar el waypoint, en metros
                                     float('nan'), #Orientación/rumbo del dron
                                     float('nan'))) #Intervalo de distancia en metros para el disparo de cámara tras salir del waypoint

    mission_items.append(MissionItem(num_lat,
                                     num_lon,
                                     2,
                                     0.5,
                                     False,
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.CameraAction.NONE,
                                     float('nan'),
                                     float('nan'),
                                     float('nan'),
                                     float('nan')))
    mission_items.append(MissionItem(lat_home,
                                     lon_home,
                                     2,
                                     0.5,
                                     False,
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.CameraAction.NONE,
                                     float('nan'),
                                     float('nan'),
                                     float('nan'),
                                     float('nan')))
    mission_items.append(MissionItem(lat_home,
                                     lon_home,
                                     3,
                                     0.5,
                                     False,
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.CameraAction.NONE,
                                     float('nan'),
                                     float('nan'),
                                     float('nan'),
                                     float('nan')))

    mission_items.append(MissionItem(num_lat,
                                     num_lon,
                                     3,
                                     0.5,
                                     False,
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.CameraAction.NONE,
                                     float('nan'),
                                     float('nan'),
                                     float('nan'),
                                     float('nan')))
    mission_items.append(MissionItem(lat_home,
                                     lon_home,
                                     3,
                                     0.5,
                                     False,
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.CameraAction.NONE,
                                     float('nan'),
                                     float('nan'),
                                     float('nan'),
                                     float('nan')))
    mission_items.append(MissionItem(lat_home,
                                     lon_home,
                                     4,
                                     0.5,
                                     False,
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.CameraAction.NONE,
                                     float('nan'),
                                     float('nan'),
                                     float('nan'),
                                     float('nan')))

    mission_items.append(MissionItem(num_lat,
                                     num_lon,
                                     4,
                                     0.5,
                                     False,
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.CameraAction.NONE,
                                     float('nan'),
                                     float('nan'),
                                     float('nan'),
                                     float('nan')))

    mission_items.append(MissionItem(lat_home,
                                     lon_home,
                                     4,
                                     0.5,
                                     False,
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.CameraAction.NONE,
                                     float('nan'),
                                     float('nan'),
                                     float('nan'),
                                     float('nan')))
    mission_plan = MissionPlan(mission_items)

    await drone.mission.set_return_to_launch_after_mission(True) #Activar modo retorno tras finalizar la misión

    print("-- Uploading mission")
    await drone.mission.upload_mission(mission_plan) #Cargar la misión en el dron

    print("-- Arming")
    await drone.action.arm() #Armar motores
    print("-- Starting mission")
    await drone.mission.start_mission() #Comenzar la misión
    await termination_task


async def print_mission_progress(drone): #Mostrar en pantalla el progreso de la misión
    async for mission_progress in drone.mission.mission_progress():
        print(f"Mission progress: "
              f"{mission_progress.current}/"
              f"{mission_progress.total}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
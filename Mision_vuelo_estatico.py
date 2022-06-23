#!/usr/bin/env python3

import asyncio
from mavsdk import System  #Importación de MAVSDK en el entorno


async def run():
    print("Inicio")
    drone = System()  #Creación de un sistema denominado drone
    await drone.connect(system_address="serial:///dev/ttyACM0")  #Dirección de conexión con el dron

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state(): #Bucle de espera hasta la conexión con el dron
        if state.is_connected:
            print(f"Drone discovered!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health(): #Bucle de espera hasta la geolocalización del dron
        if health.is_global_position_ok:
            print("Global position estimate ok")
            break

    print("-- Arming")
    await drone.action.arm()  #Armar motores

    print("-- Taking off")
    await drone.action.takeoff()   #Despegar según los parámetros de despegue automático

    await asyncio.sleep(300)  #Mantenerse en modo Holding durante el tiempo especificado (en s)

    print("-- Landing")
    await drone.action.land()  #Aterrizar según los parámetros de aterrizaje automático

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

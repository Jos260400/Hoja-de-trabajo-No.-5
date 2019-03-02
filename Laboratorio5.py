#Universidad del Valle de Guatemala
#Curso: Algoritmos y Estructuras de Datos
#Nombre: Fernando José Garavito Ovando	 Carné: 18071
#Nombre: Jose Gabriel Block Staackmann 	 Carné: 18935
#Hoja de Trabajo No. 5

import simpy
import random
from math import sqrt
from statistics import stdev
env = simpy.Environment()
cpu = simpy.Resource(env, capacity=1)#Cambiar el cpu de 1 a 2
ram = simpy.Container(env, capacity=100, init=100) # cambiar capacity e init a 200 para ram
listaTiempo = []
def proceso(env, cpu, ram, num_inst, num_ram):
	#	pedir ram
	print ("Numero de instruccion =",num_inst,"\n", "Ram Disponible =",num_ram,"\n","Ram Level =",ram.level,"\n")
	tiempo_inicial = env.now
	with ram.get(num_ram) as memoria:
		yield memoria

		while num_inst > 2:
			#	pedir cpu
			with cpu.request() as turno:
				yield turno
				#	esperar turno
				yield env.timeout(1)
				#	simular proceso
				num_inst = num_inst - 3

			#	devuelve cpu
			r = random.randint(1,2)
			if r == 2:
				#	simula operaciones I/O
				yield env.timeout(1)
	ram.put(num_ram)
	tiempo_final = env.now - tiempo_inicial
	listaTiempo.append(tiempo_final)
	print("Tiempo final=",tiempo_final,"\n")
	
	
	#	devolver ram al finzalizar proceso
proc = 25#cambiar de 25 a 50 a 100 a 200 para cada test 
def process_generator(env, cpu, ram):
    
    for i in range(proc):
        env.process(proceso(env, cpu, ram, random.randint(1, 10), random.randint(1, 10)))
        yield env.timeout(random.expovariate(1/1))
env.process(process_generator(env, cpu, ram))
env.run()
tiempoPromedio = sum(listaTiempo)/proc
print("El tiempo promedio es: ",tiempoPromedio)

desviación = stdev(listaTiempo)
print ("La desviación estándar es ", desviación)

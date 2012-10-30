#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sin título.py
#
#  Copyright 2012 Abraham Toriz Cruz <a.wonderful.code@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from time import time
from math import *
from pprint import pprint
from mysql_conn import Numbers_db

numbers = Numbers_db() #Se crea el enlace y esas cosas
agegados = 0

def t_convert(tiempo):
    """Convierte un tiempo en milisegundos a una hora legible"""
    if tiempo == float('inf'):
        return "un chingo"
    segs = int(tiempo)
    milis = int((tiempo-segs)*1000)
    min = [0, segs/60][segs>60]
    segs = segs%60
    horas = [0, min/60][min>60]
    min = min%60
    dias = [0, horas/24][horas>24]
    horas = horas%60
    s = ""
    if dias:
        s += "%d días "%dias
    if horas:
        s += "%d horas "%horas
    if min:
        s += "%d minutos "%min
    if segs:
        s += "%d segundos "%segs
    if milis:
        s += "%d milésimas"%milis
    if s:
        return s
    else:
        return "nada"

def inf(n = float('inf')):
    """iterador infinito"""
    i = 0
    while i<n:
        yield i
        i += 1

def is_prime(num):
    """Determina si el número dado es primo según una búsqueda en la
    base de datos"""
    for id, p in numbers.get_lower_than(sqrt(num)):
        if num%p == 0:
            break
    else: #Ningun primo lo dividio, es primo
        return True
    return False

def next_prime():
    """Encuentra el siguiente primo de la lista y lo añade a la base de
    datos"""
    id, num =  numbers.get_biggest()
    while True:
        num += 2
        if is_prime(num):#Es primo, lo imprimimos e insertamos en la base de datos
            #print num
            numbers.new(num)
            break

def seek_primes(how_many):
    """Función que se encarga de juntar más y más primos y añadirlos a
    la base de datos"""
    id, num =  numbers.get_biggest()
    global agregados
    agregados = 0
    for i in inf(how_many):
        if i == 0:
            ini = time()
        while True:
            num += 2
            if is_prime(num):#Es primo, lo imprimimos e insertamos en la base de datos
                numbers.new(num)
                break
        if i == 0:
            fin = time()
            print "Es probable que me tarde", t_convert((fin-ini)*how_many), "en hacer esto..."
        agregados += 1

def factor(num):
    """Factoriza el número dado"""
    factores = dict()
    for id, p in numbers.get_lower_than(num/2):
        while num%p==0:
            num = num/p
            if factores.has_key(p):
                factores[p] += 1
            else:
                factores.update({p:1})
    return factores

def n_format(num):
    """Da formato a un número para ser expuesto"""
    num = str(num)
    s = ""
    j = 0
    for i in xrange(len(num)):
        pos = len(num)-(i+1)
        s = num[pos] + s
        if j%3==2:
            s = ','+s
        j+=1
    if s.startswith(','):
        s = s[1:]
    return s

def human(fact, exp="^"):
    """Toma un diccionario de factores y lo hace legible"""
    s = ""
    for key in fact:
        s += "%d%s%d*"%(key, exp, fact[key])
    return s[:-1]

if __name__ == '__main__':
    op = raw_input("Desea?\n\tcalcular numeros [C],\n\tfactorizar un numero[F],\n\tver las estadísticas[E]\nopcion: ")
    op = op.lower()
    if op=='c':
        n_primes = raw_input("Cuántos primos nuevos quieres? ")
        if n_primes == 'inf':
            n_primes = float('inf')
        else:
            n_primes = int(n_primes)
        ini = time()
        try:
            seek_primes(n_primes)
        except KeyboardInterrupt:
            print "ok, terminamos antes..."
        end = time()
        print "Agregados", agregados, "en", t_convert(end-ini)
        id, num = numbers.get_biggest()
        print "El mas grande es ", n_format(num), "con el indice", n_format(id), "de", n_format(len(str(num))), "cifras"
    elif op == 'e':#ver las estadísticas
        ini = time()
        next_prime()
        fin = time()
        id, num = numbers.get_biggest()
        print "El número primo más grande calculado es", n_format(num), "con el índice", n_format(id)
        print "El número máximo que puedo factorizar con presición es", n_format(num*2)
        print "El número más grande del que puedo determinar primalidad es", n_format(num**2)
        print "Me toma", t_convert(fin-ini), "calcular un primo"
    elif op == 'f':
        id, num = numbers.get_biggest()
        print "Recuerda que el número más grande que puedo factorizar es", n_format(num*2)
        num = input("Numero a factorizar: ")
        ini = time()
        print "Los factores de", num, "son", human(factor(num), '**')
        fin = time()
        print "Me tomó", t_convert(fin-ini), "hacer esta factorización"
    elif op=='t': #test
        print t_convert(input("Numero: "))
    else:
        print "Nada que hacer.."


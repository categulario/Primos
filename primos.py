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
from util import t_convert, n_format

#Preparativos
numbers = Numbers_db() #Se crea el enlace y esas cosas
agegados = 0

print "cargando lista de primos..."
ini = time()
primos = [num for id, num in numbers.get_all()]
fin = time()
id, num = numbers.get_biggest()
print "me ha tomado", t_convert(fin-ini), "cargar la lista de primos con", n_format(id), "numeros"
del ini
del fin

def inf(n = float('inf')):
    """iterador infinito"""
    i = 0
    while i<n:
        yield i
        i += 1

def is_prime(num):
    """Determina si el número dado es primo según una búsqueda en la
    base de datos"""
    prime = True
    for p in primos:
        if num%p == 0:
            prime = False
            break
        if p>sqrt(num):
            break
    if prime:
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
            if is_prime(num):#Es primo, lo insertamos en la base de datos
                numbers.new(num)
                break
        if i == 0:
            fin = time()
            print "Es probable que me tarde", t_convert((fin-ini)*how_many), "en hacer esto..."
        agregados += 1

def factor(num):
    """Factoriza el número dado"""
    factores = dict()
    for id, p in numbers.get_lower_than(num):
        while num%p==0:
            num = num/p
            if factores.has_key(p):
                factores[p] += 1
            else:
                factores.update({p:1})
    return factores

def human(fact, exp="^"):
    """Toma un diccionario de factores y lo hace legible"""
    s = ""
    for key in fact:
        s += "%d%s%d*"%(key, exp, fact[key])
    return s[:-1]

if __name__ == '__main__':
    while True:
        op = raw_input("Desea?\n\tcalcular numeros [C],\n\tfactorizar un numero[F],\n\tver las estadísticas[E],\n\tSalir[Q]\nopcion: ")
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
            print is_prime(input("Numero: "))
        elif op=='q':
            break
        else:
            print "nada que hacer"


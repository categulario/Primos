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

from math import *
from pprint import pprint
from mysql_conn import Numbers_db

numbers = Numbers_db('numbers_copy') #Se crea el enlace y esas cosas

def inf(n = float('inf'), begin=0, step=1):
    """iterador infinito"""
    i = begin
    while i<n:
        yield i
        i += step

def is_prime(num):
    """Determina si el número dado es primo según una búsqueda en la
    base de datos"""
    for p in inf(sqrt(num), 2):
        if num%p == 0:
            break
    else: #Ningun primo lo dividio, es primo
        return True
    return False

def seek_primes(how_many):
    """Función que se encarga de juntar más y más primos y añadirlos a
    la base de datos"""
    id, num =  numbers.get_biggest()
    for i in inf(how_many):
        num += 2
        if is_prime(num):#Es primo, lo imprimimos e insertamos en la base de datos
            numbers.new(num)

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
    seek_primes(float('inf'))
    #num = 987455581
    #print num, is_prime(num), human(factor(num))
    #num = 1245887
    #print num, is_prime(num), human(factor(num))
    #num = 2105449
    #print num, is_prime(num), human(factor(num))


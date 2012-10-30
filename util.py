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

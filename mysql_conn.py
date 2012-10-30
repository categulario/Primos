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

"""
Aquí se deben hacer sencillas las interacciones con la base de datos
de números primos
"""

import MySQLdb

class Numbers_db(object):
    """clase con acceso a la base de datos de números"""
    def __init__(self, table='numbers'):
        """Crea la conexión"""
        data = {
            'host'  :'localhost',
            'user'  :'root',
            'passwd':'mai5ql',
            'db'    :'numbers'
        }
        self.db=MySQLdb.connect(
            host=data['host'],
            user=data['user'],
            passwd=data['passwd'],
            db=data['db']
        )
        self.table = table
        self.get_query = "SELECT id, number FROM "+self.table+";"
        self.get_biggest_query = "SELECT id, number FROM "+self.table+" ORDER BY id DESC LIMIT 1;"
        self.get_lower_than_query = "SELECT id, number FROM "+self.table+" WHERE number <= %d;"
        self.new_query = "INSERT INTO "+self.table+" (number) VALUES (%d);"
        self.num_rows = 0
        self.cursor = self.db.cursor()

    def get_all(self):
        """Obtiene el cursor"""
        self.num_rows = self.cursor.execute(self.get_query)
        return self.cursor #Ahora puedes iterar sobre el cursor

    def get_biggest(self):
        """Obtiene el número primo más grande encontrado"""
        self.num_rows = self.cursor.execute(self.get_biggest_query)
        resultado = self.cursor.fetchone()
        return resultado

    def get_lower_than(self, n):
        """Hace una búsqueda de los números primos menores que n"""
        self.num_rows = self.cursor.execute(self.get_lower_than_query%n)
        return self.cursor

    def new(self, n):
        """Inserta un nuevo número primo en la base de datos"""
        self.cursor.execute(self.new_query%n)
        self.db.commit()


if __name__ == "__main__":
    n = Numbers_db()
    cursor = n.get()
    for registro in cursor:
        print registro

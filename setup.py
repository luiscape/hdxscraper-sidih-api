#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(dir, 'code'))

import scraperwiki
from utilities.prompt_format import item

def CreateTables():
  '''Creating the tables of the new database.'''

  #
  # Dictionty of SQL squemas.
  #
  sql_statements = {
    'sidih_values': 'CREATE TABLE IF NOT EXISTS sidih_values(ID_VALDA TEXT, FIN_VALDA TEXT, INI_VALDA TEXT, ID_DATO TEXT, ID_UNIDAD TEXT, ID_MUN TEXT, VAL_VALDA TEXT, ID_DEPTO TEXT)'
  }

  #
  # Create all tables from a loop.
  #
  for table in sql_statements:
    try:
      query = scraperwiki.sqlite.execute(sql_statements[table])
      print "%s Table `%s` created." % (item('prompt_bullet'), str(table))

    except Exception as e:
      print e
      return False


  print "%s Database created successfully.\n" % item('prompt_success')
  return True


if __name__ == '__main__':
  CreateTables()
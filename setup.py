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
  # Creating tables for all the indicators.
  #
  indicators = [642, 653, 654, 593, 587, 3, 190, 504, 495, 343, 322, 337, 545, 384, 664, 645, 541, 540, 684, 588, 'all_data']
  sql_statements = {
    'sidih_values': 'CREATE TABLE IF NOT EXISTS sidih_values(ID_VALDA TEXT, FIN_VALDA TEXT, INI_VALDA TEXT, ID_DATO TEXT, ID_UNIDAD TEXT, ID_MUN TEXT, VAL_VALDA TEXT, ID_DEPTO TEXT)'
  }

  #
  # Create all tables from a loop.
  #
  for indicator in indicators:
    try:
      query_string = 'CREATE TABLE IF NOT EXISTS sidih_' + str(indicator) + '(ID_VALDA TEXT, FIN_VALDA TEXT, INI_VALDA TEXT, ID_DATO TEXT, ID_UNIDAD TEXT, ID_MUN TEXT, VAL_VALDA TEXT, ID_DEPTO TEXT)'
      query = scraperwiki.sqlite.execute(query_string)
      print "%s Table `sidih_%s` created." % (item('prompt_bullet'), str(indicator))

    except Exception as e:
      print e
      return False


  print "%s Database created successfully.\n" % item('prompt_success')
  return True


if __name__ == '__main__':
  CreateTables()
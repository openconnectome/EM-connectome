# Copyright 2014 Open Connectome Project (http://openconnecto.me)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import cStringIO
import zlib
import MySQLdb
import re
from collections import defaultdict
import itertools

import logging
logger=logging.getLogger("ocp")


"""Helpers function to do cube I/O in across multiple DBs.
    This uses the state and methods of ocpcadb"""

class MySQLKVIO:

  def __init__ ( self, db ):
    """Connect to the database"""

    self.db = db
    self.conn = None

    # Connection info 
    try:
      self.conn = MySQLdb.connect (host = self.db.annoproj.getDBHost(),
                            user = self.db.annoproj.getDBUser(),
                            passwd = self.db.annoproj.getDBPasswd(),
                            db = self.db.annoproj.getDBName())

    except MySQLdb.Error, e:
      self.conn = None
      logger.error("Failed to connect to database: %s, %s" % (db.annoproj.getDBHost(), db.annoproj.getDBName()))
      raise

    # start with no cursor
    self.txncursor = None

  def close ( self ):
    """Close the connection"""
    if self.conn:
      self.conn.close()

  def startTxn ( self ):
    """Start a transaction.  Ensure database is in multi-statement mode."""

    self.txncursor = self.conn.cursor()
    sql = "START TRANSACTION"
    self.txncursor.execute ( sql )

  def commit ( self ):
    """Commit the transaction.  Moved out of del to make explicit.""" 
    if self.txncursor:
      self.conn.commit()
      self.txncursor.close()
      self.txncursor = None

  def rollback ( self ):
    """Rollback the transaction.  To be called on exceptions."""

    if self.txncursor:
      self.conn.rollback()
      self.txncursor.close()
      self.txncursor = None

  def getCube ( self, zidx, resolution, update ):
    """Retrieve a cube from the database by token, resolution, and zidx"""

    # if in a TxN us the transaction cursor.  Otherwise create one.
    if self.txncursor == None:
      cursor = self.conn.cursor()
    else:
      cursor = self.txncursor

    sql = "SELECT cube FROM " + self.db.annoproj.getTable(resolution) + " WHERE zindex = " + str(zidx) 
    if update==True:
          sql += " FOR UPDATE"

    try:
      cursor.execute ( sql )
      row = cursor.fetchone()
    except MySQLdb.Error, e:
      logger.error ( "Failed to retrieve data cube: %d: %s. sql=%s" % (e.args[0], e.args[1], sql))
      raise
    finally:
      # close the local cursor if not in a transaction
      if self.txncursor == None:
        cursor.close()

    # If we can't find a cube, assume it hasn't been written yet
    if ( row == None ):
      return None
    else: 
      return row[0]

  
  def getChannelCube ( self, zidx, channel, resolution, update ):
    """Retrieve a cube from the Channel database by token, resolution, channel and zidx"""

    # if in a TxN us the transaction cursor.  Otherwise create one.
    if self.txncursor == None:
      cursor = self.conn.cursor()
    else:
      cursor = self.txncursor

    sql = "SELECT cube FROM {} WHERE (channel,zindex) = ({},{})".format( self.db.annoproj.getTable(resolution), channel, zidx )
    if update==True:
          sql += " FOR UPDATE"

    try:
      cursor.execute ( sql )
      row = cursor.fetchone()
    except MySQLdb.Error, e:
      logger.error ( "Failed to retrieve data cube: {}: {}. sql={}".format(e.args[0], e.args[1], sql) )
      raise
    finally:
      # close the local cursor if not in a transaction
      if self.txncursor == None:
        cursor.close()

    # If we can't find a cube, assume it hasn't been written yet
    if ( row == None ):
      return None
    else: 
      return row[0]

  
  def getTimeSeriesCube ( self, zidx, timestamp, resolution, update ):
    """Retrieve a cube from the TimeSeries database by token, resolution, timestamp and zidx"""

    # if in a TxN us the transaction cursor.  Otherwise create one.
    if self.txncursor == None:
      cursor = self.conn.cursor()
    else:
      cursor = self.txncursor

    sql = "SELECT cube FROM {} WHERE (zindex,timestamp) = ({},{})".format( self.db.annoproj.getTable(resolution), zidx, timestamp )
    if update==True:
          sql += " FOR UPDATE"

    try:
      cursor.execute ( sql )
      row = cursor.fetchone()
    except MySQLdb.Error, e:
      logger.error ( "Failed to retrieve data cube: {}: {}. sql={}".format(e.args[0], e.args[1], sql) )
      raise
    finally:
      # close the local cursor if not in a transaction
      if self.txncursor == None:
        cursor.close()

    # If we can't find a cube, assume it hasn't been written yet
    if ( row == None ):
      return None
    else: 
      return row[0]
  
  
  def getCubes ( self, listofidxs, resolution ):

    # if in a TxN us the transaction cursor.  Otherwise create one.
    if self.txncursor == None:
      cursor = self.conn.cursor()
    else:
      cursor = self.txncursor

    # RBTODO need to fix this for neariso interfaces
    sql = "SELECT zindex, cube FROM {} WHERE zindex in (%s)".format( self.db.annoproj.getTable(resolution) ) 

    # creats a %s for each list element
    in_p=', '.join(map(lambda x: '%s', listofidxs))
    # replace the single %s with the in_p string
    sql = sql % in_p

    try:
      rc = cursor.execute(sql, listofidxs)
    
      # Get the objects and add to the cube
      while ( True ):
        try: 
          retval = cursor.fetchone() 
        except:
          break
        if retval != None:
          yield ( retval )
        else:
          return
 
    finally:
      # close the local cursor if not in a transaction
      if self.txncursor == None:
        cursor.close()


  def getChannelCubes ( self, listofidxs, channel, resolution ):

    # if in a TxN us the transaction cursor.  Otherwise create one.
    if self.txncursor == None:
      cursor = self.conn.cursor()
    else:
      cursor = self.txncursor

    # RBTODO need to fix this for neariso interfaces
    sql = "SELECT zindex, cube FROM {} WHERE channel={} and zindex in (%s)".format( self.db.annoproj.getTable(resolution), channel )

    # creats a %s for each list element
    in_p=', '.join(map(lambda x: '%s', listofidxs))
    # replace the single %s with the in_p string
    sql = sql % in_p

    try:
      rc = cursor.execute(sql, listofidxs)
    
      # Get the objects and add to the cube
      while ( True ):
        try: 
          retval = cursor.fetchone() 
        except:
          break
        if retval != None:
          yield ( retval )
        else:
          return
 
    finally:
      # close the local cursor if not in a transaction
      if self.txncursor == None:
        cursor.close()


  def getTimeSeriesCubes ( self, listofidxs, timestamp, resolution ):

    # if in a TxN us the transaction cursor.  Otherwise create one.
    if self.txncursor == None:
      cursor = self.conn.cursor()
    else:
      cursor = self.txncursor

    # RBTODO need to fix this for neariso interfaces
    sql = "SELECT zindex, cube FROM {} WHERE timestamp={} and zindex in (%s)".format( self.db.annoproj.getTable(resolution), timestamp )

    # creats a %s for each list element
    in_p=', '.join(map(lambda x: '%s', listofidxs))
    # replace the single %s with the in_p string
    sql = sql % in_p

    try:
      rc = cursor.execute(sql, listofidxs)
    
      # Get the objects and add to the cube
      while ( True ):
        try: 
          retval = cursor.fetchone() 
        except:
          break
        if retval != None:
          yield ( retval )
        else:
          return
 
    finally:
      # close the local cursor if not in a transaction
      if self.txncursor == None:
        cursor.close()
  
  
  def getTimeSeriesColumn ( self, idx, listoftimestamps, resolution ):

    # if in a TxN us the transaction cursor.  Otherwise create one.
    if self.txncursor == None:
      cursor = self.conn.cursor()
    else:
      cursor = self.txncursor

    # RBTODO need to fix this for neariso interfaces
    sql = "SELECT zindex, cube FROM {} WHERE zindex={} and timestamp in (%s)".format( self.db.annoproj.getTable(resolution), idx )

    # creats a %s for each list element
    in_p=', '.join(map(lambda x: '%s', listoftimestamps))
    # replace the single %s with the in_p string
    sql = sql % in_p

    try:
      rc = cursor.execute(sql, listoftimestamps)
    
      # Get the objects and add to the cube
      while ( True ):
        try: 
          retval = cursor.fetchone() 
        except:
          break
        if retval != None:
          yield ( retval )
        else:
          return
 
    finally:
      # close the local cursor if not in a transaction
      if self.txncursor == None:
        cursor.close()
  
  
  #
  # putCube
  #
  def putCube ( self, zidx, resolution, cubestr, update=False ):
    """Store a cube from the annotation database"""

    # if in a TxN us the transaction cursor.  Otherwise create one.
    if self.txncursor == None:
      cursor = self.conn.cursor()
    else:
      cursor = self.txncursor

    # we created a cube from zeros
    if not update:

      sql = "INSERT INTO " + self.db.annoproj.getTable(resolution) +  "(zindex, cube) VALUES (%s, %s)"

      # this uses a cursor defined in the caller (locking context): not beautiful, but needed for locking
      try:
        cursor.execute ( sql, (zidx,cubestr))
      except MySQLdb.Error, e:
        logger.error ( "Error inserting cube: %d: %s. sql=%s" % (e.args[0], e.args[1], sql))
        raise
      finally:
        # close the local cursor if not in a transaction
        # and commit right away
        if self.txncursor == None:
          cursor.close()

    else:

      sql = "UPDATE " + self.db.annoproj.getTable(resolution) + " SET cube=(%s) WHERE zindex=" + str(zidx)
      try:
        cursor.execute ( sql, (cubestr))
      except MySQLdb.Error, e:
        logger.error ( "Error updating data cube: %d: %s. sql=%s" % (e.args[0], e.args[1], sql))
        raise
      finally:
        # close the local cursor if not in a transaction
        # and commit right away
        if self.txncursor == None:
          cursor.close()

    # commit if not in a txn
    if self.txncursor == None:
      self.conn.commit()


  #
  # putChannel
  #
  def putChannel ( self, channelstr, channelid ):
    """ Store a channel in the channels database """

    # if in a TxN us the transaction cursor.  Otherwise create one.
    if self.txncursor == None:
      cursor = self.conn.cursor()
    else:
      cursor = self.txncursor

    sql = "INSERT INTO channels (chanstr,chanid) VALUES (%s,%s)"

    # this uses a cursor defined in the caller (locking context): not beautiful, but needed for locking
    try:
      cursor.execute ( sql, (channelstr, str(channelid)) )
    except MySQLdb.Error, e:
      logger.error ( "Error inserting cube: {}: {}. sql={}".format(e.args[0], e.args[1], sql))
      raise
    finally:
      # close the local cursor if not in a transaction
      # and commit right away
      if self.txncursor == None:
        cursor.close()
  
    # commit if not in a txn
    if self.txncursor == None:
      self.conn.commit()

  #
  # putChannelCube
  #
  def putChannelCube ( self, zidx, channel, resolution, cubestr, update=False ):
    """ Store a cube from the channel database """

    # if in a TxN us the transaction cursor.  Otherwise create one.
    if self.txncursor == None:
      cursor = self.conn.cursor()
    else:
      cursor = self.txncursor

    # we created a cube from zeros
    if not update:

      sql = "INSERT INTO {} (channel, zindex, cube) VALUES (%s, %s, %s)".format( self.db.annoproj.getTable(resolution) )

      # this uses a cursor defined in the caller (locking context): not beautiful, but needed for locking
      try:
        cursor.execute ( sql, (channel,zidx,cubestr))
      except MySQLdb.Error, e:
        logger.error ( "Error inserting cube: {}: {}. sql={}".format(e.args[0], e.args[1], sql))
        raise
      finally:
        # close the local cursor if not in a transaction
        # and commit right away
        if self.txncursor == None:
          cursor.close()

    else:

      sql = "UPDATE {} SET cube=(%s) WHERE (channel,zindex)=({},{})".format( self.db.annoproj.getTable(resolution), channel, zidx )
      try:
        cursor.execute ( sql, (cubestr))
      except MySQLdb.Error, e:
        logger.error ( "Error updating data cube: {}: {}. sql={}".format(e.args[0], e.args[1], sql))
        raise
      finally:
        # close the local cursor if not in a transaction
        # and commit right away
        if self.txncursor == None:
          cursor.close()

    # commit if not in a txn
    if self.txncursor == None:
      self.conn.commit()

  #
  # putBatchCube
  #
  def putBatchCube ( self, zidx, resolution, cubestr, update=False ):
    """ Store a batch of cubes from the annotation database """

    # if in a TxN us the transaction cursor.  Otherwise create one.
    if self.txncursor == None:
      cursor = self.conn.cursor()
    else:
      cursor = self.txncursor

    # we created a cube from zeros
    if not update:

      sql = "INSERT INTO {} (zindex, cube) VALUES (%s, %s)".format( self.db.annoproj.getTable(resolution) )

      # this uses a cursor defined in the caller (locking context): not beautiful, but needed for locking
      try:
        cursor.executemany ( sql, zip(zidx,cubestr) )
      except MySQLdb.Error, e:
        logger.error ( "Error inserting cube: %d: %s. sql=%s" % (e.args[0], e.args[1], sql))
        raise
      finally:
        # close the local cursor if not in a transaction and commit right away
        if self.txncursor == None:
          cursor.close()

    else:

      sql = "UPDATE {} SET cube=(%s) WHERE zindex=".format( self.db.annoproj.getTable(resolution) )
      try:
        cursor.executemany ( sql, zip(zidx,cubestr) )
      except MySQLdb.Error, e:
        logger.error ( "Error updating data cube: %d: %s. sql=%s" % (e.args[0], e.args[1], sql))
        raise
      finally:
        # close the local cursor if not in a transaction and commit right away
        if self.txncursor == None:
          cursor.close()

    # commit if not in a txn
    if self.txncursor == None:
      self.conn.commit()


  def getIndex ( self, annid, resolution, update ):
    """MySQL fetch index routine"""

    # if in a TxN us the transaction cursor.  Otherwise create one.
    if self.txncursor == None:
      cursor = self.conn.cursor()
    else:
      cursor = self.txncursor

    #get the block from the database                                            
    sql = "SELECT cube FROM " + self.db.annoproj.getIdxTable(resolution) + " WHERE annid\
= " + str(annid) 
    if update==True:
      sql += " FOR UPDATE"
    try:
      cursor.execute ( sql )
      row = cursor.fetchone ()
    except MySQLdb.Error, e:
      logger.warning ("Failed to retrieve cube %d: %s. sql=%s" % (e.args[0], e.args[1], sql))
      raise
    except BaseException, e:
      logger.exception("Unknown exception")
      raise
    finally:
      # close the local cursor if not in a transaction
      if self.txncursor == None:
        cursor.close()
   
    # If we can't find a index, they don't exist                                
    if ( row == None ):
       return []
    else:
       return row[0]


  def putIndex ( self, zidx, resolution, indexstr, update ):
    """MySQL put index routine"""

    # if in a TxN us the transaction cursor.  Otherwise create one.
    if self.txncursor == None:
      cursor = self.conn.cursor()
    else:
      cursor = self.txncursor

    if not update:

      sql = "INSERT INTO " +  self.db.annoproj.getIdxTable(resolution)  +  "( annid, cube) VALUES ( %s, %s)"
      
      try:
         cursor.execute ( sql, (zidx, indexstr))
      except MySQLdb.Error, e:
         logger.warning("Error updating index %d: %s. sql=%s" % (e.args[0], e.args[1], sql))
         raise
      except BaseException, e:
         logger.exception("Unknown error when updating index")
         raise
      finally:
        # close the local cursor if not in a transaction
        if self.txncursor == None:
          cursor.close()

    else:

      #update index in the database
      sql = "UPDATE " + self.db.annoproj.getIdxTable(resolution) + " SET cube=(%s) WHERE annid=" + str(zidx)
      try:
         cursor.execute ( sql, (indexstr))
      except MySQLdb.Error, e:
         logger.warnig("Error updating exceptions %d: %s. sql=%s" % (e.args[0], e.args[1], sql))
         raise
      except:
        logger.exception("Unknown exception")
        raise
      finally:
        # close the local cursor if not in a transaction
        if self.txncursor == None:
          cursor.close()

    # commit if not in a txn
    if self.txncursor == None:
      self.conn.commit()


  def deleteIndex ( self, annid, resolution ):
    """MySQL update index routine"""

    # if in a TxN us the transaction cursor.  Otherwise create one.
    if self.txncursor == None:
      cursor = self.conn.cursor()
    else:
      cursor = self.txncursor

    sql = "DELETE FROM " +  self.db.annoproj.getIdxTable(resolution)  +  " WHERE annid=" + str(annid)
    
    try:
       cursor.execute ( sql )
    except MySQLdb.Error, e:
       logger.error("Error deleting the index %d: %s. sql=%s" % (e.args[0], e.args[1], sql))
       raise
    except:
      logger.exception("Unknown exception")
    finally:
      # close the local cursor if not in a transaction
      if self.txncursor == None:
        cursor.close()

    # commit if not in a txn
    if self.txncursor == None:
      self.conn.commit()


  #
  # getExceptions
  #
  def getExceptions ( self, zidx, resolution, annid ):
    """Load a the list of excpetions for this cube."""

    # if in a TxN us the transaction cursor.  Otherwise create one.
    if self.txncursor == None:
      cursor = self.conn.cursor()
    else:
      cursor = self.txncursor

    # get the block from the database
    sql = "SELECT exlist FROM %s where zindex=%s AND id=%s" % ( 'exc'+str(resolution), zidx, annid )
    try:
      cursor.execute ( sql )
      row = cursor.fetchone()
    except MySQLdb.Error, e:
      logger.error ( "Error reading exceptions %d: %s. sql=%s" % (e.args[0], e.args[1], sql))
      raise
    finally:
      # close the local cursor if not in a transaction
      if self.txncursor == None:
        cursor.close()

    # If we can't find a list of exceptions, they don't exist
    if ( row == None ):
      return []
    else: 
      return row[0] 

  #
  # deleteExceptions
  #
  def deleteExceptions ( self, zidx, resolution, annid ):
    """Delete a list of exceptions for this cuboid"""

    # if in a TxN us the transaction cursor.  Otherwise create one.
    if self.txncursor == None:
      cursor = self.conn.cursor()
    else:
      cursor = self.txncursor

    table = 'exc'+str(resolution)

    sql = "DELETE FROM " + table + " WHERE zindex = %s AND id = %s" 
    try:
      self.txncursor.execute ( sql, (zidx, annid))
    except MySQLdb.Error, e:
      logger.error ( "Error deleting exceptions %d: %s. sql=%s" % (e.args[0], e.args[1], sql))
      if self.txncursor == None:
        cursor.close()
      raise

    # commit if not in a txn
    if self.txncursor == None:
      self.conn.commit()
      cursor.close()


  #
  # putExceptions
  #
  def putExceptions ( self, zidx, resolution, annid, excstr, update=False ):
    """Store a list of exceptions"""
    """This should be done in a transaction"""

    # if in a TxN us the transaction cursor.  Otherwise create one.
    if self.txncursor == None:
      cursor = self.conn.cursor()
    else:
      cursor = self.txncursor

    table = 'exc'+str(resolution)

    if not update:

      sql = "INSERT INTO " + table + " (zindex, id, exlist) VALUES (%s, %s, %s)"
      try:
        cursor.execute ( sql, (zidx, annid, zlib.compress(excstr)))
      except MySQLdb.Error, e:
        logger.error ( "Error inserting exceptions %d: %s. sql=%s" % (e.args[0], e.args[1], sql))
        if self.txncursor == None:
          cursor.close()
        raise

    # In this case we have an update query
    else:

      sql = "UPDATE " + table + " SET exlist=(%s) WHERE zindex=%s AND id=%s" 
      try:
        cursor.execute ( sql, (zlib.compress(excstr),zidx,annid))
      except MySQLdb.Error, e:
        logger.error ( "Error updating exceptions %d: %s. sql=%s" % (e.args[0], e.args[1], sql))
        if self.txncursor == None:
          cursor.close()
        raise

    # commit if not in a txn
    if self.txncursor == None:
      self.conn.commit()
      cursor.close()


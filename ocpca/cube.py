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
import array
import cStringIO
from PIL import Image
import zlib

import zindex

import logging
logger=logging.getLogger("ocp")

#
#  AnnotateCube: manipulate the in-memory data representation of the 3-d cube of data
#    that contains annotations.  
#

class Cube:

  # Constructor 
  #
  #  Express cubesize in [ x,y,z ]
  def __init__(self, cubesize):
    """Create empty array of cubesize"""

    # cubesize is in z,y,x for interactions with tile/image data
    self.zdim, self.ydim, self.xdim = self.cubesize = [ cubesize[2],cubesize[1],cubesize[0] ]


  #
  #  addData -- from another cube to this cube
  #
  def addData ( self, other, index ):
    """Add data to a larger cube from a smaller cube"""

    xoffset = index[0]*other.xdim
    yoffset = index[1]*other.ydim
    zoffset = index[2]*other.zdim

    self.data [ zoffset:zoffset+other.zdim,\
                yoffset:yoffset+other.ydim,\
                xoffset:xoffset+other.xdim]\
            = other.data [:,:,:]

  #
  # Trim off the excess data
  #
  def trim ( self, xoffset, xsize, yoffset, ysize, zoffset, zsize ):
    """Trim off the excess data"""
    self.data = self.data [ zoffset:zoffset+zsize, yoffset:yoffset+ysize, xoffset:xoffset+xsize ]

  # load the object from a Numpy pickle
  def fromNPZ ( self, pandz ):
    """Load the cube from a pickled and zipped blob"""
    try:
      newstr = zlib.decompress ( pandz[:] )
      newfobj = cStringIO.StringIO ( newstr )
      self.data = np.load ( newfobj )
    except:
      logger.error ("Failed to decompress database cube.  Data integrity concern.")
      raise

    self._newcube = False


  # return a numpy pickle to be stored in the database
  def toNPZ ( self ):
    """Pickle and zip the object"""
    try:
      # Create the compressed cube
      fileobj = cStringIO.StringIO ()
      np.save ( fileobj, self.data )
      return  zlib.compress (fileobj.getvalue())
    except:
      logger.error ("Failed to compress database cube.  Data integrity concern.")
      raise



# end cube


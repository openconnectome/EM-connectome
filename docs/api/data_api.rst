Data API's
***********

HDF5 Service
============

POST
----

.. http:post:: (string:server_name)/ca/(string:token_name)/(string:channel_name)/hdf5/(int:resolution)/(int:min_x),(int:max_x)/(int:min_y),(int:max_y)/(int:min_z),(int:max_z)/(int:min_time),(int:max_time)/
   
   :synopsis: Post a HDF5 file to the server

   :param server_name: Server Name in OCP. In the general case this is ocp.me.
   :type server_name: string
   :param token_name: Token Name in OCP.
   :type token_name: string
   :param channel_name: Channel Name in OCP. *Optional*. If missing will use default channel for the token.
   :type channel_name: string
   :param resolution: Resolution for the data
   :type resolution: int
   :param min_x: Minimum value in the xrange
   :type min_x: int
   :param max_x: Maximum value in the xrange
   :type max_x: int
   :param min_y: Minimum value in the yrange
   :type min_y: int
   :param max_y: Maximum value in the yrange
   :type max_y: int
   :param min_z: Minimum value in the zrange
   :type min_z: int
   :param max_z: Maximum value in the zrange
   :type max_z: int
   :param min_time: Minimum value in the timerange. *Optional*. Only used for timeseries channels.
   :type min_time: int
   :param max_time: Maximum value in the timerange. *Optional*. Only used for timeseries channels.
   :type max_time: int
    
   :form CUTOUT: HDF5 group, Post data
   :form CHANNELTYPE: HDF5 group, Channel type(image, annotation, probmap, timeseries)
   :form DATATYPE: HDF5 group, Data type(uint8, uint16, uint32, rgb32, rgb64, float32)

   :statuscode 200: No error
   :statuscode 404: Error in the syntax or file format

.. gist:: https://gist.github.com/kunallillaney/19b78e5a83611edf7808


GET
----

.. http:get:: (string:server_name)/ca/(string:token_name)/(string:channel_name)/hdf5/(int:resolution)/(int:min_x),(int:max_x)/(int:min_y),(int:max_y)/(int:min_z),(int:max_z)/(int:min_time),(int:max_time)/
   
   :synopsis: Get a HDF5 file from the server

   :param server_name: Server Name in OCP. In the general case this is ocp.me.
   :type server_name: string
   :param token_name: Token Name in OCP.
   :type token_name: string
   :param channel_name: Channel Name in OCP. *Optional*. If missing will use default channel for the token.
   :type channel_name: string
   :param resolution: Resolution for the data
   :type resolution: int
   :param min_x: Minimum value in the xrange
   :type min_x: int
   :param max_x: Maximum value in the xrange
   :type max_x: int
   :param min_y: Minimum value in the yrange
   :type min_y: int
   :param max_y: Maximum value in the yrange
   :type max_y: int
   :param min_z: Minimum value in the zrange
   :type min_z: int
   :param max_z: Maximum value in the zrange
   :type max_z: int
   :param min_time: Minimum value in the timerange. *Optional*. Only used for timeseries channels.
   :type min_time: int
   :param max_time: Maximum value in the timerange. *Optional*. Only used for timeseries channels.
   :type max_time: int
    
   :form CUTOUT: HDF5 group, Post data
   :form CHANNELTYPE: HDF5 group, Channel type(image, annotation, probmap, timeseries)
   :form DATATYPE: HDF5 group, Data type(uint8, uint16, uint32, rgb32, rgb64, float32)

   :statuscode 200: No error
   :statuscode 404: Error in the syntax or file format
  
.. gist:: https://gist.github.com/kunallillaney/19b78e5a83611edf7808

Numpy Service
=============

POST
----

.. http:post:: (string:server_name)/ca/(string:token_name)/(string:channel_name)/npz/(int:resolution)/(int:min_x),(int:max_x)/(int:min_y),(int:max_y)/(int:min_z),(int:max_z)/(int:min_time),(int:max_time)/
   
   :synopsis: Post a Numpy file to the server

   :param server_name: Server Name in OCP. In the general case this is ocp.me.
   :type server_name: string
   :param token_name: Token Name in OCP.
   :type token_name: string
   :param channel_name: Channel Name in OCP. *Optional*. If missing will use default channel for the token.
   :type channel_name: string
   :param resolution: Resolution for the data
   :type resolution: int
   :param min_x: Minimum value in the xrange
   :type min_x: int
   :param max_x: Maximum value in the xrange
   :type max_x: int
   :param min_y: Minimum value in the yrange
   :type min_y: int
   :param max_y: Maximum value in the yrange
   :type max_y: int
   :param min_z: Minimum value in the zrange
   :type min_z: int
   :param max_z: Maximum value in the zrange
   :type max_z: int
   :param min_time: Minimum value in the timerange. *Optional*. Only used for timeseries channels.
   :type min_time: int
   :param max_time: Maximum value in the timerange. *Optional*. Only used for timeseries channels.
   :type max_time: int
    
   :form DATA: Numpy Array

   :statuscode 200: No error
   :statuscode 404: Error in the syntax or file format

.. gist:: https://gist.github.com/kunallillaney/19b78e5a83611edf7808


GET
----

.. http:get:: (string:server_name)/ca/(string:token_name)/(string:channel_name)/npz/(int:resolution)/(int:min_x),(int:max_x)/(int:min_y),(int:max_y)/(int:min_z),(int:max_z)/(int:min_time),(int:max_time)/
   
   :synopsis: Get a Numpy file from the server

   :param server_name: Server Name in OCP. In the general case this is ocp.me.
   :type server_name: string
   :param token_name: Token Name in OCP.
   :type token_name: string
   :param channel_name: Channel Name in OCP. *Optional*. If missing will use default channel for the token.
   :type channel_name: string
   :param resolution: Resolution for the data
   :type resolution: int
   :param min_x: Minimum value in the xrange
   :type min_x: int
   :param max_x: Maximum value in the xrange
   :type max_x: int
   :param min_y: Minimum value in the yrange
   :type min_y: int
   :param max_y: Maximum value in the yrange
   :type max_y: int
   :param min_z: Minimum value in the zrange
   :type min_z: int
   :param max_z: Maximum value in the zrange
   :type max_z: int
   :param min_time: Minimum value in the timerange. *Optional*. Only used for timeseries channels.
   :type min_time: int
   :param max_time: Maximum value in the timerange. *Optional*. Only used for timeseries channels.
   :type max_time: int
    
   :form DATA: Numpy Array

   :statuscode 200: No error
   :statuscode 404: Error in the syntax or file format
  
.. gist:: https://gist.github.com/kunallillaney/19b78e5a83611edf7808


Image Slice Service
===================

GET XY Slice Cutout
-------------------

.. http:get:: (string:server_name)/ca/(string:token_name)/(string:channel_name)/xy/(int:resolution)/(int:min_x),(int:max_x)/(int:min_y),(int:max_y)/(int:z_slice)/(int:time_slice)/
   
   :synopsis: Get a XY Slice Cutout

   :param server_name: Server Name in OCP. In the general case this is ocp.me.
   :type server_name: string
   :param token_name: Token Name in OCP.
   :type token_name: string
   :param channel_name: Channel Name in OCP. *Optional*. If missing will use default channel for the token.
   :type channel_name: string
   :param resolution: Resolution for the data
   :type resolution: int
   :param min_x: Minimum value in the xrange
   :type min_x: int
   :param max_x: Maximum value in the xrange
   :type max_x: int
   :param min_y: Minimum value in the yrange
   :type min_y: int
   :param max_y: Maximum value in the yrange
   :type max_y: int
   :param z_slice: Z-slice value
   :type z_slice: int
   :param time_slice: Minimum value in the timerange. *Optional*. Only used for timeseries channels.
   :type time_slice: int
    
   :statuscode 200: No error
   :statuscode 404: Error in the syntax or file format

.. gist:: https://gist.github.com/19b78e5a83611edf7808.git


GET XZ Slice Cutout
-------------------

.. http:get:: (string:server_name)/ca/(string:token_name)/(string:channel_name)/xz/(int:resolution)/(int:min_x),(int:max_x)/(int:y_slice)/(int:min_z),(int:max_z)/(int:time_slice/
   
   :synopsis: Get a HDF5 file from the server

   :param server_name: Server Name in OCP. In the general case this is ocp.me.
   :type server_name: string
   :param token_name: Token Name in OCP.
   :type token_name: string
   :param channel_name: Channel Name in OCP. *Optional*. If missing will use default channel for the token.
   :type channel_name: string
   :param resolution: Resolution for the data
   :type resolution: int
   :param min_x: Minimum value in the xrange
   :type min_x: int
   :param max_x: Maximum value in the xrange
   :type max_x: int
   :param y_slice: Y-slice value
   :type y_slice: int
   :param min_z: Minimum value in the zrange
   :type min_z: int
   :param max_z: Maximum value in the zrange
   :type max_z: int
   :param time_slice: Minimum value in the timerange. *Optional*. Only used for timeseries channels.
   :type time_slice: int

   :statuscode 200: No error
   :statuscode 404: Error in the syntax or file format

GET YZ Slice Cutout
-------------------

.. http:get:: (string:server_name)/ca/(string:token_name)/(string:channel_name)/yz/(int:resolution)/(int:x_slice)/(int:min_y),(int:max_y)/(int:min_z),(int:max_z)/(int:time_slice)/
   
   :synopsis: Get a HDF5 file from the server

   :param server_name: Server Name in OCP. In the general case this is ocp.me.
   :type server_name: string
   :param token_name: Token Name in OCP.
   :type token_name: string
   :param channel_name: Channel Name in OCP. *Optional*. If missing will use default channel for the token.
   :type channel_name: string
   :param resolution: Resolution for the data
   :type resolution: int
   :param x_slice: X-slice value
   :type x_slice: int
   :param min_y: Minimum value in the yrange
   :type min_y: int
   :param max_y: Maximum value in the yrange
   :type max_y: int
   :param min_z: Minimum value in the zrange
   :type min_z: int
   :param max_z: Maximum value in the zrange
   :type max_z: int
   :param min_time: Minimum value in the timerange. *Optional*. Only used for timeseries channels.
   :type min_time: int
   :param max_time: Maximum value in the timerange. *Optional*. Only used for timeseries channels.
   :type max_time: int
    
   :form CUTOUT: HDF5 group, Post data
   :form CHANNELTYPE: HDF5 group, Channel type(image, annotation, probmap, timeseries)
   :form DATATYPE: HDF5 group, Data type(uint8, uint16, uint32, rgb32, rgb64, float32)

   :statuscode 200: No error
   :statuscode 404: Error in the syntax or file format
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


import json
import argparse
import requests
import os
import requests
import autoingest
SITE_HOST = "http://openconnecto.me"

def main():

    ai = autoingest.AutoIngest()

    """
    Edit the below values, type and default information can be found on the ingesting page of the ndio docs page.
    """

    dataset_name=''        #(type=str, help='Name of Dataset')
    imagesize=(0,0,0)           #(type=int[], help='Image size (X,Y,Z)')
    voxelres=(0,0,0)            #(type=float[], help='Voxel resolution (X,Y,Z) - In nanometers')
    offset=(0,0,0)              #(type=int[], default=[0, 0, 0], help='Image Offset in X,Y,Z')
    timerange=(0,0)           #(type=int[], default=[0, 0], help='Time Dimensions')
    scalinglevels=0       #(type=int, default=0, help='Required Scaling levels/ Zoom out levels')
    scaling=0             #(type=int, default=0, help='Type of Scaling - Isotropic or Normal')

    channel_name=''        #(type=str, help='Name of Channel. Has to be unique in the same project. User Defined.')
    datatype=''            #(type=str, help='Channel Datatype')
    channel_type=''        #(type=str, help='Type of channel - Image, Annotation. Timeseries, Probability-Maps')
    exceptions=0          #(type=int, default=0, help='Exceptions')
    resolution=0          #(type=int, default=0, help='Start Resolution')
    windowrange=(0,0)         #(type=int[], default=[0, 0], help='Window clamp function for 16-bit channels with low max value of pixels')
    readonly=0            #(type=int, default=0, help='Read-only Channel or Not. You can remotely post to channel if it is not readonly and overwrite data')
    data_url= ''           #(type=str, help='This url points to the root directory of the files. Dropbox is not an acceptable HTTP Server.')
    file_format=''         #(type=str, help='This is overal the file format type. For now we support only Slice stacks and CATMAID tiles.')
    file_type=''           #(type=str, help='This is the specific file format type (tiff, tif, png))

    project_name=''        #(type=str, help='Name of Project. Has to be unique in OCP. User Defined')
    token_name=''          #(type=str, default='', help='Token Name. User Defined')
    public=0              #(type=int, default=0, help='Make your project publicly visible')

    metadata=""            #(type=Any, default='', help='Any metadata as appropriate from the LIMS schema')

    #Adds data set information
    ai.add_dataset(dataset_name, imagesize, voxelres, offset, timerange, scalinglevels, scaling)

    #Adds project information
    ai.add_project(project_name, token_name, public)

    #Adds a channel
    ai.add_channel(channel_name, datatype, channel_type, data_url, file_format, file_type, exceptions,
            resolution, windowrange, readonly)

    """
    If you wish to add additional channels to the object, simply call the
    add_channel function for as many channels as you have
    """

    #Adds metada
    ai.add_metadata(metadata)

    """
    EDIT ABOVE HERE
    """

    #Uncomment this line if you wish to get a json file names file_name
    #ai.output_json("ocp.json")

    #Post the data
    ai.post_data(SITE_HOST)

if __name__ == "__main__":
  main()
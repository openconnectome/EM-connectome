/*
* Copyright 2014 Open Connectome Project (http://openconnecto.me)
* 
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
* 
*     http://www.apache.org/licenses/LICENSE-2.0
* 
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/


/*
 * Annotate Dense Entity Function 
 * Naive implementation 
 */

#include<stdio.h>
#include<stdint.h>
#include<stdbool.h>
#include<stdlib.h>
#include<string.h>

void annotateEntityDense( uint32_t * data, int * dims, int entityid)
{
		int i,j,k,index;

    int xdim = dims[0];
    int ydim = dims[1];
    int zdim = dims[2];

		for ( i=0; i<xdim; i++ )
      for ( j=0; j<ydim; j++ )
        for ( k=0; k<zdim; k++ )
        {
          index = (i*zdim*ydim)+(j*zdim)+(k);
          if ( data[index] !=0 )
            data[index] = entityid;
        }
}
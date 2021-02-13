Map generator

This program creates a map with locations of films that are the nearest to 
the user's location and were directed in the year the user has given.

Module consists of six functions for reading data and generating map.
To begin with, program asks the user to enter the year of a film and 
the user's location. 

!!!Warning!!!
This programs works really long, but you can shorten the base with data
in filter_year() function. It consists of 1000 films of a given year 
by default, but you can change it.

The result is a map with three layers: the user's location, my location 
and films' locations. You can add and remove layers on the map using 
the layer control.

The example of a generated map:
![Map](generated_map.png?raw=true "output_map")

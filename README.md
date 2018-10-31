# Skylarkdrone_assignment
The code includes a total of 9 methods

get_value_images() - It reads the images from the folder and gets the details of all the images such as longitude ,latitude,altitude and their references
                      It then consist of two functions degree() and altit(). degree() converts the longitude and latitude into degrees while altit converts altitude into degree
                      The whole of image data is stored in image_data which contains image name as key and lon,lat,alt as values
 
 get_value_videos() -  It reads the srt file and gets the information.It stores the data in drone_loc which has time as key and lon,lat and alt as values.
 
 get_dist() - It calculates the distance between the drone_loc and images which are at 35 metres from the drone and stores it in csv35 .
 
 write_35m() - It writes the data into a csv file. The data includes time of drone and the image name which are 35 metres from it
 
 poi() - It reads the data from assets.csv and calculates the distance of images which are at 50m from poi using haversine formula.
 
 gen_kml()- It generates the kml file
 
 write_poi()-It writes the image name with its respective poi.
 
 haversine() - It calculates the distance between 2 location using altitude.
 
 Output file
 assets2.csv contain all the images which are at 50m from poi
 names.csv contain all the images which at 35m from deones
 drone_path contains the kml file
 
 
 

from PIL import Image
from math import cos, asin, sqrt, pi, radians, sin, inf,atan2
import csv
import simplekml
import os
latitude=list()
lat_ref=list()
longitude=list()
long_ref=list()
altitude=list()
alt_ref=list()
def degree(value):
        "get the value of latitude and longitude in degrees"
        deg = (value[0][0])/(value[0][1])
        min = (value[1][0])/(value[1][1])
        sec = (value[2][0])/(value[2][1])
        return( (deg + min/60 + sec/3600))
def altit(value):
    "get the value of altitude in degrees"
    return(value[0]/value[1])
imagesData = {}
def get_value_images():
    x = r"C:\Users\Eushkmu\Downloads\technical_assignment_software_developer_4\images"
    for entry in os.scandir(x):
        data = entry.name
        image=Image.open(x+"/"+entry.name)
        #print(entry.name)
        info=image._getexif()[0x8825]
        exif_data={}
        gps_latitude_ref = info[1]
        gps_latitude = info[2]
        gps_longitude_ref = info[3]
        gps_longitude = info[4]
        gps_altitude_ref = info[5]
        gps_altitude = info[6]
        lat_ref.append(gps_altitude_ref)
        long_ref.append(gps_longitude_ref)
        latit = degree(gps_latitude)
        if gps_latitude_ref != "N":
            latit = 0 - latit
        latitude.append(latit)

        longit = degree(gps_longitude)
        if gps_longitude_ref != "E":
            longit = 0 - longit
        longitude.append(longit)
        altitu = altit(gps_altitude)
        if ord(gps_altitude_ref) != 0:
            altitu = 0 - altitu
        altitude.append(altitu)
        imagesData[entry.name] = [longit, latit, altitu]
    return 0
time = 0
lat = list()
long = list()
alt = list()
drone_loc={}
def get_value_videos():
    "get the drone location with time in drone_loc"
    x = r"C:\Users\Eushkmu\Downloads\technical_assignment_software_developer_4\software_dev\videos"
    for entry in os.scandir(x):
        f = open(x + "/" + "DJI_0301.SRT", "r")
        t = list()
        time = 0
        for line in f:
            if line.strip():
                t.append(line)
        x = 0

        for item in t:
            x = x + 1
            if (x % 3 == 0):
                l1, l2, l3 = item.split(',')
                long.append((float)(l1))
                lat.append((float)(l2))
                alt.append((float)(l3))
                time += 1
                drone_loc[time]=[l1,l2,l3]




def haversine(lon1, lat1, lon2, lat2, alt1=0, alt2=0):
    "calculate the distance between two points"
    mean_earth_radius = 6371
    lon1, lat1, lon2, lat2 = map(radians, list(
        map(float, [lon1, lat1, lon2, lat2])))
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    dalt = (float)(alt2)
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a),sqrt(1-a))
    distance = mean_earth_radius * c * 1000
    distance = distance ** 2 + dalt ** 2
    return sqrt(distance)
csv35=[]
def get_dist():
    for every_drone_loc in drone_loc:
        img_35=[]
        for image_loc in imagesData:
            lon1,lat1,alt1=imagesData[image_loc]
            lon2,lat2,alt2=drone_loc[every_drone_loc]
            #print(alt2)
            dist=haversine(lon1, lat1, lon2, lat2, alt1, alt2)
            if(dist<35):
                img_35.append(image_loc)
       # print(img_35)
        csv35.append(img_35)
img=list()
def write_35m():
    with open('C:/Users/Eushkmu/Documents/names.csv', 'w') as csvfile:   #choose your own directory
       fieldname = ['Time', 'Images']
       writer = csv.DictWriter(csvfile, fieldnames=fieldname)
       writer.writeheader()
       t=0
       for get_images_per_second in csv35:
           t=t+1
           y=str(t)
           writer.writerow({'Time': y, 'Images': get_images_per_second})
csv_50=[]
lines=[]
def poi():
    with open("C:/Users/Eushkmu/Downloads/technical_assignment_software_developer_4/software_dev/assets.csv",'r') as csvfile: #choose your own directory
        line1=csvfile.readline()
        lines.append(line1)
        for line in csvfile:
            lines.append(line)
            name,lon,lat,img=line.split(',')
            img_50=[]
            for image_loc in imagesData:
                lon2,lat2,alt2=imagesData[image_loc]
                dist=haversine(lon,lat,lon2,lat2)
                if(dist<50):
                    img_50.append(image_loc)
            csv_50.append(img_50)
            #print(csv_50)
def write_poi():
    with open("C:/Users/Eushkmu/Downloads/technical_assignment_software_developer_4/software_dev/assets2.csv",'w') as csvfile2:
        p=0;
        fieldnames = ['asset_name', 'longitude', 'latitude', 'image_name']
        writer = csv.DictWriter(csvfile2, fieldnames=fieldnames)
        writer.writeheader()
        for images in csv_50:
            name,lon,lat,img=lines[p].split(',')
            p=p+1

            writer.writerow({'asset_name': name,'longitude':lon,'latitude':lat,'image_name':images})

def gen_kml():
    kml = simplekml.Kml()
    lineString = kml.newlinestring(name="Drone path")
    for every_drone_loc in drone_loc:
        lon, lat, alt = drone_loc[every_drone_loc]
        lineString.coords.addcoordinates([(lon, lat, alt)])
        try:
            kml.save('C:/Users/Eushkmu/Documents/drone_path.kml')
        except :
            print("Drone path was not created")
if __name__=="__main__":
    get_value_images()
    get_value_videos()
    get_dist()
    write_35m()
    poi()
    gen_kml()
    write_poi()
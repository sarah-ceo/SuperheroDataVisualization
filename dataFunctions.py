# -*- coding: utf-8 -*-
"""
Fichier permettant la récupération et le traitement des données

@author: Sarah CE-OUGNA
"""
import webbrowser
import urllib.request
import json
import csv
from collections import OrderedDict
import folium
import time

class Data():

    def __init__(self, download = False):
        self.fields = ["ID", "Name", "Full-Name", "Publisher", "Place of Birth",
                       "Intelligence", "Strength", "Speed", "Durability", "Power", "Combat", "Image"]
        if(download):
            try:
                self.getData()
            except:
                print("Une erreur s'est produite pendant le téléchargement des données...")
                print("Nous allons donc utiliser le fichier .csv pré-téléchargé")
                self.readFile()
        else:
            self.readFile()
            
        self.intelligence, self.strength, self.speed, self.durability, self.power, self.combat, self.total = [],[],[],[],[],[],[]
        self.geoRows =[]
        self.pre_html = """<html>
        <head>{NAME}</head>
        <body><p>{FULLNAME}</p>
        <p>{PUBLISHER}</p>
        <div><img src="{IMAGE}" style="max-height:100px;max-width:100px;"></div></body>
        </html>"""
        
        self.prepareData()
        
    def prepareData(self):
        self.retrieveData()
        self.eraseUnknownLocations()
        self.locatePlacesOfBirth()
        self.frequencies = {"Otherwordly": 0}
        for geoRow in self.geoRows:
            if(geoRow["Real Location"] == "YES"):
                if(geoRow["Country"] in self.frequencies.keys()):
                    self.frequencies[geoRow["Country"]] += 1
                else:
                    self.frequencies.update({geoRow["Country"]:1})
            else:
                self.frequencies["Otherwordly"] += 1
        
    def readFile(self):
        with open('data/preloaded/Superhero_data.csv','r') as f:
            reader = csv.DictReader(f, fieldnames=self.fields)
            self.rows = list(reader)

    ################################### RECUPERATION DES DONNEES ####################################
    def getData(self):
        proxy_address = 'http://147.215.1.189:3128/'
        proxy_handler = urllib.request.ProxyHandler({'http': proxy_address, 'https': proxy_address})
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)
            
        self.rows = []
        start = time.clock()
        #132, 173, 368 are None 
        print("Téléchargement : ")
        for i in range(1,132):
            self.requestData(str(i))
            print(str(i) +"/731")
        for i in range(133,173):
            self.requestData(str(i))
            print(str(i) +"/731")
        for i in range(174,368):
            self.requestData(str(i))
            print(str(i) +"/731")
        for i in range(369,732):
            self.requestData(str(i))
            print(str(i) +"/731")
        elapsed = time.clock()
        print ("Données récupérées ! Cela a pris:", (elapsed - start), "secondes, soit", (elapsed - start)/60, "minutes...")
            
    def requestData(self, heroID):
        u = urllib.request.urlopen('https://superheroapi.com/api.php/10215544482839651/'+heroID)
        dataRead = u.read()
        encoding = u.info().get_content_charset('utf-8')
        data = json.loads(dataRead.decode(encoding))
        oD = OrderedDict()
        oD["ID"] = data["id"]
        oD["Name"] = data['name']
        oD["Full-Name"] = data["biography"]["full-name"]
        oD["Publisher"] = data["biography"]["publisher"]
        oD["Place of Birth"] = data["biography"]["place-of-birth"]
        oD["Intelligence"] = data["powerstats"]["intelligence"]
        oD["Strength"] = data["powerstats"]["strength"]
        oD["Speed"] = data["powerstats"]["speed"]
        oD["Durability"] = data["powerstats"]["durability"]
        oD["Power"] = data["powerstats"]["power"]
        oD["Combat"] = data["powerstats"]["combat"]
        oD["Image"] = data["image"]["url"]
        self.rows.append(oD)

    ################################### AFFICHAGE DES HISTOGRAMMES ####################################

    def plotData(self, arg_figure):
        
        fig = arg_figure
        
        a = fig.add_subplot(331)
        self.makePlot(a, self.intelligence,"Intelligence")
        a.set_ylabel('Personnages')
        b = fig.add_subplot(332)
        self.makePlot(b, self.strength,"Force")
        c = fig.add_subplot(333)
        self.makePlot(c, self.speed,"Vitesse")
        d = fig.add_subplot(334)
        self.makePlot(d, self.durability,"Longévité")
        d.set_ylabel('Personnages')
        e = fig.add_subplot(335)
        self.makePlot(e, self.power,"Pouvoir")
        f = fig.add_subplot(336)
        self.makePlot(f, self.combat,"Combat")
        g = fig.add_subplot(338)
        self.makePlot(g, self.total,"Total")
        g.set_ylabel('Personnages')
        
        return fig
    
    def retrieveData(self):
        i = 0
        for row in self.rows:
            if i!=0 and ((row['Intelligence'] != "null") and (row['Strength'] != "null") and (row['Speed'] != "null") and 
                         (row['Durability'] != "null") and (row['Power'] != "null") and (row['Combat'] != "null")):
                self.intelligence.append(int(row["Intelligence"]))
                self.strength.append(int(row["Strength"]))
                self.speed.append(int(row["Speed"]))
                self.durability.append(int(row["Durability"]))
                self.power.append(int(row["Power"]))
                self.combat.append(int(row["Combat"]))
                self.total.append((int(row["Intelligence"])+int(row["Strength"])+int(row["Speed"])+int(row["Durability"])+int(row["Power"])+int(row["Combat"]))/6)
            i+=1
            
    def makePlot(self, subplot_index, theList, name):
        x = theList
        num_bins = 10
        subplot_index.hist(x, num_bins, facecolor='blue', alpha=0.5, edgecolor='black', linewidth=1.5)
        subplot_index.set_xlabel(name)
    
    ################################### PRE-TRAITEMENT GEOLOCALISATION ####################################

                                    # EFFACEMENT DES LIGNES AUX CHAMPS NON-IDENTIFIES
    def eraseUnknownLocations(self):
        nb_row = 0
        for row in self.rows:
            if (nb_row != 0):
                if( ("unknown".lower() in row['Place of Birth'].lower()) or ("Unrevealed".lower() in row['Place of Birth'].lower()) 
                or ("undisclosed".lower() in row['Place of Birth'].lower())):
                    row['Place of Birth'] = "-"
                if(row['Place of Birth'] != "-"):
                    oD = OrderedDict(row)
                    oD['Real Location'] = "-"
                    oD['City'] = "-"
                    oD['Country'] = "-"
                    oD['Latitude'] = "-"
                    oD['Longitude'] = "-"
                    self.geoRows.append(oD)
            nb_row +=1
        
    
                                        #RECUPERATION AUTOMATIQUE DES COORDONNEES
    def locatePlacesOfBirth(self):
        ## PAR VILLE (DES USA)
        with open('data/US_cities.json') as json_data:
            data = json.loads(json_data.read())
        for geoRow in self.geoRows:
            for city in reversed(data):
                if (city["city"].lower() in geoRow['Place of Birth'].lower()):
                    geoRow["Real Location"] = "YES"
                    geoRow["City"] = city["city"]
                    geoRow["Country"] = "United States"
                    geoRow["Latitude"] = city["latitude"]
                    geoRow["Longitude"] = city["longitude"]
        
        # PAR VILLES (MANUELLEMENT)
        with open('data/manual_coordinates.csv','r') as f:
            reader = csv.reader(f, delimiter=";")
            manualRows = list(reader)
            
        for geoRow in self.geoRows:
            for manualRow in manualRows:
                if ((geoRow["Real Location"] != "YES") and (str(manualRow[0]).lower() in geoRow['Place of Birth'].lower())):
                    geoRow["Real Location"] = "YES"
                    geoRow["City"] = manualRow[0]
                    geoRow["Country"] = manualRow[1]
                    geoRow["Latitude"] = manualRow[2]
                    geoRow["Longitude"] = manualRow[3]
            
        # RESTE
        for geoRow in self.geoRows:
            if(geoRow["Real Location"] == "-"):
                geoRow["Real Location"] = "NO"
                
    ################################### GEOLOCALISATION ####################################

    def individual_geolocalisation(self):
        coords = (48.8398094,2.5840685)
        map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=2)
        
        for geoRow in self.geoRows:
            if(geoRow["Real Location"] == "YES"):
                html = self.pre_html.format(NAME=geoRow["Name"], FULLNAME=geoRow["Full-Name"], PUBLISHER=geoRow["Publisher"], IMAGE=geoRow["Image"])
                iframe = folium.Html(html, script=True)
                popup  = folium.Popup(iframe, max_width=100)
                folium.CircleMarker(
                        location = (float(geoRow["Latitude"]), float(geoRow["Longitude"])),
                        radius = 10,
                        color = 'crimson',
                        fill = True,
                        fill_color = 'crimson',
                        popup = popup
                        ).add_to(map)
            
        map.save(outfile='map.html')
        webbrowser.open("map.html", new=1)
        
    def frequency_geolocalisation(self):
        coords = (48.8398094,2.5840685)
        map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=2)
    
        with open('data/Country_List.csv','r') as f:
            reader = csv.DictReader(f)
            countryRows = list(reader)
        
            for key,value in self.frequencies.items():
                for countryRow in countryRows:
                    if(key == countryRow["Country"]):
                        folium.CircleMarker(
                                location = (float(countryRow["Latitude (average)"]), float(countryRow["Longitude (average)"])),
                                radius = 0.2*value,
                                color = 'crimson',
                                fill = True,
                                fill_color = 'black',
                                popup = ("Nombre de personnages : "+str(value))
                                ).add_to(map)
    
            folium.CircleMarker(
                    location = (34.753975, -40.714643),
                    radius = 0.3*self.frequencies["Otherwordly"],
                    color = 'blue',
                    fill = True,
                    fill_color = 'black',
                    popup=("Personnages venant d'un autre monde ou d'une autre planète : "+str(self.frequencies["Otherwordly"]))
                    ).add_to(map)
                        
        map.save(outfile='map.html')
        webbrowser.open("map.html", new=1)
        
    def usa_geolocalisation(self):
        coords = (38,-97)
        map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=3)
        
        for geoRow in self.geoRows:
            if(geoRow["Real Location"] == "YES" and geoRow["Country"] == "United States"):
                html = self.pre_html.format(NAME=geoRow["Name"], FULLNAME=geoRow["Full-Name"], PUBLISHER=geoRow["Publisher"], IMAGE=geoRow["Image"])
                iframe = folium.Html(html, script=True)
                popup  = folium.Popup(iframe, max_width=100)
                folium.Marker(
                        location= (float(geoRow["Latitude"]),float(geoRow["Longitude"])),
                        popup = popup
                        ).add_to(map)
            
        map.save(outfile='map.html')
        webbrowser.open("map.html", new=1)
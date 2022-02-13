# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 18:53:08 2022

@author: Martin
"""

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pickle
import numpy

def make_soup(url):
    thepage=uReq(url)
    soupdata=soup(thepage,"html.parser")
    return soupdata


Liste0=[]
Months=['october','november','december','january','february','march',"april"]
Teams=['Brooklyn Nets','Milwaukee Bucks','Golden State Warriors','Los Angeles Lakers','Indiana Pacers','Charlotte Hornets','Chicago Bulls','Detroit Pistons','Boston Celtics','New York Knicks','Washington Wizards','Toronto Raptors','Cleveland Cavaliers','Memphis Grizzlies','Houston Rockets','Minnesota Timberwolves','Philadelphia 76ers','New Orleans Pelicans','Orlando Magic','San Antonio Spurs','Oklahoma City Thunder','Utah Jazz','Sacramento Kings','Portland Trail Blazers','Denver Nuggets','Phoenix Suns','Dallas Mavericks','Atlanta Hawks','Miami Heat','Los Angeles Clippers','New Orleans Hornets','Charlotte Bobcats','New Jersey Nets']
print(len(Teams))
year=['2015','2016','2017','2018','2019','2022']
#url2='https://www.basketball-reference.com/leagues/NBA_'+year+'+_games-'+Months[-1]+'.html'

arrayR,arrayG=[],[]
def Get_data(Score):
    l=[[0,0,0,0,0] for i in Teams]
    #Offense/Defense/Victory/NB Games/Victory or Defeat Streak
    
    listG=[]
    #List of data for each game
    listR=[]
    #List of result of each games
    #List of games with OFF-DEF for home, OFF-DEF for visitor, streak for home, streak for visitor, 1 if home win 0 else  
    
    miniG=40
    dict_data=dict(zip(Teams,l))
    compt=0
    while compt<len(Score)-2:
        if Score[compt] in Teams and Score[compt+1]!="" and dict_data[Score[compt]][3]<82:
            VT,HT=Score[compt],Score[compt+2]
            #Visitor Team and Home Team
            print(VT,end=" ")
            print(Score[compt+1],end=" ")
            print(HT,end=" ")
            print(Score[compt+3])
            G=[]
            sv,sh=int(Score[compt+1]),int(Score[compt+3])
            if dict_data[HT][3]>miniG and dict_data[VT][3]>miniG:
                avgWinh,avgWinv,avgOFF_h,avgDEF_h,avgOFF_v,avg_DEF_v=dict_data[HT][2]/dict_data[HT][3],dict_data[VT][2]/dict_data[VT][3],dict_data[HT][0]/dict_data[HT][3],dict_data[HT][1]/dict_data[HT][3],dict_data[VT][0]/dict_data[VT][3],dict_data[VT][1]/dict_data[VT][3]
                G=[avgWinh,avgWinv,avgOFF_h-avg_DEF_v,avgOFF_v-avgDEF_h]#,dict_data[HT][4],dict_data[VT][4]]
                if sv>sh:
                    listR.append(0)
                else:
                    listR.append(1)
                listG.append(G)
            dict_data[VT][3]+=1
            dict_data[HT][3]+=1
            
            #Score visitor/Score home
            
            
            
            dict_data[VT][0]+=sv
            dict_data[VT][1]+=sh
            dict_data[HT][0]+=sh
            dict_data[HT][1]+=sv
            if sv>sh:
                dict_data[VT][2]+=1
                if dict_data[VT][4]>=0:
                    dict_data[VT][4]+=1
                if dict_data[HT][4]<0:
                    dict_data[HT][4]-=1
                if dict_data[HT][4]>=0:
                    dict_data[HT][4]=-1
                if dict_data[VT][4]<0:
                    dict_data[VT][4]=1
                
                
            else:
                dict_data[Score[compt+2]][2]+=1
                if dict_data[HT][4]>=0:
                    dict_data[HT][4]+=1
                if dict_data[VT][4]<0:
                    dict_data[VT][4]-=1
                if dict_data[VT][4]>=0:
                    dict_data[VT][4]=-1
                if dict_data[HT][4]<0:
                    dict_data[HT][4]=1
                
                
            
                
            print(dict_data[Score[compt]])
            compt+=3
            print(G)
        compt+=1
    return listG,listR

for y in year:
    Score=[]
    for h in range(len(Months)):
        url1='https://www.basketball-reference.com/leagues/NBA_'+y+'_games-'+Months[h]+'.html'
        print(url1)
        sou=make_soup(url1)
        container=sou.find("table",{"id":"schedule"})
        for record in container.findAll('td'):
            Score.append(record.get_text())
            #print(record.get_text())
            for data in record.findAll('a'):
                #print(data.get_text())
                Liste0.append(data.get_text())
    a,b=Get_data(Score)
    arrayG=arrayG+a
    arrayR=arrayR+b
print(arrayG)
print(arrayR)
numpy.save('Games.npy',arrayG,allow_pickle=True)
numpy.save('Results.npy',arrayR,allow_pickle=True)
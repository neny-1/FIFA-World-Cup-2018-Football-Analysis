import json
import matplotlib.pyplot as plt

# Egypt vs Saudi Arabia match FIFA World Cup 2018

#load competitions file.json
with open("../../Statsbomb/data/competitions.json") as comp:
  competitions =json.load(comp)
                                         
for comp in competitions:
    if comp['competition_name']=="FIFA World Cup" :
       World_cup_id = comp['competition_id']
       
#Get all matches in FIFA World Cup
#Load the list of matches for this competition
with open('../../Statsbomb/data/matches/'+str(World_cup_id)+'/3.json') as f:
    matches_world_cup = json.load(f)
    
# Get match id from  World_cup_id => FIFA World Cup
home_team_required="Saudi Arabia"
away_team_required="Egypt"

for match in matches_world_cup:
    home_team = match["home_team"]["home_team_name"] 
    away_team = match["away_team"]["away_team_name"]
    if (home_team== home_team_required  and away_team==away_team_required ):
       Egypt_vs_Saudi_id = match["match_id"]
print(Egypt_vs_Saudi_id)

file_name = str(Egypt_vs_Saudi_id)+".json"

#Get match event data from match id
with open('../../Statsbomb/data/events/'+str(Egypt_vs_Saudi_id)+".json") as data_file:
 
   Egypt_vs_Saudi_match = json.load(data_file)


#Get the nested structure into a dataframe 
#Store the dataframe in a dictionary with the match id as key (remove '.json' from string)
from pandas.io.json import json_normalize
df = json_normalize(Egypt_vs_Saudi_match, sep = "_").assign(match_id = file_name[:-5])

#A dataframe of shots
shots = df.loc[df['type_name'] == 'Shot'].set_index('id')


#Size of the pitch in yards 
pitchLengthX=120
pitchWidthY=80

#Draw the pitch
from mplsoccer.pitch import Pitch
def mplsoccer_pitchh(length,width,linecolor) :
    pitch = Pitch(pitch_color='#1f8f18', line_color=linecolor,
                  pitch_length=length, pitch_width=width,
                  stripe_color='#1f7319', stripe=True)  # optional stripes
    fig, ax = pitch.draw()
    return fig,ax
  
  
(fig,ax) = mplsoccer_pitchh(pitchLengthX,pitchWidthY,"white")

Saudi_shots_counter=0
Egypt_shots_counter=0

#Plot the shots
for i,shot in shots.iterrows():
    x=shot['location'][0]
    y=shot['location'][1]
    
    goal=shot['shot_outcome_name']=='Goal'
    team_name=shot['team_name']
    
    circleSize=2
    if (team_name==home_team_required):
        if goal:
            shotCircle=plt.Circle((x,y),circleSize,color="red")
            if shot['player_name']=="Salem Mohammed Al Dawsari":
              shot['player_name'] ="Al Dawsari"
            if shot['player_name']=="Salman Mohammed Al Faraj":
              shot['player_name'] ="Al Faraj"
            plt.text((x-3),y+2.5,shot['player_name'],color="white",fontsize=14,fontweight="bold") 
        else:
            shotCircle=plt.Circle((x,y),circleSize,color="red")     
            shotCircle.set_alpha(.38)
        Saudi_shots_counter=Saudi_shots_counter+1
    elif (team_name==away_team_required):
        if goal:
            shotCircle=plt.Circle((pitchLengthX-x,pitchWidthY-y),circleSize,color="blue") 
            plt.text((pitchLengthX-x+1),(pitchWidthY-y+1),shot['player_name'],color="white",fontsize=14,fontweight="bold") 
        else:
            shotCircle=plt.Circle((pitchLengthX-x,pitchWidthY-y),circleSize,color="blue")      
            shotCircle.set_alpha(.38)
        Egypt_shots_counter=Egypt_shots_counter+1
    ax.add_patch(shotCircle)

#Goals counter
plt.text(44,5,away_team_required+' '+str(match['away_score'])+' : ',color="white",fontsize=25,fontweight="bold") 
plt.text(62,5,str(match['home_score'])+' '+home_team_required ,color="white",fontsize=25,fontweight="bold") 

#Shots counter
plt.text(39,70,away_team_required + ' shots',color="white",fontsize=22,fontweight="bold") 
plt.text(62,70,home_team_required + ' shots',color="white",fontsize=22,fontweight="bold") 

plt.text(48,75,Egypt_shots_counter,color="white",fontsize=22,fontweight="bold") 
plt.text(75,75,Saudi_shots_counter,color="white",fontsize=22,fontweight="bold") 



fig.set_size_inches(14, 10)
fig.savefig('plots/shots.png', dpi=300) 
plt.show()
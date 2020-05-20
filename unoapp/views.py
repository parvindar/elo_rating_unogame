from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from unoapp import showstats as data
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
import json

rating = data.calcRating()
scores = data.showScores()
avg = data.showAverage() 


class RatingChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        # return 
        labels = rating['x']
        return labels

    def get_providers(self):
        """Return names of datasets."""
        # return ["Central", "Eastside", "Westside"]
        providers = ["Daddy","Mummy","Parvindar","Ricky"]
        return providers

    def get_data(self):
        """Return 3 datasets to plot."""
        chartdata = rating['indivisual']
        # return [[75, 44, 92, 11, 44, 95, 35],
        #         [41, 92, 18, 3, 73, 87, 92],
        #         [87, 21, 94, 3, 90, 13, 65]]
        return chartdata

class AvgChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        # return 
        labels = avg['x']
        return labels

    def get_providers(self):
        """Return names of datasets."""
        # return ["Central", "Eastside", "Westside"]
        providers = ["Daddy","Mummy","Parvindar","Ricky"]
        return providers

    def get_data(self):
        """Return 3 datasets to plot."""
        chartdata = avg['average']
        # return [[75, 44, 92, 11, 44, 95, 35],
        #         [41, 92, 18, 3, 73, 87, 92],
        #         [87, 21, 94, 3, 90, 13, 65]]
        return chartdata


class SumScoreChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        # return 
        labels = scores['x']
        return labels

    def get_providers(self):
        """Return names of datasets."""
        # return ["Central", "Eastside", "Westside"]
        providers = ["Daddy","Mummy","Parvindar","Ricky"]
        return providers

    def get_data(self):
        """Return 3 datasets to plot."""
        chartdata = scores['sum']
        # return [[75, 44, 92, 11, 44, 95, 35],
        #         [41, 92, 18, 3, 73, 87, 92],
        #         [87, 21, 94, 3, 90, 13, 65]]
        return chartdata



rating_line_chart = TemplateView.as_view(template_name='index.html')
rating_line_chart_json = RatingChartJSONView.as_view()

avg_line_chart = TemplateView.as_view(template_name='index.html')
avg_line_chart_json = AvgChartJSONView.as_view()


sumscore_line_chart = TemplateView.as_view(template_name='index.html')
sumscore_line_chart_json = SumScoreChartJSONView.as_view()

names = {
	0 : "Daddy",
	1 : "Mummy",
	2 : "Parvindar",
	3 : "Ricky",
	"Daddy" : 0,
	"Mummy" : 1,
	"Parvindar" : 2,
	"Ricky" : 3
}

def calcconsecutivewins(ranks):
	conswins = [0,0,0,0]
	curr = [0,0,0,0]
	for i in range(len(ranks)):
		for j in range(len(ranks[i])):
			if ranks[i][j]==1 :
				if j>0 :
					if ranks[i][j-1] == 1 :
						curr[i]+=1
					else:
						curr[i]=1
					conswins[i] = max(conswins[i],curr[i])
				else:
					curr[i]=1
					conswins[i]=1

	return conswins

def getRanks():
	ranks = [[],[],[],[]]
	for game in rating['games']:
		for p in game :
			ranks[names[p.name]].append(p.rank)
	return ranks


def calcwins():
	wins = [0,0,0,0]
	for game in rating['games']:
		for i in range(len(game)):
			if game[i].rank==1 :
				wins[names[game[i].name]]+=1
	return wins

def calcmax():
	maxx = [0,0,0,0]
	for game in rating['games']:
		for i in range(len(game)):
			if game[i].score > maxx[names[game[i].name]] :
				maxx[names[game[i].name]] = game[i].score
	return maxx

def calcmaxrating():
	maxx = [0,0,0,0]
	for game in rating['games']:
		for i in range(len(game)):
			if game[i].new_rating > maxx[names[game[i].name]] :
				maxx[names[game[i].name]] = game[i].new_rating
	return maxx	

profile_maxx = calcmax()
profile_wins = calcwins()
profile_maxrating = calcmaxrating()
profile_ranks = getRanks()
profile_conswins = calcconsecutivewins(profile_ranks)

def index(request):
	template = loader.get_template('unoapp/index.html')
	m_maxwins = 0
	m_maxscore = 0
	m_maxrating = 1500
	m_maxsum = 0

	profiles = []
	maxx =  profile_maxx
	wins = profile_wins
	maxrating = profile_maxrating
	ranks = profile_ranks
	conswins = profile_conswins


	for i in range(4):
		player = {
			'name' : names[i],
			'rating' : rating['indivisual'][i][len(rating['indivisual'][i])-1],
			'avg'	: round(avg['average'][i][len(avg['average'][i])-1],2),
			'sum' : scores['sum'][i][len(scores['sum'][i])-1],
			'wins' : wins[i],
			'conswins' : conswins[i],
			'maxscore' : maxx[i],
			'maxrating' : maxrating[i],
			'lastmatch' : scores['scores'][i][len(scores['scores'][i])-1],
			'ranks' : ranks[i],
			'scores': scores['scores'][i],
			'ratings': rating['indivisual'][i],
			'avgs' : avg['average'][i]
		}
		if player['wins'] > m_maxwins :
			m_maxwins = player['wins']
		if player['maxrating'] > m_maxrating :
			m_maxrating = player['maxrating']
		if player['sum'] > m_maxsum:
			m_maxsum = player['sum']
		if player['maxscore'] > m_maxscore:
			m_maxscore = player['maxscore']

		profiles.append(player)
	
	profiles = sorted(profiles,key=lambda x: x['rating'], reverse=True)

	m_maxscore_player = []
	m_maxrating_player = []
	m_maxwins_player = []
	m_maxsum_player = []

	for p in profiles :
		if p['wins'] == m_maxwins :
			m_maxwins_player.append(p['name'])

		if p['maxrating'] == m_maxrating :
			m_maxrating_player.append(p['name'])

		if p['sum'] == m_maxsum:
			m_maxsum_player.append(p['name'])

		if p['maxscore'] == m_maxscore:
			m_maxscore_player.append(p['name'])

	highlights = {
		'maxscore' : {
			'val' : m_maxscore,
			'players' : m_maxscore_player
		},
		'maxrating' :{
			'val' : m_maxrating,
			'players' : m_maxrating_player
		},
		'maxwins' :{
			'val' : m_maxwins,
			'players' : m_maxwins_player
		},
		'maxsum' :{
			'val' : m_maxsum,
			'players' : m_maxsum_player
		}
	}

	context = {
		'rating' : rating,
		'scores' : scores,
		'avg' : avg,
		'profiles' : profiles,
		'highlights' : highlights
	}
	return HttpResponse(template.render(context,request))

def profile(request,user_id):
	template = loader.get_template('unoapp/profile.html')
	index = int(user_id)

	profiles = []
	maxx =  profile_maxx
	wins = profile_wins
	maxrating = profile_maxrating
	ranks = profile_ranks
	conswins = profile_conswins

	games = []
	for i in range(len(ranks[index])) :
		game = {
			'rank' : ranks[index][i],
			'old_rating' : rating['indivisual'][index][i],
			'new_rating' : rating['indivisual'][index][i+1],
			'score' : scores['scores'][index][i],
			'delta' : rating['indivisual'][index][i+1] - rating['indivisual'][index][i],
			'avg' : avg['average'][index][i]
		}
		games.append(game)

	i = index
	player = {
		'name' : names[i],
		'rating' : rating['indivisual'][i][len(rating['indivisual'][i])-1],
		'avg'	: round(avg['average'][i][len(avg['average'][i])-1],2),
		'sum' : scores['sum'][i][len(scores['sum'][i])-1],
		'wins' : wins[i],
		'conswins' : conswins[i],
		'maxscore' : maxx[i],
		'maxrating' : maxrating[i],
		'lastmatch' : scores['scores'][i][len(scores['scores'][i])-1],
		'games' : games
	}


	return HttpResponse(template.render(player,request))

def newGame(request):
	Daddy = request.GET['Daddy'] # u_name is the name of the input tag
	Mummy = request.GET['Mummy']
	Parvindar = request.GET['Parvindar']
	Ricky = request.GET['Ricky']
	if Daddy==None or Mummy==None or Parvindar==None or Ricky==None :
		return

	print("all ok upto here")



	









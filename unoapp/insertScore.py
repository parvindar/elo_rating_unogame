from unoapp import datafunc as db

game_name = "original"
first_prize = 200
second_prize = 100

players = ["Daddy","Mummy","Parvindar","Ricky"]
num = len(players)

def insertScores(scores):
	game_id = db.newGame(game_name,first_prize,second_prize)
	for i in range(0,num):
		name = players[i]
		score = scores[i]
		db.insertScore(game_id,name,score)


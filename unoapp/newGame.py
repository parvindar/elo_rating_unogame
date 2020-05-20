import datafunc as db

game_name = "original"
first_prize = 200
second_prize = 100

game_id = db.newGame(game_name,first_prize,second_prize)
players = ["Daddy","Mummy","Parvindar","Ricky"]

num = len(players)

for i in range(0,num):
	name = players[i]
	score = input("Enter score of " + players[i]+"\n")
	db.insertScore(game_id,name,score)


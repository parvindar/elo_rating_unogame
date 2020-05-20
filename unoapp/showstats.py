from unoapp import datafunc as db
import numpy as np
import math
import matplotlib.pyplot as plt

DS = "Daddy"
SK = "Mummy"
PS = "Parvindar"
SS = "Ricky"

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


class User(object):

	def __init__(self,score,rank, old_rating,avg=0 ,name='', official_new_rating=0):
		self.score = int(score)
		self.rank = float(rank)
		self.old_rating = int(old_rating)
		self.seed = 1.0
		self.name = str(name)
		self.new_rating = 0
		self.avg = avg
        # official_new_rating: used for validating result
		self.official_new_rating = int(official_new_rating)

class RatingCalculator(object):

    def __init__(self, users):
        self.user_list = users
        # for user in users:
        #     self.user_list.append(User(user.score,user.rank, user.old_rating, user.name, user.new_rating,user.avg))

    def cal_p(self, user_a, user_b):
        return 1.0 / (1.0 + pow(10, (user_b.old_rating - user_a.old_rating) / 400.0))

    def get_ex_seed(self, user_list, rating, own_user):
        ex_user = User(0.0,0.0, rating)
        result = 1.0
        for user in user_list:
            if user != own_user:
                result += self.cal_p(user, ex_user)
        return result

    def cal_rating(self, user_list, rank, user):
        left = 1
        right = 8000
        while right - left > 1:
            mid = int((left + right) / 2)
            if self.get_ex_seed(user_list, mid, user) < rank:
                right = mid
            else:
                left = mid
        return left

    def calculate(self):
        # Calculate seed
        for i in range(len(self.user_list)):
            self.user_list[i].seed = 1.0
            for j in range(len(self.user_list)):
                if i != j:
                    self.user_list[i].seed += self.cal_p(self.user_list[j], self.user_list[i])

        # Calculate initial delta and sum_delta
        sum_delta = 0
        for user in self.user_list:
            user.delta = int(
                (self.cal_rating(self.user_list, math.sqrt(user.rank * user.seed), user) - user.old_rating) / 2.0)
            sum_delta += user.delta

        # Calculate first inc
        inc = int((-sum_delta / len(self.user_list)))
        mod = sum_delta%len(self.user_list)
        for user in self.user_list:
            user.delta += inc

        # while mod > 0 :
        # 	self.user_list[mod].delta -= 1
        # 	mod-=1

        self.user_list = sorted(self.user_list,key = lambda x:x.avg,reverse=False)
        for i in range(mod):
        	self.user_list[i].delta -= 1







        # # # Calculate second inc
        # self.user_list = sorted(self.user_list, key=lambda x: x.old_rating, reverse=True)
        # s = min(len(self.user_list), int(4 * round(math.sqrt(len(self.user_list)))))
        # sum_s = 0
        # for i in range(s):
        #     sum_s += self.user_list[i].delta
        # inc = min(max(int(-sum_s / s), -10), 0)
        # Calculate new rating
        for user in self.user_list:
            # user.delta += inc
            user.new_rating = user.old_rating + user.delta
        self.user_list = sorted(self.user_list, key=lambda x: x.rank, reverse=False)




results = db.getScores()


def showAverage():
	y1 = []
	y2 = []
	y3 = []
	y4 = []
	x = []
	for i in range(len(results)):
		x.append(i+1)
		y1.append(results[i][1])
		y2.append(results[i][2])
		y3.append(results[i][3])
		y4.append(results[i][4])

	for i in range(1,len(y1)):
		y1[i] = round(float((y1[i-1]*i)+y1[i])/(i+1),2)

	for i in range(1,len(y2)):
		y2[i] = round(float((y2[i-1]*i)+y2[i])/(i+1),2)

	for i in range(1,len(y1)):
		y3[i] = round(float((y3[i-1]*i)+y3[i])/(i+1),2)

	for i in range(1,len(y4)):
		y4[i] = round(float((y4[i-1]*i)+y4[i])/(i+1),2)

	res = {
		'average' : [y1,y2,y3,y4],
		'x' : x
	}
	return res


def calcRating():
	games = []
	averages = showAverage()
	avg = averages['average']

	old_rating = [0,1500,1500,1500,1500]
	for i in range(len(results)):
		players = []
		players.append(User(results[i][1],1,old_rating[1],avg[0][i],DS))
		players.append(User(results[i][2],1,old_rating[2],avg[1][i],SK))
		players.append(User(results[i][3],1,old_rating[3],avg[2][i],PS))
		players.append(User(results[i][4],1,old_rating[4],avg[3][i],SS))
		players = sorted(players, key=lambda x: x.score, reverse=True)

		for j in range(1,len(players)):
			if players[j].score == players[j-1].score :
				players[j].rank = players[j-1].rank
			else :
				players[j].rank = players[j-1].rank + 1;


		calculator = RatingCalculator(players)
		calculator.calculate()
		games.append(calculator.user_list)
		ratesum = 0
		for j in range(len(games[i])):
			p = games[i][j]
			ratesum+=p.new_rating
			# print(p.new_rating," + ",end = ' ')
			p.rank = int(p.rank)
			if(p.name == DS):
				old_rating[1]=p.new_rating
			elif p.name == SK :
				old_rating[2]=p.new_rating
			elif p.name == PS:
				old_rating[3]=p.new_rating
			elif p.name == SS:
				old_rating[4]=p.new_rating
		print("rating sum : ",ratesum)

	
	y1 = [1500]
	y2 = [1500]
	y3 = [1500]
	y4 = [1500]
	x  = [0]
	for i in range(len(games)) :
		print(i)
		x.append(i+1)
		for j in range (len(games[i])):
			p = games[i][j]
			if(p.name == DS):
				y1.append(p.new_rating)
			elif p.name == SK :
				y2.append(p.new_rating)
			elif p.name == PS:
				y3.append(p.new_rating)
			elif p.name == SS:
				y4.append(p.new_rating)
			# print(games[i][j].rank," ",games[i][j].name ," ",games[i][j].score," ",games[i][j].old_rating," ",games[i][j].new_rating," ",games[i][j].delta)

	res = {
		'games' : games,
		'indivisual': [y1,y2,y3,y4],
		'averages' : averages,
		'x' : x
	}
	return res
	# plt.plot(x,y1,label = DS,marker="o",markersize=4)
	# plt.plot(x,y2,label = SK,marker="o",markersize=4)
	# plt.plot(x,y3,label = PS,marker="o",markersize=4)
	# plt.plot(x,y4,label = SS,marker="o",markersize=4)

	# plt.xlabel("Games")
	# plt.ylabel("Ratings")

	# plt.title("Rating Changes")
	# plt.legend()
	# plt.show()


def showScores():
	y1 = []
	y2 = []
	y3 = []
	y4 = []
	x = []
	for i in range(len(results)):
		x.append(i+1)
		y1.append(results[i][1])
		y2.append(results[i][2])
		y3.append(results[i][3])
		y4.append(results[i][4])
	s1 = []
	s2 = []
	s3 = []
	s4 = []

	s1.append(y1[0])
	s2.append(y2[0])
	s3.append(y3[0])
	s4.append(y4[0])

	for i in range(1,len(y1)):
		s1.append(s1[i-1]+y1[i])
		s2.append(s2[i-1]+y2[i])
		s3.append(s3[i-1]+y3[i])
		s4.append(s4[i-1]+y4[i])

	res = {
		'scores' : [y1,y2,y3,y4],
		'sum' : [s1,s2,s3,s4],
		'x' : x
	}
	return res
	# plt.plot(x,y1,label = "Daddy",marker="o",markersize=4)
	# plt.plot(x,y2,label = "Mummy",marker="o",markersize=4)
	# plt.plot(x,y3,label = "Parvindar",marker="o",markersize=4)
	# plt.plot(x,y4,label = "Ricky",marker="o",markersize=4)

	# plt.xlabel("Games")
	# plt.ylabel("Scores")

	# plt.title("Scores of UNO")
	# plt.legend()
	# plt.show()

	# plt.plot(x,s1,label = "Daddy",marker="o",markersize=4)
	# plt.plot(x,s2,label = "Mummy",marker="o",markersize=4)
	# plt.plot(x,s3,label = "Parvindar",marker="o",markersize=4)
	# plt.plot(x,s4,label = "Ricky",marker="o",markersize=4)
	# plt.xlabel("Games")
	# plt.ylabel("Total Scores")

	# plt.title("Total Scores of UNO")
	# plt.legend()
	# plt.show()


	# plt.plot(x,y1,label = DS,marker="o",markersize=4)
	# plt.plot(x,y2,label = SK,marker="o",markersize=4)
	# plt.plot(x,y3,label = PS,marker="o",markersize=4)
	# plt.plot(x,y4,label = SS,marker="o",markersize=4)

	# plt.xlabel("Games")
	# plt.ylabel("Average")

	# plt.title("Average Scores")
	# plt.legend()
	# plt.show()


# showScores()
# showAverage()
# calcRating()

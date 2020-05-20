import sqlite3

DB_Name =  "unoapp/uno.db"

def newGame(name,first_prize,second_prize):
	TableSchema = "insert into games(name,first_prize,second_prize,datetime) values(?,?,?,datetime('now'))"
	val = (name,first_prize,second_prize)

	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()
	#Create Tables
	curs.execute(TableSchema,val)
	conn.commit()
	TableSchema = "SELECT id FROM games ORDER BY id DESC LIMIT 1;"
	curs.execute(TableSchema)
	result = curs.fetchall()
	curs.close()
	conn.close()
	return result[0][0]

def insertScore(gameid,name,score):
	TableSchema = "insert into results(gameid,name,score) values(?,?,?)"
	val = (gameid,name,score)

	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()
	#Create Tables
	curs.execute(TableSchema,val)
	conn.commit()
	curs.close()
	conn.close()

def getTotalScores():
	TableSchema = "select name,sum(score) as 'total score' from results group by name order by sum(score) desc;"
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()
	curs.execute(TableSchema)
	result = curs.fetchall()
	curs.close()
	conn.close()
	return result

def getAll():
	TableSchema = "select * from results"
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()
	curs.execute(TableSchema)
	result = curs.fetchall()
	curs.close()
	conn.close()
	return result

def getWinners():
	TableSchema = "select * from results group by gameid order by gameid,max(score);"
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()
	curs.execute(TableSchema)
	result = curs.fetchall()
	curs.close()
	conn.close()
	return result

def getScores():
	TableSchema = "select * from v1;"
	try:
		conn = sqlite3.connect(DB_Name)
	except Error as e:
		print(e)

	curs = conn.cursor()
	curs.execute(TableSchema)
	result = curs.fetchall()
	curs.close()
	conn.close()
	return result

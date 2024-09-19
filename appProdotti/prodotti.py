from flask import Flask, render_template, request
import mysql.connector
class prodotto:
    def __init__(self, nome, marca, prezzo, url,pezzi,  prodottiV):
        self.nome = nome
        self.marca = marca
        self.prezzo = prezzo
        self.url = url
        self.pezzi = pezzi
        self.prodottiV = prodottiV




app = Flask(__name__)


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Ilfoggia1",
  database="PyDb"
)

@app.route('/gestore')
def index():
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM prodotti")

    myresult = mycursor.fetchall()
    listaD = []
    for i in myresult:
        listaD.append(i[2])


    listaS = list(dict.fromkeys(listaD))
    print(listaS)

    return render_template("gestore.html", lista = myresult, listaS = listaS)

@app.route('/process', methods=['POST', 'GET'])
def process():
    if request.method == 'POST':
        nome = request.form['nome']
        marca = request.form['marca']
        prezzo = request.form['prezzo']
        url = request.form['url']
        pezzi = request.form['pezzi']
        prodottiV = 0

        mycursor = mydb.cursor()
        sql = ("INSERT INTO prodotti (nome, marca, prezzo, url,pezzi,  prodottiV) VALUES (%s, %s,%s, %s, %s, %s)")
        val = (nome, marca, prezzo, url, pezzi, prodottiV)
        mycursor.execute(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "record inserted.")

        p1 = prodotto(nome, marca, prezzo, url, pezzi, prodottiV)


    return render_template("insert.html", prod = p1)


@app.route("/remove", methods=['POST', 'GET'])
def remove():
    if request.method == 'POST':
        id = int(request.form['prod'])
        mycursor = mydb.cursor()
        sql = ("DELETE FROM prodotti WHERE id = %s")
        val = (id,)
        mycursor.execute(sql, val)
        mydb.commit()

        print(mycursor.rowcount, "record removed.")


        return(index())

@app.route("/search", methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        marca = request.form['marca']
        mycursor = mydb.cursor()
        sql = "SELECT * FROM prodotti WHERE marca = (%s)"
        val = (marca,)
        mycursor.execute(sql, val)

        myresult = mycursor.fetchall()






        return render_template("stampaMarche.html", lista = myresult)
@app.route("/")
def store():
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM prodotti")

    myresult = mycursor.fetchall()


    return render_template("store.html", lista = myresult)
@app.route("/updatePezzi", methods=['POST', 'GET'])
def updatePezzi():
    if request.method == 'POST':
        id = int(request.form['prodID'])
        pezzi = request.form['Npezzi']
        mycursor = mydb.cursor()
        sql =  "UPDATE prodotti SET pezzi = pezzi + %s  WHERE id = %s"
        val = (pezzi, id)
        mycursor.execute(sql, val)
        mydb.commit()

        print(mycursor.rowcount, "record update.")


        return(index())
if __name__ == '__main__':

   app.run(debug = True)
from flask import Flask,jsonify,request,render_template
from pymongo import MongoClient
import os
app = Flask(__name__)
mongourl = os.getenv("MONGO-URL","mongodb://localhost:27017")
client = MongoClient(mongourl)
db = client.todoapp
customerCollection=db["order"]

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/admin')
def admin():
  return render_template('admin.html')

@app.route("/order")
def evaluateorder():
    name = request.args.get('name', '', type=str)
    phone = request.args.get('phone', 0, type=int)
    quantity = request.args.get('quantity', 0, type=int)
    customerCollection.insert_one({'name':name,'phone':phone,'quantity':quantity})
    return jsonify ({'result':'Success'})

@app.route("/orders", methods=['POST'])
def orderlist():
    returnList = []
    page_size=request.form.get('rowCount', 10, type=int)
    page_num=request.form.get('current', 1, type=int)
    skips = page_size * (page_num - 1)
    totalcount=customerCollection.count()
    for customer in customerCollection.find().skip(skips).limit(page_size):
        returnList.append({'name':customer['name'],'phone':customer['phone'],'quantity':customer['quantity']})
    return jsonify ({'current':page_num,
                     'rowCount': page_size,
                     'rows':returnList,'total':totalcount})

@app.route("/deleteorder", methods=['DELETE'])
def deleteOrder():
    phone=request.form.get('phone',0,type=int)
    deletemap = {'phone': phone}
    x=customerCollection.delete_many(deletemap)
    print(x.deleted_count, " documents deleted.")
    return jsonify({'result': 'Success'})

app.run(port=5000)
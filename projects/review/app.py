from pymongo import MongoClient

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/list', methods=["GET"])
def star_list():
    star_list = list(db.mystar.find({},{'_id':False}).sort('like',-1))

    return jsonify({'result':'success','star_list':star_list})

@app.route('/api/like', methods=["POST"])
def star_like():
    star_name = request.form['name_give']
    name_get = db.mystar.find_one({'name':star_name})
    new_like = name_get['like']+1
    db.mystar.update_one({'name':star_name},{'$set':{'like':new_like}})

    return jsonify({'result':'success','msg':'좋아요 완료!'})

@app.route('/api/delete', methods=["POST"])
def star_del():
    star_name = request.form['name_give']
    db.mystar.delete_one({'name':star_name})

    return jsonify({'result':'success','msg':'삭제 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

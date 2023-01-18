from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.csmowq9.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/homework", methods=["POST"])
def homework_post():
    nick_name = request.form['nick_name']
    comment = request.form['comment']
    print(nick_name, comment)
    doc = {'nick_name': nick_name, 'comment': comment}
    db.guests.insert_one(doc)
    return jsonify({'msg':'소중한 익명 의견 감사합니다!'})

@app.route("/homework", methods=["GET"])
def homework_get():
    all_guests = list(db.guests.find({}, {'_id': False}))
    return jsonify({'guests': all_guests})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
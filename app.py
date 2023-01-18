import pymongo
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.csmowq9.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/blind", methods=["POST"])
def blind_post():
    nick_name = request.form['nick_name']
    content = request.form['content']
    all_posts = list(db.posts.find({}, {'_id': False}))
    count = len(all_posts) + 1
    doc = {'nick_name': nick_name, 'content': content, 'post_id': count}
    db.posts.insert_one(doc)
    return jsonify({'msg':'소중한 익명 의견 감사합니다!'})

@app.route("/blind/comment", methods=["POST"])
def blind_comment():
    post_num = request.form['post_num']
    comment = request.form['comment']
    nick_name = request.form['nick_name']
    doc = {'nick_name': nick_name, 'comment': comment, 'post_num': post_num}
    db.comments.insert(doc)
    return jsonify({'msg': '블라인드 창 생태계에 중독되셨군요!'})

@app.route("/blind", methods=["GET"])
def blind_get():
    page = int(request.args.get('page', 1))
    limit = 5
    offset = (page -1)* limit
    all_posts = list(db.posts.find({}, {'_id': False}).sort('post_id',pymongo.DESCENDING).limit(limit).skip(offset))
    return jsonify({'posts': all_posts})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
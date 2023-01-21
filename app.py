import pymongo
from flask import Flask, render_template, request, jsonify, session, redirect
from pymongo import MongoClient
import random
client = MongoClient('mongodb+srv://test:sparta@cluster0.csmowq9.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta
app = Flask(__name__)
app.secret_key = "super secret key"


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/blind", methods=["POST"])
def blind_post():
    nick_name = request.form['nick_name']
    content = request.form['content']
    title = request.form['title']
    all_posts = list(db.posts.find({}, {'_id': False}))
    count = len(all_posts) + 1
    doc = {'nick_name': nick_name, 'content': content, 'post_id': count, 'title': title, 'views': 0, 'comments': 0}
    db.posts.insert_one(doc)

    session['username'] = nick_name # 테스트 필요

    return jsonify({'msg': '소중한 익명 의견 감사합니다!'})


@app.route("/blind/comment", methods=["POST"])
def blind_comment():
    post_id = int(request.form['post_id'])
    comment = request.form['comment']
    nick_name = session.get('username','')
    doc = {'nick_name': nick_name, 'comment': comment, 'post_id': post_id}
    db.comments.insert_one(doc)

    all_comments = list(db.comments.find({'post_id': post_id}, {'_id': False}))
    comment_count = len(all_comments)
    db.posts.update_one({'post_id': post_id}, {'$set': {'comments': comment_count}})

    return jsonify({'msg': '블라인드 창 생태계에 중독되셨군요!'})


@app.route("/blind", methods=["GET"])
def blind_get():
    page = int(request.args.get('page', 1))
    username = session.get('username', '')
    limit = 5
    offset = (page - 1) * limit
    all_posts = list(db.posts.find({}, {'_id': False}).sort('post_id', pymongo.DESCENDING).limit(limit).skip(offset))
    popular_posts = list(db.posts.find({},{'_id': False}).sort([('views', pymongo.DESCENDING), ('comments', pymongo.DESCENDING)]).limit(limit))
    return jsonify({'posts': all_posts, 'popular_posts': popular_posts, 'post_num': len(list(db.posts.find({}, {'_id': False}))), 'username': username})


@app.route("/blind/one-post", methods=["GET"])
def show_one_post():
    post_id = int(request.args.get('post_id', 1))
    all_comments = list(db.comments.find({'post_id': post_id}, {'_id': False}))
    post = db.posts.find_one({'post_id': post_id})
    views = int(post['views'])

    db.posts.update_one({'post_id': post_id}, {'$set': {'views': views + 1}})

    # post_session = session.get(f'post_{post_id}', None)
    # if not post_session: # 이미 저장된 세션이 없을 때만
    #     db.posts.update_one({'post_id': post_id}, {'$set': {'views': views+1}})
    #     session[f'post_{post_id}'] = post_id

    nick_name = post['nick_name']
    content = post['content']
    title = post['title']
    return jsonify({'comments': all_comments, 'nick_name': nick_name, 'content': content, 'title': title})

@app.route("/randint", methods=["GET"])
def randint_get():
    # 확률 : 1/100
    lucky_num = random.randint(1,10000)
    return jsonify({'lucky_num': lucky_num})

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', port=5001, debug=True)

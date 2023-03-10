import pymongo
from flask import Flask, render_template, request, jsonify, session, redirect
from pymongo import MongoClient
import random
from fortune import fortune_list

client = MongoClient('mongodb+srv://test:sparta@cluster0.csmowq9.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta
app = Flask(__name__)
app.secret_key = "super secret key"


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pc')
def pc():
    return render_template('pc.html')

@app.route('/mobile')
def mobile():
    return render_template('mobile.html')

@app.route('/ads')
def ads():
    return render_template('ads.html')

@app.route('/posts')
def posts():
    return render_template('posts.html')

@app.route('/populars')
def populars():
    return render_template('populars.html')


@app.route('/events')
def events():
    return render_template('events.html')



@app.route("/blind", methods=["POST"])
def blind_post():
    nick_name = request.form['nick_name']
    content = request.form['content']
    title = request.form['title']
    all_posts = list(db.posts.find({}, {'_id': False}).sort('post_id', pymongo.DESCENDING))
    last_index = int(all_posts[0]['post_id'])
    post_id = last_index + 1
    doc = {'nick_name': nick_name, 'content': content, 'post_id': post_id, 'title': title, 'views': 0, 'comments': 0}
    db.posts.insert_one(doc)

    session['username'] = nick_name # 테스트 필요

    return jsonify({'msg': '소중한 익명 의견 감사합니다!'})


@app.route("/blind/comment", methods=["POST"])
def blind_comment():
    post_id = int(request.form['post_id'])
    comment = request.form['comment']
    nick_name = request.form['nick_name']
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
    popular_posts = list(db.posts.aggregate([
        {"$addFields": {"recent": {"$multiply": ["$post_id", 0.8]}}},
        {"$addFields": {"sort_order": {"$add": ["$views", "$comments", "$recent"]}}},
        {"$sort": {"sort_order": -1}},
        {"$project": {"_id": 0}}
    ]))[:5]

    print(popular_posts)

    #popular_posts = list(db.posts.find({},{'_id': False}).sort([('views', pymongo.DESCENDING), ('comments', pymongo.DESCENDING)]).limit(limit))
    return jsonify({'posts': all_posts, 'popular_posts': popular_posts, 'post_num': len(list(db.posts.find({}, {'_id': False}))), 'username': username})

@app.route("/blind/acc", methods= ["GET"])
def acc_get():
    all_posts = list(db.posts.find({}, {'_id': False}).sort('post_id', pymongo.DESCENDING))
    total_views = 0
    for post in all_posts:
        total_views = total_views + int(post['views'])
    return jsonify({'total_views': total_views})

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
    # 확률 : 1/1000
    lucky_num = random.randint(1,1000)
    return jsonify({'lucky_num': lucky_num})

@app.route("/fortune", methods=["GET"])
def fortune_get():
    fortune = random.choice(fortune_list)
    return jsonify({'fortune': fortune})


if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', port=5001, debug=True)
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
    popular_posts = list(db.posts.find({},{'_id': False}).sort([('views', pymongo.DESCENDING), ('comments', pymongo.DESCENDING)]).limit(limit))
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
    # 확률 : 1/100
    lucky_num = random.randint(1,10000)
    return jsonify({'lucky_num': lucky_num})

@app.route("/fortune", methods=["GET"])
def fortune_get():
    fortune = random.choice(fortune_list)
    return jsonify({'fortune': fortune})

# 포춘쿠키 문장
fortune_list = [
"간절하게 가지고 싶어하던 것이 나에게 알아서 찾아온다.",
"너무 말도 안되게 웃겨서 웃다가 눈물이 날 정도로 재미있는 일이 곧 있을 예정  :)",
"걱정하던 일이 생각보다 너무 쉽게 풀리고 생각하지 못한 신나는 일이 곧 찾아온다.",
"지금은 전혀 모르는 사이지만, 언제나 연락할 수 있는, 소울메이트 같은 친구가 찾아올 예정.",
"전혀 생각하지 못했던 사람에게서 평생 잊지 못할 감동을 받을 예정. 기대하세요!",
"무슨 일이 있어도 당신의 편! 든든한 지원군이 생긴다네요~ 좋은 소식 기다려 보세요 :)",
"내 인생에서 잊지 못할, 언제나 나를 행복하게 해주는 평생 최고의 노래를 만나게 됩니다~",
"내가 안 좋았다고 생각했던 일 덕분에 오히려 더 큰 도움을 받을 일이 생깁니다.",
"오래 전에 베푼 작은 친절이 눈덩이처럼 커져 행운으로 너에게 돌아올 예정이네요~",
"내가 다른 사람을 도와서, 그 사람이 평생 잊지 못할 은인이 되는군요!",
"선택의 길에 있을 때, 이번에는 내가 평소 선택하지 않았을 것을 선택해 보라. 엄청난 행운이 기다리고 있으니.",
"정말 예상치도 못한 큰 선물을 받게 됩니다.",
"엄청난 고민이 찾아오네요. 그러나 너가 최고의 선택을 할 예정이니 걱정마세요. 대신 기대하세요.",
"내가 너무 좋아하는 사람을 올해 진짜로 만나게 됩니다. 언제 만나는 지는 알려줄 수 없지만.",
"정말 마음껏 열심히 해봐도 좋아요. 노력한 만큼 그대로 결과가 나타나서 너무나 뿌듯한 순간이 찾아옵니다.",
"하고 싶었던 일이 있다면 혹은 생겼다면, 바로 도전할 것. 올해는 너에게 진짜 큰 기회가 된다.",
"나랑 닮은 부분이 너무나 많은 소울메이트를 만나게 된다. 금방 너를 찾아올 예정.",
"그 동안 망설였던 걸, 바로 해볼 것. 망설인 시간만큼이나 내가 전혀 예상하지 못한 놀라운 결과를 만날 것이다.",
"나를 항상 자기 일처럼 나서서 도와주는 정말 고마운 친구가 나타난다",
"너에게 지금의 너는 상상도 못한 새로운 모습이 나타난다",
"당신은 모든 사람이 감탄할 만한 엄청난 일을 해낼 예정",
"굳이 힘들여 노력하지 않았는데도, 상상도 못 할 정도로 멋진 일이…",
"내가 좋아하는 음식을 너무 맛있게 자주 먹을 운세. ‘진짜 맛있다. 행복이 따로 있나, 이거지!’",
"누군가를 도울 수 있는 상황에서 잠시 고민을 하다가 나서서 도움을 주니 엄청난 행운이 찾아오게 된다.",
"너에게 얼마나 멋진 일이 벌어지는지 여기에 다 설명할 수가 없다. 기대하라.",
"내 주변의 모든 걸 자세히 살펴보라. 지금도 반짝이는 행운이 바로 곁에 숨어 있다.",
"알지 못했던 나의 능력을 찾아내서 모두가 깜짝 놀랄 만한 일을 하게 된다.",
"전혀 생각지도 못한 곳에서 엄청난 보물을 찾게 되는데…",
"보기만 해도 웃음이 터지는 너무 재미있는 친구를 새로 만나게 된다.",
"내가 잠시 후회했던 선택이 갑자기 엄청난 멋진 결과를 낳는다.",
"내가 평생 잊지 못할 은인을 만날 예정. 누구인지는 직접 찾아낼 것.",
"시간 낭비라고 생각했던 일들이 위기의 순간 나에게 큰 도움이 된다.",
"뭐든 과감하게 도전해도 된다. 모든 일이 예상대로 이루어질 운세.",
"기분 좋은 일이 이래도 되나 싶을 정도로 연달아 이어질 운세.",
"금전은 무자비한 주인이지만 유익한 종이 되기도 한다.",
"미래에 대해 걱정할 필요 없다. 일단 오늘, 내일 할 일 부터 해결하자.",
"물 속에 있던 용이 비로소 승천하는 격. 명예와 재물운이 상승한다.",
"머지않아 단비가 내리니 욕심을 버리고 때를 기다려라.",
"물신양면으로 도와주는 귀인이 나타날 것이다. 귀인의 말에 귀를 기울여야 한다.",
"좋은 인연을 얻게 될 것입니다. 정성과 진심으로 대해주세요.",
"이성과의 생각지 못한 만남이 있으니 긴장을 늦추지 마라.",
"그동안 모르고 있었던 재능이 발현될 것입니다. 새로운 일도 두려워 마세요.",
"내가 옳다고 판단하는 일을 주저하지 말고 실천하라.",
"꿈같이 여겼던 일이 당신 손에 닿을 수 있을 만큼 가까이 다가옵니다. 특히 금전운의 기운이 높아집니다.",
"조금 먼 곳으로 여행을 떠나보세요. 새로운 경험은 당신을 크게 만들어 줄 것입니다.",
"땅을 파면 금을 얻을 운세. 오해는 풀리고 귀인을 만나니 만사형통하다.",
"이해하기 힘든 사람에게 말을 걸어보세요. 생각지 못한 것들을 보게 될 거에요.",
"돈을 벌고 싶다면 돈을 아끼지 마라.",
"성공이 행복의 열쇠가 아니다. 오히려 행복이 성공의 열쇠다.",
"생각지 않은 곳에서 열매를 맺는 격. 가정에 큰 행운이 찾아온다.",
"당신만의 행기를 내뿜는 것에 주저하지 마세요. 당신은 비교되지 않게 아름답습니다.",
"당신에게 행운을 가져다 줄 사람이 가까이 와있습니다. 활짝 웃으며 맞아주세요.",
"이제는 새로운 도전을 시작할 때입니다. 도전하는 당신에게 행운이 함께 하기를!!",
"머지않아 행운이 찾아오겠군요. 행운은 오래 머물지 않고 스쳐 지나는 것입니다. 놓치지 마세요.",
"다른 이에게 나눠줘도 남을 만큼의 거대한 행운이 당신을 향해 한 걸음씩 다가옵니다.",
"직감이 놀랍도록 상승하는 때입니다. 당신의 감을 믿고 도전해보세요.",
"윗 사람에게 많ㅇ은 도움을 받을 운세입니다. 윗 사람에게 많은 덕을 베푸세요.",
"당신의 탁월한 선택이 곧 결실을 맺게 되니 주위의 부러움을 사게 될 것입니다.",
"자신의 감정을 숨기지 마세요. 상대는 당신의 진심을 기다리고 있습니다.",
"할까 말까 고민되는 일이 있다면 지금 당장 도전하라.",
"뜻밖의 행운이 올 것 같은 날입니다. 기대해봐도 좋겠습니다.",
"변화의 시기입니다. 그것은 일상의 즐거움이 될 것입니다. 행복한 날이 이어지겠군요.",
"호랑이 굴에 가야 호랑이를 볼 수 있습니다. 원하는 것이 있다면 실행할 때입니다.",
"금전운이 좋은 날입니다. 예상치 못했던 수입이 들어올 수 있습니다.",
"가치 있는 것에 대해 결코 늦은 때란 없다.",
"하나의 덕으로 열 개의 복을 얻을 것이다. 고집은 멀리하고 겸손을 가까이하라.",
"재물운이 최상입니다. 이렇게 들엉온 재물운은 다른 사람을 위하여 사용하면 좋습니다.",
"지금의 어려움들은 하나의 시기일뿐 언젠가 반드시 이겨낼 수 있습니다.",
"아주 잘하고 있어요! 당신을 사랑하는 사람들이 있다는 사실을 항상 잊지 마세요. 오늘도 행복한 하루 되길.",
"걱정보다 잘하고 있다고 말해보세요. 생각한대로 된다고 하잖아요.",
"오늘은 가슴을 펴고 당당하게 일을 추진시켜보세요. 자신의 생각이 옳다고 믿는다면 순조로운 기운이 당신의 일을 도울 겁니다.",
"위대한 것치고 열정 없이 이루어진 것은 없다.",
"일을 할 때 당신만의 기준을 갖춰 놓으십시오. 내가 어디에 서있고, 어디로 향해 가고 있는지 제대로 알기 위함입니다. 당신은 최고 수준에 도달할 수 있는 사람입니다.",
"새로운 일을 시작한다는 것은 그만큼 새로운 스트레스가 있을 것을 의미합니다. 하지만 새로운 기쁨이 있으므로 시작합니다. 출발선에 오른 당신에게 행운이 함께 하기를!",
"좀 더 유심히 주변을 둘러보세요. 당신에게 특별한 호의를 가지고 도와주는 사람이 있습니다. 당신의 장점을 크게 부각시켜 줄 사람이니 마땅히 감사해야 할 일입니다.",
"인생을 바꿀 수 있는 위대한 비책은 독서다. 오늘 하루 독서로 시작해보세요!",
"책을 읽는다는 것은 오랜 세월동안 축적된 인류의 경험을 배우는 것이다. 책을 가까이 해보세요. 인생이 달라질 것입니다.",
"남의 책을 읽는 데 시간을 보내라. 남이 고생한 것에 의해 쉽게 자기를 개선할 수 있다.",
"한 인간의 존재를 결정짓는 것은 그가 읽은 책과 그가 쓴 글이다.",
"인생에 있어서 가장 큰 기쁨은 '너는 그것을 할 수 없다'고 세상 사람들이 말하는 그 일을 성취시키는 일이다.",
"세월은 누구에게나 공평하게 주어진 자본금이다. 이 자본을 잘 이용한 사람에겐 승리가 있다.",
"매사에 감사해 보세요. 감사는 상대방을 인정하여 자신의 편으로 만드는 가장 좋은 방법입니다.",
"남이 나에게 무엇인가 해주기를 기대하지 말고, 반대로 가능한 남을 위해 살아라. 그러면 어느듯 때가 되면 남들이 나를 위해 필요한 일을 해주고 있을 것이다.",
"좋은 결과를 얻고 싶다면 몸으로 연습하는 것과 똑가이 마음속으로도 연습할 필요가 있다.",
"사업은 망해도 다시 일어설 수 있지만, 인간은 한 번 신용을 잃으면 그것으로 끝장이다.",
"위대한 일을 이루기 위해서는 행동만이 아니라 꿈이 필요하다. 계획만이 아니라 믿음이 필요하다.",
"성공은 성공지향적인 사람에게만 온다. 실패는 스스로 실패할 수밖에 없다고 체념해버리는 사람에게 온다.",
"시간은 인간이 쓸 수 있는 가장 값진 것이다.",
"명성을 쌓는 것에는 20년이란 세월이 걸리며 명성을 무너뜨리는 것에는 5분도 걸리지 않는다. 그걸 명심한다면 당신의 행동이 달라질 것이다.",
"항상 갈구하라. 바보짓을 두려워마라.",
"모든 위대한 사업에도 최초에는 불가능한 일이라고 했던 것들입니다.",
"인간의 마지막 자유는 자신의 사고방식을 결정하는 데에 있다.",
"가끔은 혁신을 추구하다 실수할 때도 있다. 하지만 빨리 인정하고 다른 혁신을 개선해 나가는 것이 최선이다.",
"시간 엄수는 비지니스의 영혼이다.",
"성공의 커다란 비결은 결코 지치지 않는 인간으로 인생을 살아가는 것이다.",
"들은 것은 잊어버리고, 본 것은 기억하고, 직접 해본 것은 이해한다.",
"운명은 우연이 아니라 선택이다. 기다리는 것이 아니라 성취하는 것이다.",
"지금까지 이루어진 수많은 성공적인 비즈니스 뒤에는 다른 사람의 고뇌에 찬 결단이 있었다.",
"승리하면 조금 배울 수 있고, 패배하면 모든 것을 배울 수 있다.",
"앞서 가는 방법의 비밀은 시작하는 것이다. 시작하는 방법의 비밀은 복잡하고 과중한 작업을, 다룰 수 있는 작은 업무로 나누어, 그 첫 번째 업무부터 시작하는 것이다.",
"당신 스스로가 하지 않으면 아무도 당신의 운명을 개선시켜 주지 않을 것이다."
]

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', port=5001, debug=True)
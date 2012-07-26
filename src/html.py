#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
import logging
import Cookie
import tweepy
import uuid
from django.utils import simplejson
from google.appengine.ext import webapp, db
from google.appengine.api import memcache
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from kyouenserver import KyouenPuzzle, KyouenPuzzleSummary
from app import templatefilters

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
SESSION_EXPIRE = 60 * 60 * 24 * 60 # 60日

USER_KEY_PREFIX = 'KEY'

# カスタムタグの登録
webapp.template.register_template_library('app.templatefilters')

class RequestToken(db.Model):
    token_key = db.StringProperty(required=True)
    token_secret = db.StringProperty(required=True)
    creation_date = db.DateTimeProperty(auto_now_add=True)

# ユーザデータ
class User(db.Model):
    userId = db.StringProperty(required=True)
    screenName = db.StringProperty()
    image = db.StringProperty()
    accessToken = db.StringProperty()
    accessSecret = db.StringProperty()
    clearStageCount = db.IntegerProperty()
    
    @staticmethod
    def create_key(userId):
        return(USER_KEY_PREFIX + userId)

# ステージ・ユーザ接続データ
class StageUser(db.Model):
    stage = db.ReferenceProperty(reference_class=KyouenPuzzle, required=True)
    user = db.ReferenceProperty(reference_class=User, required=True)
    clearDate = db.DateTimeProperty(auto_now=True, required=True)

# cookieの取得
def get_cookie():
    cookie = Cookie.SimpleCookie()
    cookie.load(os.environ.get('HTTP_COOKIE', ""))
    return(cookie)

# uuidの設定
def set_uuid(handler, cookie=None):
    if not cookie:
        cookie = get_cookie()
    if not cookie.has_key('sid'):
        cookie['sid'] = str(uuid.uuid4())
        cookie['sid']['max-age'] = SESSION_EXPIRE
        handler.response.headers.add_header(
                                         'Set-Cookie', cookie.output(header='')
                                         )
    return(cookie)

# 文字列を数値に変換（失敗した場合は'0'を返却）
def strToInt(str1):
    return int(str1) if str1.isdigit() else 0

# Twitterのデータを取得
def get_twitter_data(cookie):
    access_token = None
    if cookie.has_key('sid'):
        access_token = memcache.get(cookie['sid'].value) #@UndefinedVariable
    
    if not access_token:
        return None

    try:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(access_token.key, access_token.secret)
        api = tweepy.API(auth_handler=auth)
        me = api.me()
        user = {}
        user['id'] = me.id_str.encode('utf-8')
        user['name'] = me.name.encode('utf-8')
        user['screen_name'] = me.screen_name.encode('utf-8')
        user['profile_image_url'] = me.profile_image_url
        return user
    except:
        return None

def get_user(cookie):
    if not cookie:
        return None
    if not cookie.has_key('sid'):
        return None
    access_token = memcache.get(cookie['sid'].value) #@UndefinedVariable
    if not access_token:
        return None
    return User.gql('WHERE accessToken=:1', access_token.key).get()

# ページを描画
def render_page(handler, page, values=None):
    cookie = set_uuid(handler)
    
    template_values = values or {}
    if not template_values.has_key('user'):
        template_values['user'] = get_user(cookie)

    folder = 'template'
    if is_mobile(handler):
        folder = 'template_mobile'
    path = os.path.join(os.path.dirname(__file__), folder, page)
    html = template.render(path, template_values)
    handler.response.out.write(html)

def is_mobile(handler):
    user_agent = handler.request.user_agent
    if user_agent.find('DoCoMo') > 0:
        return True
    if user_agent.find('KDDI') > 0:
        return True
    if user_agent.find('Vodafone') > 0 or user_agent.find('SoftBank') > 0 or user_agent.find('MOT-') > 0:
        return True
    if user_agent.find('Android') > 0:
        return True
    if user_agent.find('iPhone') > 0:
        return True
    return False

# ログイン処理
class OauthLogin(webapp.RequestHandler):
    def get(self):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth_url = auth.get_authorization_url()
        request_token = RequestToken(token_key=auth.request_token.key, token_secret=auth.request_token.secret)
        request_token.put()
        self.redirect(auth_url)

# ログアウト処理
class OauthLogout(webapp.RequestHandler):
    def get(self):
        cookie = get_cookie()
        if cookie.has_key('sid'):
            memcache.delete(cookie['sid'].value) #@UndefinedVariable
            del cookie['sid']
        self.redirect('/')

# ログインコールバック処理
class OauthLoginCallBack(webapp.RequestHandler):
    def get(self):
        request_token_key = self.request.get("oauth_token")
        request_verifier = self.request.get('oauth_verifier')
        if not request_token_key:
            self.redirect('/')
            return

        request_token = RequestToken.gql("WHERE token_key=:1", request_token_key).get()
        request_token.delete()

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_request_token(request_token.token_key, request_token.token_secret)
        access_token = auth.get_access_token(request_verifier)
        cookie = get_cookie()
        memcache.set(cookie['sid'].value, access_token, SESSION_EXPIRE) #@UndefinedVariable

        twitter_user = get_twitter_data(cookie)
        user = User.get_or_insert(key_name=User.create_key(twitter_user['id']),
                                  userId=twitter_user['id'])
        user.accessToken = access_token.key
        user.accessSecret = access_token.secret
        user.screenName=twitter_user['screen_name']
        user.image=twitter_user['profile_image_url']
        user.put()

        self.redirect('/')

# リスト表示
class ListPage(webapp.RequestHandler):
    def get(self):
        index = strToInt(self.request.get('index'))
        openStage = strToInt(self.request.get('open'))
        
        cookie = get_cookie()
        twitter_user = get_user(cookie)

        summary = {}
        summary['count'] = KyouenPuzzleSummary.all().get().count or 0
        summary['index'] = index
        summary['open'] = openStage

        template_values = {
                           'summary': summary,
                           }
        if not twitter_user:
            template_values['user'] = twitter_user

        render_page(self, 'list.html', template_values)

    def post(self):
        self.get(self)

class ListStages(webapp.RequestHandler):
    def post(self):
        index = strToInt(self.request.get('index'))
        
        cookie = get_cookie()
        twitter_user = get_user(cookie)

        puzzle_query = KyouenPuzzle.all().filter('stageNo >', index).order('stageNo')
        puzzles = puzzle_query.fetch(limit=10)
        if twitter_user:
            user = User.get_by_key_name(User.create_key(twitter_user.userId))
            for p in puzzles:
                clear = StageUser.gql("WHERE stage = :1 AND user = :2", p, user).get()
                if clear:
                    p.clear = '1'

        json = simplejson.dumps([dict(stageNo=p.stageNo,
                                      size=p.size,
                                      stage=p.stage,
                                      creator=p.creator,
                                      registDate=templatefilters.jst(p.registDate).strftime('%Y/%m/%d %H:%M:%S'),
                                      clear=p.clear if hasattr(p, 'clear') else '0',
                                      ) for p in puzzles])
        self.response.out.write(json)

class AddStageUser(webapp.RequestHandler):
    def post(self):
        stageNo = strToInt(self.request.get("stageNo"))
        logging.info('stageNo=' + str(stageNo))
        stage = KyouenPuzzle.all().filter('stageNo =', stageNo).get()
        cookie = get_cookie()
        user = get_user(cookie)
        if not user:
            user = User.get_or_insert(key_name=User.create_key('0'),
                                      userId='0',
                                      screenName='Guest',
                                      image='http://my-android-server.appspot.com/image/icon.png')
        stage_user = StageUser.gql('WHERE stage = :1 AND user = :2', stage, user).get()
        if not stage_user:
            # 存在しない場合は新規作成
            stage_user = StageUser(stage=stage,
                                   user=user)
            # 新規クリア時はUser.clearStageCountをインクリメント
            count = user.clearStageCount
            if not count:
                count = StageUser.gql('WHERE user = :1', user).count()
            user.clearStageCount = count + 1
            user.put()
        stage_user.put()

class ListRanking(webapp.RequestHandler):
    def post(self):
        users = User.all().order('-clearStageCount')
        
        json = simplejson.dumps([dict(screenName=u.screenName,
                                      image=u.image,
                                      clearStageCount=u.clearStageCount,
                                      ) for u in users])
        self.response.out.write(json)

# インデックスページ表示
class IndexPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        
        # 最近の登録
        recent = KyouenPuzzle.gql('ORDER BY stageNo DESC').fetch(limit=10)
        for r in recent:
            r.index = (r.stageNo - 1) - (r.stageNo - 1) % 10
        template_values['recent'] = recent
        
        # アクティビティ
        activity = StageUser.gql('ORDER BY clearDate DESC').fetch(limit=20)
        template_values['activity'] = activity
        
        render_page(self, 'index.html', template_values)

    def post(self):
        self.get(self)

class StaticPage(webapp.RequestHandler):
    def get(self, value=None):
        if not value:
            value = 'index.html'

        render_page(self, value)

    def post(self):
        self.get(self)

# ステージ作成テスト
class TestAdd(webapp.RequestHandler):
    def get(self):
        self.test()
        return
        
        # http://my-android-server.appspot.com/page/test_add?stage=31&size=6&stage=000000000000111111000000000000000000&creator=no_name
        stageNo = int(self.request.get('stageNo'))
        size = int(self.request.get('size'))
        stage = self.request.get('stage')
        creator = self.request.get('creator')
        KyouenPuzzle(stageNo=stageNo,
                     size=size,
                     stage=stage,
                     creator=creator).put()

    def test(self):
        c = KyouenPuzzle.all().count()
        summary = KyouenPuzzleSummary(count=c)
        summary.put()
        if KyouenPuzzle.all().count() != 0:
            return
        data = u"""1,6,000000010000001100001100000000001000,noboru
2,6,000000000000000100010010001100000000,noboru
3,6,000000001000010000000100010010001000,noboru
4,6,001000001000000010010000010100000000,noboru
5,6,000000001011010000000010001000000010,noboru
6,6,000100000000101011010000000000000000,noboru
7,6,000000001010000000010010000000001010,noboru
8,6,001000000001010000010010000001000000,noboru
9,6,000000001000010000000010000100001000,noboru
10,6,000100000010010000000100000010010000,noboru
11,6,010001000000001010000000010000000000,noboru
12,6,001010000000010001000010001000000100,noboru
13,6,000100000010001000000100010010001000,noboru
14,6,000010000100001000001010010000001000,noboru
15,6,000000010010000000100010000100001000,noboru
16,6,000000000100001000010010000000000100,noboru
17,6,000000010000001010000000010000001010,noboru
18,6,000010010000000100100000010100000000,noboru
19,6,001000100001000000010001000000000100,noboru
20,6,000010010001001000000100000000001000,noboru
21,6,000000010100000010000000001000010010,noboru
22,6,000100000000011000001000000010010100,noboru
23,6,000010000010010000000000100001001000,noboru
24,9,000000001001010000000000000010000000001000100000100000010000001000001000000000000,noboru
25,6,010000100000010000001000001000000110,no name
26,6,001000010000000000001000000100010001,noboru
27,9,000000100000000000001000001000010000000000000000101000000000000001010000000000001,no name
28,6,000000001000010100000010001000000000,no name
29,6,010100000100010000000010001000001000,noboru
30,6,100000000000010101101000000010010000,りゅう
31,6,000000010000001100001100000000001000,noboru
32,6,000000000000000100010010001100000000,noboru
33,6,000000001000010000000100010010001000,noboru
34,6,001000001000000010010000010100000000,noboru
35,6,000000001011010000000010001000000010,noboru
36,6,000100000000101011010000000000000000,noboru
37,6,000000001010000000010010000000001010,noboru
38,6,001000000001010000010010000001000000,noboru
39,6,000000001000010000000010000100001000,noboru
40,6,000100000010010000000100000010010000,noboru
41,6,010001000000001010000000010000000000,noboru
42,6,001010000000010001000010001000000100,noboru
43,6,000100000010001000000100010010001000,noboru
44,6,000010000100001000001010010000001000,noboru
45,6,000000010010000000100010000100001000,noboru
46,6,000000000100001000010010000000000100,noboru
47,6,000000010000001010000000010000001010,noboru
48,6,000010010000000100100000010100000000,noboru
49,6,001000100001000000010001000000000100,noboru
50,6,000010010001001000000100000000001000,noboru
51,6,000000010100000010000000001000010010,noboru
52,6,000100000000011000001000000010010100,noboru
53,6,000010000010010000000000100001001000,noboru
54,9,000000001001010000000000000010000000001000100000100000010000001000001000000000000,noboru
55,6,010000100000010000001000001000000110,no name
56,6,001000010000000000001000000100010001,noboru
57,9,000000100000000000001000001000010000000000000000101000000000000001010000000000001,no name
58,6,000000001000010100000010001000000000,no name
59,6,010100000100010000000010001000001000,noboru
60,6,100000000000010101101000000010010000,aaa
61,6,000000010000001100001100000000001000,noboru
62,6,000000000000000100010010001100000000,noboru
63,6,000000001000010000000100010010001000,noboru
64,6,001000001000000010010000010100000000,noboru
65,6,000000001011010000000010001000000010,noboru
66,6,000100000000101011010000000000000000,noboru
67,6,000000001010000000010010000000001010,noboru
68,6,001000000001010000010010000001000000,noboru
69,6,000000001000010000000010000100001000,noboru
70,6,000100000010010000000100000010010000,noboru
71,6,000000010000001100001100000000001000,noboru
72,6,000000000000000100010010001100000000,noboru
73,6,000000001000010000000100010010001000,noboru
74,6,001000001000000010010000010100000000,noboru
75,6,000000001011010000000010001000000010,noboru
76,6,000100000000101011010000000000000000,noboru
77,6,000000001010000000010010000000001010,noboru
78,6,001000000001010000010010000001000000,noboru
79,6,000000001000010000000010000100001000,noboru
80,6,000100000010010000000100000010010000,noboru
81,6,000000010000001100001100000000001000,noboru
82,6,000000000000000100010010001100000000,noboru
83,6,000000001000010000000100010010001000,noboru
84,6,001000001000000010010000010100000000,noboru
85,6,000000001011010000000010001000000010,noboru
86,6,000100000000101011010000000000000000,noboru
87,6,000000001010000000010010000000001010,noboru
88,6,001000000001010000010010000001000000,noboru
89,6,000000001000010000000010000100001000,noboru
90,6,000100000010010000000100000010010000,noboru
91,6,000000010000001100001100000000001000,noboru
92,6,000000000000000100010010001100000000,noboru
93,6,000000001000010000000100010010001000,noboru
94,6,001000001000000010010000010100000000,noboru
95,6,000000001011010000000010001000000010,noboru
96,6,000100000000101011010000000000000000,noboru
97,6,000000001010000000010010000000001010,noboru
98,6,001000000001010000010010000001000000,noboru
99,6,000000001000010000000010000100001000,noboru
100,6,000100000010010000000100000010010000,noboru
101,6,000000010000001100001100000000001000,noboru
102,6,000000000000000100010010001100000000,noboru
103,6,000000001000010000000100010010001000,noboru
104,6,001000001000000010010000010100000000,noboru
105,6,000000001011010000000010001000000010,noboru
106,6,000100000000101011010000000000000000,noboru
107,6,000000001010000000010010000000001010,noboru
108,6,001000000001010000010010000001000000,noboru
109,6,000000001000010000000010000100001000,noboru
110,6,000100000010010000000100000010010000,noboru
111,6,000000010000001100001100000000001000,noboru
112,6,000000000000000100010010001100000000,noboru
113,6,000000001000010000000100010010001000,noboru
114,6,001000001000000010010000010100000000,noboru
115,6,000000001011010000000010001000000010,noboru
116,6,000100000000101011010000000000000000,noboru
117,6,000000001010000000010010000000001010,noboru
118,6,001000000001010000010010000001000000,noboru
119,6,000000001000010000000010000100001000,noboru
120,6,000100000010010000000100000010010000,noboru
121,6,000000010000001100001100000000001000,noboru
122,6,000000000000000100010010001100000000,noboru
123,6,000000001000010000000100010010001000,noboru
124,6,001000001000000010010000010100000000,noboru
125,6,000000001011010000000010001000000010,noboru
126,6,000100000000101011010000000000000000,noboru
127,6,000000001010000000010010000000001010,noboru
128,6,001000000001010000010010000001000000,noboru
129,6,000000001000010000000010000100001000,noboru
130,6,000100000010010000000100000010010000,noboru
131,6,000000010000001100001100000000001000,noboru
132,6,000000000000000100010010001100000000,noboru
133,6,000000001000010000000100010010001000,noboru
134,6,001000001000000010010000010100000000,noboru
135,6,000000001011010000000010001000000010,noboru
136,6,000100000000101011010000000000000000,noboru
137,6,000000001010000000010010000000001010,noboru
138,6,001000000001010000010010000001000000,noboru
139,6,000000001000010000000010000100001000,noboru
140,6,000100000010010000000100000010010000,noboru
141,6,000000010000001100001100000000001000,noboru
142,6,000000000000000100010010001100000000,noboru
143,6,000000001000010000000100010010001000,noboru
144,6,001000001000000010010000010100000000,noboru
145,6,000000001011010000000010001000000010,noboru
146,6,000100000000101011010000000000000000,noboru
147,6,000000001010000000010010000000001010,noboru
148,6,001000000001010000010010000001000000,noboru
149,6,000000001000010000000010000100001000,noboru
150,6,000000001000010000000010000100001000,noboru"""
        list_data = data.split('\n')
        for l in list_data:
            d = l.split(',')
            puzzle = KyouenPuzzle(stageNo=int(d[0]),
                                  size=int(d[1]),
                                  stage=d[2],
                                  creator=d[3])
            puzzle.put()

application = webapp.WSGIApplication([('/', IndexPage),
                                      ('/index.html', IndexPage),
                                      ('/page/list.html', ListPage),
                                      ('/page/list', ListStages),
                                      ('/page/add', AddStageUser),
                                      ('/page/ranking', ListRanking),
                                      ('/page/login', OauthLogin),
                                      ('/page/login_callback', OauthLoginCallBack),
                                      ('/page/logout', OauthLogout),
#                                      ('/page/test_add', TestAdd),
                                      ('/page/(.*)', StaticPage),
                                      ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

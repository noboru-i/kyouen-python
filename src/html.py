#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
import logging
import Cookie
import tweepy
import uuid
import datetime
from django.utils import simplejson
from google.appengine.ext import webapp, db
from google.appengine.api import memcache
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from kyouenserver import KyouenPuzzle, KyouenPuzzleSummary
from app import templatefilters
from const import Const

SESSION_EXPIRE = 60 * 60 * 24 * 20 # 60日

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
    clearDate = db.DateTimeProperty(required=True)

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
        auth = tweepy.OAuthHandler(Const.CONSUMER_KEY, Const.CONSUMER_SECRET)
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
        auth = tweepy.OAuthHandler(Const.CONSUMER_KEY, Const.CONSUMER_SECRET)
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

        auth = tweepy.OAuthHandler(Const.CONSUMER_KEY, Const.CONSUMER_SECRET)
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

# APIでのログイン処理
class ApiLogin(webapp.RequestHandler):
    def post(self):
        request_token = self.request.get("token")
        request_token_secret = self.request.get('token_secret')
        if not request_token:
            self.response.content_type = 'application/json'
            responseJson = {'message': 'invalid parameter'}
            simplejson.dump(responseJson, self.response.out, ensure_ascii=False)
            return

        # memcacheへ認証情報を設定
        from tweepy import oauth
        access_token = oauth.OAuthToken(request_token, request_token_secret)
        cookie = set_uuid(self)
        memcache.set(cookie['sid'].value, access_token, SESSION_EXPIRE) #@UndefinedVariable

        # DBへユーザ情報を登録
        twitter_user = get_twitter_data(cookie)
        user = User.get_or_insert(key_name=User.create_key(twitter_user['id']),
                                  userId=twitter_user['id'])
        user.accessToken = access_token.key
        user.accessSecret = access_token.secret
        user.screenName=twitter_user['screen_name']
        user.image=twitter_user['profile_image_url']
        user.put()

        self.response.content_type = 'application/json'
        responseJson = {'message': 'success',
                        'user': {'id': user.userId,
                                 'image': user.image}}
        simplejson.dump(responseJson, self.response.out, ensure_ascii=False)
        return

# クリア情報の追加
# @param data: [
#   {
#     "stageNo": 1,
#     "clearDate": "2012-01-01 00:00:00"
#   }
# ]
class AddAllStageUser(webapp.RequestHandler):
    def post(self):
        data = simplejson.loads(self.request.get('data'))

        # ユーザ情報を取得
        cookie = get_cookie()
        user = get_user(cookie)
        if not user:
            responseJson = {'message' : 'not authentication'}
            simplejson.dump(responseJson, self.response.out, ensure_ascii=False)
            return
        # 送信されたステージ情報を登録
        clearStageNoList = [];
        for stage in data:
            stageNo = strToInt(stage['stageNo'])
            clearDate = stage['clearDate']
            logging.info('stageNo=' + str(stageNo))
            # クリアステージ追加
            if stageNo is 0:
                logging.error('invalid parameter')
                continue
            stage = KyouenPuzzle.all().filter('stageNo =', stageNo).get()
            stage_user = StageUser.gql('WHERE stage = :1 AND user = :2', stage, user).get()
            if not stage_user:
                # 存在しない場合は新規作成
                stage_user = StageUser(stage = stage,
                                       user = user,
                                       clearDate = datetime.datetime.strptime(clearDate, '%Y-%m-%d %H:%M:%S'))
                # 新規クリア時はUser.clearStageCountをインクリメント
                count = user.clearStageCount
                if not count:
                    count = StageUser.gql('WHERE user = :1', user).count()
                user.clearStageCount = count + 1
                user.put()
            stage_user.clearDate = datetime.datetime.strptime(clearDate, '%Y-%m-%d %H:%M:%S')
            stage_user.put()
            clearStageNoList.append(stageNo)

        # 送信されていないステージ情報を返す
        stageUsers = StageUser.gql('WHERE user = :1', user)
        syncStageList = []
        for stageUser in stageUsers:
            stage = stageUser.stage
            if stage.stageNo not in clearStageNoList:
                syncStageList.append({'stageNo' : stage.stageNo,
                                      'clearDate' : stageUser.clearDate.strftime('%Y-%m-%d %H:%M:%S')})
        responseJson = {'message' : 'success',
                        'data' : syncStageList}
        simplejson.dump(responseJson, self.response.out, ensure_ascii=False)
        return

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
        summary['pager'] = [{
                             'label': str((i*10)+1) + '〜' + str((i+1)*10),
                             'function': 'javascript:loadStage('+str((i+1)*10)+')',
                             } for i in range(summary['count'] /10)]

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
        if stageNo is 0:
            logging.error('invalid parameter')
            return
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
                                   user=user,
                                   clearDate = datetime.datetime.today())
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
        def _groupby_user(stage_user):
            return {'screenName':stage_user.user.screenName, 'image':stage_user.user.image}
        import itertools
        activity = [(name, list(stageusers))
                    for name, stageusers in itertools.groupby(StageUser.gql('ORDER BY clearDate DESC').fetch(limit=200), _groupby_user)]
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

application = webapp.WSGIApplication([('/', IndexPage),
                                      ('/index.html', IndexPage),
                                      ('/page/list.html', ListPage),
                                      ('/page/list', ListStages),
                                      ('/page/add', AddStageUser),
                                      ('/page/ranking', ListRanking),
                                      ('/page/login', OauthLogin),
                                      ('/page/login_callback', OauthLoginCallBack),
                                      ('/page/logout', OauthLogout),
                                      ('/page/api_login', ApiLogin),
                                      ('/page/add_all', AddAllStageUser),
                                      ('/page/(.*)', StaticPage),
                                      ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

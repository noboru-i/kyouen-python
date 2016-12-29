#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
import logging
import Cookie
import tweepy
import uuid
import datetime
import jinja2
import webapp2
import json
from google.appengine.api import memcache

from models import KyouenPuzzle, KyouenPuzzleSummary, RequestToken, User, StageUser
from const import Const

SESSION_EXPIRE = 60 * 60 * 24 * 20 # 60日

USER_KEY_PREFIX = 'KEY'

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'template')),
    extensions=['jinja2.ext.autoescape'])

from app import templatefilters
JINJA_ENVIRONMENT.filters['jst'] = templatefilters.jst
JINJA_ENVIRONMENT.filters['list_link'] = templatefilters.list_link

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

    template = JINJA_ENVIRONMENT.get_template(page)
    handler.response.out.write(template.render(template_values))

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
class OauthLogin(webapp2.RequestHandler):
    def get(self):
        auth = tweepy.OAuthHandler(Const.CONSUMER_KEY, Const.CONSUMER_SECRET)
        auth_url = auth.get_authorization_url()
        request_token = RequestToken(token_key=auth.request_token.key, token_secret=auth.request_token.secret)
        request_token.put()
        self.redirect(auth_url)

# ログアウト処理
class OauthLogout(webapp2.RequestHandler):
    def get(self):
        cookie = get_cookie()
        if cookie.has_key('sid'):
            memcache.delete(cookie['sid'].value) #@UndefinedVariable
            del cookie['sid']
        self.redirect('/')

# ログインコールバック処理
class OauthLoginCallBack(webapp2.RequestHandler):
    def get(self):
        request_token_key = self.request.get("oauth_token")
        request_verifier = self.request.get('oauth_verifier')
        if not request_token_key:
            self.redirect('/')
            return

        request_token = RequestToken.gql("WHERE token_key=:1", request_token_key).get()
        request_token.key.delete()

        auth = tweepy.OAuthHandler(Const.CONSUMER_KEY, Const.CONSUMER_SECRET)
        auth.set_request_token(request_token.token_key, request_token.token_secret)
        access_token = auth.get_access_token(request_verifier)
        cookie = get_cookie()
        memcache.set(cookie['sid'].value, access_token, SESSION_EXPIRE) #@UndefinedVariable

        twitter_user = get_twitter_data(cookie)
        user = User.get_or_insert(User.create_key(twitter_user['id']),
                                  userId=twitter_user['id'])
        user.accessToken = access_token.key
        user.accessSecret = access_token.secret
        user.screenName=twitter_user['screen_name']
        user.image=twitter_user['profile_image_url']
        user.put()

        self.redirect('/')

# APIでのログイン処理
class ApiLogin(webapp2.RequestHandler):
    def post(self):
        request_token = self.request.get("token")
        request_token_secret = self.request.get('token_secret')
        if not request_token:
            self.response.content_type = 'application/json'
            responseJson = {'message': 'invalid parameter'}
            self.response.write(json.dumps(responseJson))
            return

        # memcacheへ認証情報を設定
        from tweepy import oauth
        access_token = oauth.OAuthToken(request_token, request_token_secret)
        cookie = set_uuid(self)
        memcache.set(cookie['sid'].value, access_token, SESSION_EXPIRE) #@UndefinedVariable

        # DBへユーザ情報を登録
        twitter_user = get_twitter_data(cookie)
        user = User.get_or_insert(User.create_key(twitter_user['id']),
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
        self.response.write(json.dumps(responseJson))
        return

# クリア情報の追加
# @param data: [
#   {
#     "stageNo": 1,
#     "clearDate": "2012-01-01 00:00:00"
#   }
# ]
class AddAllStageUser(webapp2.RequestHandler):
    def post(self):
        data = json.loads(self.request.get('data'))

        # ユーザ情報を取得
        cookie = get_cookie()
        user = get_user(cookie)
        if not user:
            responseJson = {'message' : 'not authentication'}
            self.response.write(json.dumps(responseJson))
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
            stage = KyouenPuzzle.query(KyouenPuzzle.stageNo == stageNo).get()
            stage_user = StageUser.gql('WHERE stage = :1 AND user = :2', stage.key, user.key).get()
            if not stage_user:
                # 存在しない場合は新規作成
                stage_user = StageUser(stage = stage.key,
                                       user = user.key,
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
        stageUsers = StageUser.gql('WHERE user = :1', user.key)
        syncStageList = []
        for stageUser in stageUsers:
            stage = stageUser.stage.get()
            if stage.stageNo not in clearStageNoList:
                syncStageList.append({'stageNo' : stage.stageNo,
                                      'clearDate' : stageUser.clearDate.strftime('%Y-%m-%d %H:%M:%S')})
        responseJson = {'message' : 'success',
                        'data' : syncStageList}
        self.response.write(json.dumps(responseJson))
        return

class AddStageUser(webapp2.RequestHandler):
    def post(self):
        stageNo = strToInt(self.request.get("stageNo"))
        logging.info('stageNo=' + str(stageNo))
        if stageNo is 0:
            logging.error('invalid parameter')
            return
        stage = KyouenPuzzle.query(KyouenPuzzle.stageNo == stageNo).get()
        cookie = get_cookie()
        user = get_user(cookie)
        if not user:
            user = User.get_or_insert(User.create_key('0'),
                                      userId='0',
                                      screenName='Guest',
                                      image='http://my-android-server.appspot.com/image/icon.png')
        stage_user = StageUser.gql('WHERE stage = :1 AND user = :2', stage.key, user.key).get()
        if not stage_user:
            # 存在しない場合は新規作成
            stage_user = StageUser(stage=stage.key,
                                   user=user.key,
                                   clearDate=datetime.datetime.today())
            # 新規クリア時はUser.clearStageCountをインクリメント
            count = user.clearStageCount
            if not count:
                count = StageUser.gql('WHERE user = :1', user).count()
            user.clearStageCount = count + 1
            user.put()
        else:
            stage_user.clearDate = datetime.datetime.today()
        stage_user.put()

application = webapp2.WSGIApplication([('/page/add', AddStageUser),
                                      ('/page/login', OauthLogin),
                                      ('/page/login_callback', OauthLoginCallBack),
                                      ('/page/logout', OauthLogout),
                                      ('/page/api_login', ApiLogin),
                                      ('/page/add_all', AddAllStageUser),
                                      ], debug=True)

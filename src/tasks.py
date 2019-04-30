#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
import logging
import tweepy
import webapp2
import json
from google.appengine.ext import ndb

from models import RegistModel, GcmModel, ApnsModel
from const import Const

# twitterに投稿
def post_twitter(message):
    auth = tweepy.OAuthHandler(Const.TWITTER_SHARE_CONSUMER_KEY, Const.TWITTER_SHARE_CONSUMER_SECRET)
    auth.set_access_token(Const.TWITTER_SHARE_ACCESS_KEY, Const.TWITTER_SHARE_ACCESS_SECRET)
    api = tweepy.API(auth_handler=auth)
    api.update_status(message)
    return

def sendFcmAll():
    from google.appengine.api import urlfetch
    import urllib
    from oauth2client.service_account import ServiceAccountCredentials

    SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'certificate/api-project-1046368181881-firebase-adminsdk-df1u6-8141bfec61.json', SCOPES)
    access_token_info = credentials.get_access_token()

    form_fields = {
        'message': {
            'topic': 'all',
            'notification': {
                'title': '新規ステージが追加されました。'
            }
        }
    }
    form_data = json.dumps(form_fields)
    result = urlfetch.fetch(url='https://fcm.googleapis.com/v1/projects/api-project-1046368181881/messages:send',
                            payload=form_data,
                            method=urlfetch.POST,
                            headers={
                                     'Content-Type': 'application/json; UTF-8',
                                     'Authorization': 'Bearer ' + access_token_info.access_token
                                     })
    logging.debug('content=' + str(result.content) + ', statusCode=' + str(result.status_code))
    return result

class TweetTask(webapp2.RequestHandler):
    def get(self):
        max_disp = 5

        query = RegistModel.query().order(RegistModel.registDate)
        s = set(m.stageInfo.get().creator for m in query)
        if len(s) == 0:
            # 登録されてない場合、終了
            return

        length = len(s)
        creator = ','.join(list(s)[:max_disp])
        if length > max_disp:
            creator += u' たち'

        query = RegistModel.query().order(RegistModel.registDate)
        l = [m.stageInfo.get().stageNo for m in query]
        stage = str(l[0])
        if len(l) > 1:
            stage += u'～' + str(max(l))

        misStageNo = min(l) - 1
        minStageNo = misStageNo - misStageNo % 10
        import math
        pageNo = math.floor((minStageNo - 1) / 10) + 1
        message = (creator + u'によって、ステージ：' + stage + u'が登録されました。 '
                   u'http://kyouen.app/html/list.html?page_no=%d&open=%d #共円') % (pageNo, min(l))
        logging.info('message=' + message)

        try:
            # twitterに投稿
            post_twitter(message)
        except:
            return

        # 情報削除
        query = RegistModel.query().order(RegistModel.registDate)
        ndb.delete_multi([m.key for m in query])

        # FCMで送信
        sendFcmAll()
        return

application = webapp2.WSGIApplication([('/tasks/tweet', TweetTask),
                                       ], debug=True)

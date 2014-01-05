#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
import logging
import tweepy
import webapp2
from google.appengine.ext import db

from kyouenserver import RegistModel
from const import Const
from gcmserver import GcmModel
from apnsserver import ApnsModel

# https://github.com/djacobs/PyAPNs/blob/master/apns.py
from libs.pyapns.apns import APNs, Payload, PayloadAlert

# twitterに投稿
def post_twitter(message):
    auth = tweepy.OAuthHandler(Const.TWITTER_SHARE_CONSUMER_KEY, Const.TWITTER_SHARE_CONSUMER_SECRET)
    auth.set_access_token(Const.TWITTER_SHARE_ACCESS_KEY, Const.TWITTER_SHARE_ACCESS_SECRET)
    api = tweepy.API(auth_handler=auth)
    api.update_status(message)
    return

def sendGcm(gcmModel):
    from google.appengine.api import urlfetch
    import urllib

    form_fields = {
                   "registration_id": gcmModel.registrationId,
                   "collapse_key": "update",
                   "data.message": "gcm message!!!"
    }
    form_data = urllib.urlencode(form_fields)
    result = urlfetch.fetch(url='https://android.googleapis.com/gcm/send',
                            payload=form_data,
                            method=urlfetch.POST,
                            headers={
                                     'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                                     'Authorization': 'key=' + Const.GCM_API_KEY
                                     })
    logging.debug('regId=' + gcmModel.registrationId + ', statusCode=' + str(result.status_code))
    return result

def sendGcmAll():
    query = GcmModel.all()
    for m in query:
        sendGcm(m)

    return True

def sendApns(self, apnsModel):
    #apns = APNs(use_sandbox=False, cert_file='certificate/aps_production.pem')  # 本番
    apns = APNs(use_sandbox=True, cert_file='certificate/aps_development.pem') # サンドボックス
    token_hex = apnsModel.deviceToken

    loc_key = 'notification_new_stage'
    badge = 1
    alert = PayloadAlert(None, loc_key=loc_key)
    payload = Payload(alert=alert, badge=badge)

    apns.gateway_server.send_notification(token_hex, payload)
    self.response.write(u"Sent a notification message.")

    logging.debug('regId=' + token_hex)

def sendApnsAll():
    query = ApnsModel.all()
    for m in query:
        sendApns(m)
    return True

class TweetTask(webapp2.RequestHandler):
    def get(self):
        max_disp = 5

        query = RegistModel.all().order('registDate')
        s = set(m.stageInfo.creator for m in query)
        if len(s) == 0:
            # 登録されてない場合、終了
            return

        length = len(s)
        creator = ','.join(list(s)[:max_disp])
        if length > max_disp:
            creator += u' たち'

        query = RegistModel.all().order('registDate')
        l = [m.stageInfo.stageNo for m in query]
        stage = str(l[0])
        if len(l) > 1:
            stage += u'～' + str(max(l))

        misStageNo = min(l) - 1
        minStageNo = misStageNo - misStageNo % 10
        message = (creator + u'によって、ステージ：' + stage + u'が登録されました。 '
                   u'http://my-android-server.appspot.com/page/list.html?index=%d&open=%d #共円') % (minStageNo, min(l))
        logging.info('message=' + message)
        
        try:
            # twitterに投稿
            post_twitter(message)
            
            # 情報削除
            query = RegistModel.all().order('registDate')
            for m in query:
                db.delete(m)
        except:
            pass

        # GCMで送信
        sendGcmAll()
        # APNSで送信
        sendApnsAll()
        return

application = webapp2.WSGIApplication([('/tasks/tweet', TweetTask),
                                      ], debug=True)

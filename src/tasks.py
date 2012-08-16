#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
import logging
import tweepy
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app

from kyouenserver import RegistModel
from const import Const

# twitterに投稿
def post_twitter(message):
    auth = tweepy.OAuthHandler(Const.CONSUMER_KEY, Const.CONSUMER_SECRET)
    auth.set_access_token(Const.ACCESS_KEY, Const.ACCESS_SECRET)
    api = tweepy.API(auth_handler=auth)
    api.update_status(message)
    return


class TweetTask(webapp.RequestHandler):
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
        return

application = webapp.WSGIApplication([('/tasks/tweet', TweetTask),
                                      ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
import logging
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson

# GCMモデル
class GcmModel(db.Model):
    # 登録ID
    registrationId = db.StringProperty()
    # 登録日
    registDate = db.DateTimeProperty(auto_now_add=True)

# 登録処理
class GcmRegist(webapp.RequestHandler):

    # GETリクエストを処理します。
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('get not supported')
        return

    # POSTリクエストを処理します。
    def post(self):
        # パラメータを取得
        regId = self.request.get('regId')
        logging.debug("post regId:" + regId)

        if len(regId) == 0:
            # IDが取得できなかった場合
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('empty')
            return

        # 入力データの登録    
        model = GcmModel(registrationId=regId)
        model.put()

        # レスポンスの返却
        self.response.content_type = 'application/json'
        responseJson = {'message': 'success'}
        simplejson.dump(responseJson, self.response.out, ensure_ascii=False)
        return

class GcmUnregist(webapp.RequestHandler):
    # GETリクエストを処理します。
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('get not supported')
        return
    # POSTリクエストを処理します。
    def post(self):
        # パラメータを取得
        regId = self.request.get('regId')
        logging.debug("post regId:" + regId)

        if len(regId) == 0:
            # IDが取得できなかった場合
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('empty')
            return

        # データの削除
        model = GcmModel.gql("WHERE registrationId = :1", regId).get()
        if (model is None):
            # モデルが取得できなかった場合
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('empty')
        model.delete()

        # レスポンスの返却
        self.response.content_type = 'application/json'
        responseJson = {'message': 'success'}
        simplejson.dump(responseJson, self.response.out, ensure_ascii=False)
        return

application = webapp.WSGIApplication([('/gcm/regist', GcmRegist),
                                      ('/gcm/unregist', GcmUnregist),
                                      ], debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

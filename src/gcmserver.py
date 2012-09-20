#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
import logging
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson

from const import Const

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
            return
        model.delete()

        # レスポンスの返却
        self.response.content_type = 'application/json'
        responseJson = {'message': 'success'}
        simplejson.dump(responseJson, self.response.out, ensure_ascii=False)
        return

class GcmSendMessage(webapp.RequestHandler):
    def sendGcm(self, gcmModel):
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
    def get(self):
        self.post()
    def post(self):
        query = GcmModel.all()
        for m in query:
            self.sendGcm(m)

        # レスポンスの返却
        self.response.content_type = 'application/json'
        responseJson = {'message': 'success'}
        simplejson.dump(responseJson, self.response.out, ensure_ascii=False)
        return

application = webapp.WSGIApplication([('/gcm/regist', GcmRegist),
                                      ('/gcm/unregist', GcmUnregist),
                                      ('/gcm/send', GcmSendMessage)
                                      ], debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

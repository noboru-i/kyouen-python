#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
import logging
import webapp2
import json
from google.appengine.ext import db

# APNSモデル
class ApnsModel(db.Model):
    # 登録ID
    deviceToken = db.StringProperty()
    # 登録日
    registDate = db.DateTimeProperty(auto_now_add=True)

# 登録処理
class ApnsRegist(webapp2.RequestHandler):

    # GETリクエストを処理します。
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('get not supported')
        return

    # POSTリクエストを処理します。
    def post(self):
        # パラメータを取得
        device_token = self.request.get('device_token')
        logging.debug("post device_token:" + device_token)

        if not device_token:
            # IDが取得できなかった場合
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('empty')
            return

        # 既に登録されているか確認
        model = ApnsModel.gql("WHERE deviceToken = :1", device_token).get()
        if (model is not None):
            # レスポンスの返却
            self.response.content_type = 'application/json'
            responseJson = {'message': 'already registed'}
            self.response.write(json.dumps(responseJson))
            return
        
        # 入力データの登録
        model = ApnsModel(deviceToken=device_token)
        model.put()

        # レスポンスの返却
        self.response.content_type = 'application/json'
        responseJson = {'message': 'success'}
        self.response.write(json.dumps(responseJson))
        return

class ApnsUnregist(webapp2.RequestHandler):
    # GETリクエストを処理します。
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('get not supported')
        return
    # POSTリクエストを処理します。
    def post(self):
        # パラメータを取得
        device_token = self.request.get('device_token')
        logging.debug("post device_token:" + device_token)

        if not device_token:
            # IDが取得できなかった場合
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('empty')
            return

        # データの削除
        model = ApnsModel.gql("WHERE deviceToken = :1", device_token).get()
        if (model is None):
            # モデルが取得できなかった場合
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('empty')
            return
        model.delete()

        # レスポンスの返却
        self.response.content_type = 'application/json'
        responseJson = {'message': 'success'}
        self.response.write(json.dumps(responseJson))
        return

# TODO テスト用
class ApnsTestMessage(webapp2.RequestHandler):
    def get(self):
        from libs.pyapns.apns import APNs, Payload, PayloadAlert
        query = ApnsModel.all()
        apnsModel = query.fetch(1, 0)
        #apns = APNs(use_sandbox=False, cert_file='certificate/aps_production.pem')  # 本番
        apns = APNs(use_sandbox=True, cert_file='certificate/aps_development.pem') # サンドボックス
        token_hex = apnsModel[0].deviceToken

        loc_key = 'notification_new_stage'
        badge = 1
        alert = PayloadAlert(None, loc_key=loc_key)
        payload = Payload(alert=alert, badge=badge)

        apns.gateway_server.send_notification(token_hex, payload)
        self.response.write(u"Sent a notification message.")
        logging.debug('regId=' + token_hex)

application = webapp2.WSGIApplication([('/apns/regist', ApnsRegist),
                                      ('/apns/unregist', ApnsUnregist),
                                      ('/apns/test_message', ApnsTestMessage), # TODO テスト
                                      ], debug=True)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""リアルタイム対戦用のAPI.

置いた場所の受信や、一括返却など.
"""

import logging
import webapp2
import json
from google.appengine.ext import ndb

from html import User

# リアルタイム対戦の情報
class RealtimeBattleRoom(ndb.Model):
    # プレイヤー1
    player1 = ndb.KeyProperty(kind=User, required=True)
    # プレイヤー2
    player2 = ndb.KeyProperty(kind=User)
    # サイズ
    size = ndb.IntegerProperty(required=True)
    # ステージ上の石の配置
    stage = ndb.StringProperty(required=True)
    # 開始日
    startDate = ndb.DateTimeProperty(auto_now_add=True)
    # 更新日
    updateDate = ndb.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def created_battle(user_key):
        return RealtimeBattleRoom.query(RealtimeBattleRoom.player1 == user_key).get()

def to_dict(model):
    u"""modelをdictionaryに変換する."""
    output = {}

    if hasattr(model, '__iter__'):
        return [to_dict(item) for item in model]

    for key, prop in model._properties.iteritems():
        value = getattr(model, key)
        output[key] = unicode(value)

    output['id'] = model.key.id()

    return output

class Room(webapp2.RequestHandler):

    u"""対戦部屋の操作."""

    def get(self):
        u"""対戦部屋のリストを返却."""
        data = RealtimeBattleRoom.query().order(-RealtimeBattleRoom.startDate)
        output = []
        for battle in data:
            b = {
                'id': battle.key.id(),
                'size': battle.size,
                'stage': battle.stage,
                'startDate': unicode(battle.startDate),
                'updateDate': unicode(battle.updateDate)
            }
            player1 = User.get_by_id(battle.player1.id())
            b['player1'] = {
                'screenName': player1.screenName
            }
            if battle.player2 is not None:
                player2 = User.get_by_id(battle.player2.id())
                b['player2'] = {
                    'screenName': player2.screenName
                }
            output.append(b)
        self.response.out.write(json.dumps(output))

    def post(self):
        u"""対戦部屋を作成."""
        # ユーザ情報を取得
        from html import get_cookie
        from html import get_user
        cookie = get_cookie()
        user = get_user(cookie)
        if not user:
            import uuid
            self.response.set_cookie('sid', str(uuid.uuid4()))
            responseJson = {'loggedin': False}
            self.response.write(json.dumps(responseJson))
            return

        created_battle = RealtimeBattleRoom.created_battle(user.key)
        # if created_battle:
        #     responseJson = {'created': False, 'id': created_battle.key.id()}
        #     self.response.write(json.dumps(responseJson))
        #     return

        battle = RealtimeBattleRoom(player1=user.key, size=6, stage='000000000000000000000000000000000000')
        battle_key = battle.put()
        responseJson = to_dict(battle)
        self.response.out.write(json.dumps(responseJson))

class RoomJoin(webapp2.RequestHandler):

    u"""部屋に参加する."""

    def post(self):
        u"""部屋に参加する."""
        data = json.loads(self.request.body)

        # ユーザ情報を取得
        from html import get_cookie
        from html import get_user
        cookie = get_cookie()
        user = get_user(cookie)
        if not user:
            import uuid
            self.response.set_cookie('sid', str(uuid.uuid4()))
            responseJson = {'loggedin': False}
            self.response.write(json.dumps(responseJson))
            return

        battle = RealtimeBattleRoom.get_by_id(data['room_id'])

class Step(webapp2.RequestHandler):

    u"""石を置く."""

    def post(self):
        u"""石を置く."""
        logging.info('data %s', self.request.body)
        data = json.loads(self.request.body)

        # ユーザ情報を取得
        from html import get_cookie
        from html import get_user
        cookie = get_cookie()
        user = get_user(cookie)
        if not user:
            import uuid
            self.response.set_cookie('sid', str(uuid.uuid4()))
            responseJson = {'loggedin': False}
            self.response.write(json.dumps(responseJson))
            return
        logging.debug('data %s', data['x'])
        responseJson = 'x'
        self.response.out.write(json.dumps(responseJson))

application = webapp2.WSGIApplication([('/realtime/room', Room),
                                       ('/realtime/room/join', RoomJoin),
                                       ('/realtime/step', Step),
                                      ], debug=True)

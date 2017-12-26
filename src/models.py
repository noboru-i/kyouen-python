#!/usr/bin/env python
#-*- coding: utf-8 -*-
#

from google.appengine.ext import ndb

USER_KEY_PREFIX = 'KEY'

# パズルのステージ情報
class KyouenPuzzle(ndb.Model):
    # ステージ番号
    stageNo = ndb.IntegerProperty(required=True)
    # サイズ
    size = ndb.IntegerProperty(required=True)
    # ステージ上の石の配置
    stage = ndb.StringProperty(required=True)
    # 作者
    creator = ndb.StringProperty()
    # 登録日
    registDate = ndb.DateTimeProperty(auto_now_add=True)

# ステージ情報サマリ
class KyouenPuzzleSummary(ndb.Model):
    # ステージ合計
    count = ndb.IntegerProperty()
    # 最終更新日時
    lastDate = ndb.DateTimeProperty(auto_now_add=True)

# 登録情報
class RegistModel(ndb.Model):
    # ステージ情報
    stageInfo = ndb.KeyProperty(required=True, kind=KyouenPuzzle)
    # 登録日
    registDate = ndb.DateTimeProperty(required=True, auto_now_add=True)

class RequestToken(ndb.Model):
    token_key = ndb.StringProperty(required=True)
    token_secret = ndb.StringProperty(required=True)
    creation_date = ndb.DateTimeProperty(auto_now_add=True)

# ユーザデータ
class User(ndb.Model):
    userId = ndb.StringProperty(required=True)
    screenName = ndb.StringProperty()
    image = ndb.StringProperty()
    accessToken = ndb.StringProperty()
    accessSecret = ndb.StringProperty()
    clearStageCount = ndb.IntegerProperty()

    @staticmethod
    def create_key(userId):
        return(USER_KEY_PREFIX + userId)

# ステージ・ユーザ接続データ
class StageUser(ndb.Model):
    stage = ndb.KeyProperty(kind=KyouenPuzzle, required=True)
    user = ndb.KeyProperty(kind=User, required=True)
    clearDate = ndb.DateTimeProperty(required=True)

# APNSモデル
class ApnsModel(ndb.Model):
    # 登録ID
    deviceToken = ndb.StringProperty()
    # 登録日
    registDate = ndb.DateTimeProperty(auto_now_add=True)

# GCMモデル
class GcmModel(ndb.Model):
    # 登録ID
    registrationId = ndb.StringProperty()
    # 登録日
    registDate = ndb.DateTimeProperty(auto_now_add=True)

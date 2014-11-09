#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""APIレスポンスを返却するクラスを定義する.

一通りここに実装します.
"""

import logging
import webapp2
import json
import datetime
from google.appengine.ext import db

from kyouenserver import KyouenPuzzle, KyouenPuzzleSummary
from html import StageUser
from const import Const


SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)


def to_dict(model):
    u"""modelをdictionaryに変換する."""
    output = {}

    if hasattr(model, '__iter__'):
        return [to_dict(item) for item in model]

    for key, prop in model.properties().iteritems():
        value = getattr(model, key)
        output[key] = unicode(value)

    return output


class Login(webapp2.RequestHandler):

    u"""ログイン状態を取得する."""

    def get(self):
        u"""ログイン状態を取得する."""
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
        responseJson = {
            'userId': user.userId,
            'screenName': user.screenName,
            'image': user.image,
            'loggedin': True
        }
        self.response.out.write(json.dumps(responseJson))


class RecentStages(webapp2.RequestHandler):

    u"""最近の投稿を返却する.

    10件固定
    """

    def get(self):
        u""" 最近の投稿を返却する. """
        # 最近の登録
        recent = KyouenPuzzle.gql('ORDER BY stageNo DESC').fetch(limit=10)
        self.response.out.write(json.dumps(to_dict(recent)))


class Activities(webapp2.RequestHandler):

    u"""アクティビティを返却する.

    10件固定
    """

    def get(self):
        u"""アクティビティを返却する."""
        def _groupby_user(stage_user):
            return {'screenName': stage_user.user.screenName,
                    'image': stage_user.user.image}

        def _stageuser_to_dict(obj):
            return [{'clearDate': str(o.clearDate),
                     'stageNo': o.stage.stageNo}
                    for o in obj]
        stageUsers = StageUser.gql('ORDER BY clearDate DESC').fetch(limit=50)
        from itertools import groupby
        activities = [{'user': user,
                       'list': _stageuser_to_dict(stageusers)}
                      for user, stageusers
                      in groupby(stageUsers, _groupby_user)]
        self.response.out.write(json.dumps(activities))


class StageCount(webapp2.RequestHandler):

    u"""登録件数を取得する."""

    def get(self):
        u"""登録件数を取得する."""
        stages = {'count': KyouenPuzzleSummary.all().get().count}
        self.response.out.write(json.dumps(stages))


class Stages(webapp2.RequestHandler):

    u"""登録ステージ情報を取得する."""

    def get(self):
        u"""登録ステージ情報を取得する."""
        pageNo = strToInt(self.request.get('page_no'))
        page_per_count = 10

        from html import get_cookie
        from html import get_user
        cookie = get_cookie()
        twitter_user = get_user(cookie)

        puzzles = (KyouenPuzzle
                   .all()
                   .filter('stageNo >', (pageNo-1) * page_per_count)
                   .order('stageNo')
                   .fetch(limit=page_per_count))
        if twitter_user:
            from html import User
            user = User.get_by_key_name(User.create_key(twitter_user.userId))
            for p in puzzles:
                clear = StageUser.gql("WHERE stage = :1 AND user = :2", p, user).get()
                if clear:
                    p.clear = '1'
        response_json = [to_dict(p) for p in puzzles]
        self.response.out.write(json.dumps(response_json))


def strToInt(str1):
    u"""文字列を数値型に変換する."""
    return int(str1) if str1.isdigit() else 0

application = webapp2.WSGIApplication([
    ('/api/login', Login),
    ('/api/recent_stages', RecentStages),
    ('/api/activities', Activities),
    ('/api/stages/count', StageCount),
    ('/api/stages', Stages),
], debug=True)

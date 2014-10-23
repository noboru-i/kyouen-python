#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""APIレスポンスを返却するクラスを定義する.

一通りここに実装します.
"""

import logging
import webapp2
import json
from google.appengine.ext import db

from kyouenserver import KyouenPuzzle, KyouenPuzzleSummary
from const import Const


class RecentStages(webapp2.RequestHandler):

    u"""最近の投稿を返却する.

    10件固定
    """

    def get(self):
        u""" 最近の投稿を返却する. """
        # 最近の登録
        recent = KyouenPuzzle.gql('ORDER BY stageNo DESC').fetch(limit=10)
        result = []
        for entry in recent:
            result.append(dict(
                [(p, unicode(getattr(entry, p))) for p in entry.properties()]))
        self.response.out.write(json.dumps(result))

application = webapp2.WSGIApplication([
    ('/api/recent', RecentStages),
], debug=True)

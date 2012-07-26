#!-*- coding:utf-8 -*-

from google.appengine.ext import webapp

import dateutil.tz

register = webapp.template.create_template_register()

# UTC→JST変換
def jst (value):
    return value.replace(tzinfo=dateutil.tz.tzutc()).astimezone(dateutil.tz.gettz('Asia/Tokyo'))

register.filter(jst)

# ステージ一覧へのリンク作成
def list_link(stageNo):
    return '/page/list.html?index=' + str((stageNo - 1) - (stageNo - 1) % 10) + '&open=' + str(stageNo)

register.filter(list_link)
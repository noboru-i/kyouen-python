#!-*- coding:utf-8 -*-

import dateutil.tz

# UTC→JST変換
def jst (value, date_format='Y/m/d H:i'):
    return value.replace(tzinfo=dateutil.tz.tzutc()).astimezone(dateutil.tz.gettz('Asia/Tokyo')).strftime(date_format)

# ステージ一覧へのリンク作成
def list_link(stageNo):
    return '/page/list.html?index=' + str((stageNo - 1) - (stageNo - 1) % 10) + '&open=' + str(stageNo)


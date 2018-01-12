#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
import logging
import webapp2
import json

from models import KyouenPuzzle, KyouenPuzzleSummary, RegistModel

# 時計回りに90度回転させる。
def rot(stage, size):
    l = list(stage)
    temp = [0] * (size * size)
    for i in xrange(size):
        for j in xrange(size):
            temp[i * size + j] = l[(size - 1 - j) * size + i]
    return ''.join(temp)

# 左右反転する。
def mirror(stage, size):
    l = list(stage)
    temp = []
    for i in xrange(size):
        l2 = l[i * size:(i + 1) * size]
        l2.reverse()
        temp.extend(l2)
    return ''.join(temp)

# 登録処理
class KyouenRegist(webapp2.RequestHandler):

    # 次のステージ番号を返します。
    def getNextStageNo(self):
        model = KyouenPuzzle.gql("ORDER BY stageNo desc LIMIT 1").get()
        maxStageNo = None
        if model != None:
            maxStageNo = model.stageNo + 1
        else:
            maxStageNo = 1
        return maxStageNo

    # 検索します。
    # 既に登録されている場合、Trueを返します。
    def checkRegisteredStage(self, stage):
        model = KyouenPuzzle.gql("WHERE stage = :1", stage).get()
        if model == None:
            return False
        logging.debug(str(model.stageNo) + "/" + model.stage);
        return True

    # 登録済みかどうかをチェックします。
    def checkRegistered(self, stage, size):
        # 回転したパターンの作成
        ptn1 = [stage]
        for i in xrange(3):
            ptn1.append(rot(ptn1[-1], size))

        # 反転したパターンの作成
        ptn2 = []
        for b in ptn1:
            ptn2.append(mirror(b, size))

        for b in ptn1 + ptn2:
            if self.checkRegisteredStage(b):
                # すでにDB上に存在した場合
                return True
        # 存在しなかった場合
        return False

    # GETリクエストを処理します。
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('get not supported')
        return

    # POSTリクエストを処理します。
    def post(self):
        # パラメータ名：dataを取得
        data = self.request.get('data').split(',')
        logging.debug("post data:" + str(data))

        if len(data) != 3:
            # 要素が3つ取得できない場合はエラー
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('error' + str(data))
            return

        from kyouenmodule import hasKyouen, getPoints
        if len(getPoints(data[1], int(data[0]))) <= 4:
            # 石の数が4以下の場合
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write("not enough stone")
            logging.error('not enough stone.' + data[1])
            return
        if not hasKyouen(getPoints(data[1], int(data[0]))):
            # 共円でない場合
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write("not kyouen")
            logging.error('not kyouen.' + data[1])
            return

        if self.checkRegistered(data[1], int(data[0])):
            # 登録済みの場合
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write("registered")
            return

        # 入力データの登録
        model = KyouenPuzzle(stageNo=self.getNextStageNo(),
                             size=int(data[0]),
                             stage=data[1],
                             creator=data[2].replace('\n', ''))
        model.put()

        # DB登録
        regist_model = RegistModel(stageInfo=model.key)
        regist_model.put()

        # サマリの再計算
        summary = KyouenPuzzleSummary.query().get()
        if not summary:
            c = KyouenPuzzle.query().count()
            summary = KyouenPuzzleSummary(count=c)
        else:
            summary.count += 1
        summary.put()

        # レスポンスの返却
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('success stageNo=' + str(model.stageNo))
        return

# 取得処理
class KyouenGet(webapp2.RequestHandler):

    def get(self, dataType=None):
        logging.debug('dataType=' + str(dataType))
        stageNo = int(self.request.get('stageNo', '0'))
        count = int(self.request.get('count', '10'))

        data = KyouenPuzzle.query(KyouenPuzzle.stageNo > stageNo).fetch(count)

        if dataType is None:
            def generateSendData(model):
                return ','.join([str(model.stageNo), str(model.size), model.stage, model.creator])
            param = '\n'.join([generateSendData(m) for m in data])
            if len(param) == 0:
                # データが取得できなかった場合
                self.response.headers['Content-Type'] = 'text/plain'
                self.response.out.write("no_data")
                return
            self.response.headers['Content-Type'] = 'text/plain;charset=utf-8'
            self.response.out.write(param)
            return
        elif dataType == 'json':
            def generateSendData(model):
                param = {}
                param['stageNo'] = model.stageNo
                param['size'] = model.size
                param['stage'] = model.stage
                param['creator'] = model.creator
                return param
            param = []
            [param.append(generateSendData(p)) for p in data]
            self.response.headers['Content-Type'] = 'application/json;charset=utf-8'
            self.response.write(json.dumps(param))
            pass

application = webapp2.WSGIApplication([('/kyouen/regist', KyouenRegist),
                                      ('/kyouen/get\.(.*)', KyouenGet),
                                      ('/kyouen/get', KyouenGet),
                                      ], debug=True)

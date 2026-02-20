# アーキテクチャ構成図

## 1. 全体構成図

システム全体の構成を示します。

```mermaid
graph TB
    subgraph クライアント
        Browser["Webブラウザ<br/>Angular.js"]
        Android["Androidアプリ<br/>詰め共円 / 共円チェッカー"]
        iOS["iOSアプリ"]
    end

    subgraph GAE["Google App Engine (Python 2.7)"]
        subgraph 静的リソース
            Static["静的ファイル<br/>html / js / css / image"]
        end

        subgraph Webハンドラ
            HTML["html.py<br/>認証・ページ描画"]
            KyouenServer["kyouenserver.py<br/>ステージ登録・取得"]
            API["api.py<br/>REST API"]
            GCMServer["gcmserver.py<br/>Android プッシュ通知"]
            APNSServer["apnsserver.py<br/>iOS プッシュ通知"]
            Tasks["tasks.py<br/>Cron ジョブ"]
        end

        subgraph コアロジック
            KyouenModule["kyouenmodule.py<br/>共円判定"]
            Models["models.py<br/>データモデル"]
        end

        Datastore[("Cloud Datastore<br/>(NDB)")]
        Memcache[("Memcache<br/>セッション")]
    end

    subgraph 外部サービス
        Twitter["Twitter API<br/>(OAuth 1.0 / tweepy)"]
        FCM["Firebase Cloud Messaging<br/>(Android 通知)"]
        APNS["Apple Push Notification Service<br/>(iOS 通知)"]
    end

    Browser -->|HTTP GET| Static
    Browser -->|REST API| API
    Browser -->|OAuth ログイン| HTML
    Android -->|"/kyouen/regist<br/>/kyouen/get"| KyouenServer
    Android -->|"/page/api_login<br/>/page/add"| HTML
    iOS -->|"/kyouen/regist<br/>/kyouen/get"| KyouenServer

    API --> Models
    API --> Memcache
    HTML --> Models
    HTML --> Memcache
    HTML --> Twitter
    KyouenServer --> KyouenModule
    KyouenServer --> Models
    GCMServer --> FCM
    APNSServer --> APNS
    Tasks --> Twitter
    Models --> Datastore
```

---

## 2. データモデル図

Cloud Datastore (NDB) 上のエンティティとその関係を示します。

```mermaid
erDiagram
    KyouenPuzzle {
        int stageNo PK
        int size
        string stage "石の配置 (0/1 文字列)"
        string creator
        datetime registDate
    }

    KyouenPuzzleSummary {
        int count "ステージ合計数"
        datetime lastDate
    }

    RegistModel {
        key stageInfo FK
        datetime registDate
    }

    User {
        string userId PK "Twitter ユーザID"
        string screenName
        string image
        string accessToken
        string accessSecret
        int clearStageCount
    }

    StageUser {
        key stage FK
        key user FK
        datetime clearDate
    }

    RequestToken {
        string token_key
        string token_secret
        datetime creation_date
    }

    ApnsModel {
        string deviceToken
        datetime registDate
    }

    GcmModel {
        string registrationId
        datetime registDate
    }

    KyouenPuzzle ||--o{ StageUser : "クリア記録"
    User ||--o{ StageUser : "クリア記録"
    KyouenPuzzle ||--o{ RegistModel : "登録"
```

---

## 3. ステージ登録フロー

モバイルアプリからのステージ投稿処理 (`POST /kyouen/regist`) を示します。

```mermaid
flowchart TD
    Start(["開始"]) --> Receive["POST /kyouen/regist 受信<br/>data = size,stage,creator"]
    Receive --> ValidateParam{"パラメータ数 == 3?"}
    ValidateParam -->|"No"| Error1["エラー返却"]
    ValidateParam -->|"Yes"| CheckStones{"石の数 > 4?"}
    CheckStones -->|"No"| Error2["'not enough stone' 返却"]
    CheckStones -->|"Yes"| CheckKyouen{"共円判定<br/>hasKyouen()"}
    CheckKyouen -->|"No"| Error3["'not kyouen' 返却"]
    CheckKyouen -->|"Yes"| CheckDuplicate{"重複チェック<br/>回転4パターン<br/>+ 反転4パターン"}
    CheckDuplicate -->|"登録済み"| Error4["'registered' 返却"]
    CheckDuplicate -->|"未登録"| SavePuzzle["KyouenPuzzle 保存<br/>(stageNo, size, stage, creator)"]
    SavePuzzle --> SaveRegist["RegistModel 保存"]
    SaveRegist --> UpdateSummary["KyouenPuzzleSummary 更新<br/>(count をインクリメント)"]
    UpdateSummary --> Success["'success stageNo=N' 返却"]
```

---

## 4. 共円判定アルゴリズム

`kyouenmodule.py` の `isKyouen()` 関数が行う、4点が共円かどうかの判定ロジックを示します。

```mermaid
flowchart TD
    Start(["isKyouen(p1, p2, p3, p4)"]) --> L12["p1-p2 の垂直二等分線 l12 を計算"]
    L12 --> L23["p2-p3 の垂直二等分線 l23 を計算"]
    L23 --> I123{"l12 と l23 の交点 center を求める"}

    I123 -->|"交点なし<br/>(p1,p2,p3 が同一直線上)"| L34["p3-p4 の垂直二等分線 l34 を計算"]
    L34 --> I234{"l23 と l34 の交点を求める"}
    I234 -->|"交点なし<br/>(全点が同一直線上)"| ReturnLine["直線として返却<br/>(4点が一直線)"]
    I234 -->|"交点あり"| ReturnNone1["None を返却<br/>(共円でない)"]

    I123 -->|"交点あり"| Dist["d1 = dist(p1, center)<br/>d2 = dist(p4, center)"]
    Dist --> Compare{"|d1 - d2| < 0.0000001?"}
    Compare -->|"Yes (等距離)"| ReturnCircle["円として返却<br/>(stones, center, radius)"]
    Compare -->|"No"| ReturnNone2["None を返却<br/>(共円でない)"]
```

**`hasKyouen()`** は石の座標リストから4点の組み合わせをすべて列挙し、いずれかが `isKyouen()` を満たす場合に `True` を返します。

> **epsilon について**: 距離差の許容誤差 `0.0000001` は、浮動小数点演算の丸め誤差を吸収するための値です。格子点座標を扱うため、厳密な等号ではなくこのしきい値で同距離を判定します。

---

## 5. Twitter OAuth 認証フロー

Webブラウザからの Twitter OAuth 1.0 ログイン処理を示します。

```mermaid
sequenceDiagram
    participant User as ユーザ
    participant Browser as Webブラウザ
    participant GAE as Google App Engine
    participant Twitter as Twitter API
    participant MC as Memcache
    participant DS as Cloud Datastore

    User->>Browser: ログインリンクをクリック
    Browser->>GAE: GET /page/login
    GAE->>Twitter: get_authorization_url()
    Twitter-->>GAE: authorization_url + request_token
    GAE->>DS: RequestToken を保存
    GAE-->>Browser: Twitter 認証ページへリダイレクト
    Browser->>Twitter: ユーザが認証を承認
    Twitter-->>Browser: コールバック (oauth_token, oauth_verifier)
    Browser->>GAE: GET /page/login_callback
    GAE->>DS: RequestToken を取得・削除
    GAE->>Twitter: get_access_token(verifier)
    Twitter-->>GAE: access_token
    GAE->>MC: sid をキーに access_token を保存
    GAE->>Twitter: api.me() でプロフィール取得
    Twitter-->>GAE: ユーザ情報
    GAE->>DS: User を保存 / 更新
    GAE-->>Browser: トップページへリダイレクト
```

---

## 6. フロントエンド構成図

CoffeeScript / Jade / Stylus から Gulp でビルドして静的ファイルを生成する構成を示します。

```mermaid
graph LR
    subgraph src["src/ (ソース)"]
        direction TB
        CS["coffee/*.coffee<br/>Angular.js アプリ"]
        Jade["jade/*.jade<br/>HTML テンプレート"]
        Stylus["stylus/*.styl<br/>スタイルシート"]
    end

    subgraph Build["Gulp ビルド (gulpfile.coffee)"]
        direction TB
        GC["gulp-coffee"]
        GJ["gulp-jade"]
        GS["gulp-stylus"]
    end

    subgraph Dist["dist/ (出力・静的配信)"]
        direction TB
        JS["js/*.js"]
        HTML["html/*.html"]
        CSS["css/*.css"]
    end

    subgraph Angular["Angular.js モジュール構成 (coffee/)"]
        direction TB
        AppModule["app.coffee<br/>メインモジュール"]
        Controllers["controllers.coffee<br/>ビューロジック"]
        Services["services.coffee<br/>API 通信"]
        Directives["directives.coffee<br/>カスタム UI"]
        Filters["filters.coffee<br/>表示フォーマット"]
        List["list.coffee<br/>一覧画面"]
        Overlay["overlay.coffee<br/>オーバーレイ UI"]
    end

    CS --> GC --> JS
    Jade --> GJ --> HTML
    Stylus --> GS --> CSS

    AppModule --> Controllers
    AppModule --> Services
    AppModule --> Directives
    AppModule --> Filters
```

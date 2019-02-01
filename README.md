# 共円 in Google App Engine(python)

## Production environment

https://my-android-server.appspot.com/

## App for Android

### 詰め共円

https://market.android.com/details?id=hm.orz.chaos114.android.tumekyouen

### 共円チェッカー

https://market.android.com/details?id=hm.orz.chaos114.android.kyouenchecker

## Setup and run

Install Google Cloud SDK
https://cloud.google.com/appengine/docs/standard/python/download

```
cd src
pip install -t lib -r requirements.txt
yarn
npm run build
dev_appserver.py .
```

## Deploy

```
cd src
gcloud app deploy app.yaml
```

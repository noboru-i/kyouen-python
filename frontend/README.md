## How to deploy

Create build frontend.

```
npm run build
```

Copy dist directory to src.

```
rm -rf ../src/dist
cp -r dist ../src
```

Deploy to Google App Engine. https://cloud.google.com/sdk/gcloud/reference/app/deploy

```
cd ../src
gcloud app deploy app.yaml --no-promote --quiet
```

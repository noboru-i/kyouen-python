gulp = require 'gulp'
gutil = require 'gulp-util'
coffee = require 'gulp-coffee'
sourcemaps = require 'gulp-sourcemaps'
jade = require 'gulp-jade'
stylus = require 'gulp-stylus'
del = require 'del'
concat = require 'gulp-concat'
order = require 'gulp-order'

# clean
gulp.task 'clean', ->
  del ['css', 'html', 'js']

# stylus
gulp.task 'stylus', ->
  gulp.src './stylus/*.styl'
    .pipe stylus()
    .pipe concat('app.css')
    .pipe gulp.dest('./css/')
  return

# jade
gulp.task 'jade', ->
  gulp.src "./jade/**/*.jade"
    .pipe jade()
    .pipe gulp.dest("./html/")
  return

# coffee
gulp.task 'coffee', ->
  gulp.src ['coffee/app.coffee', './coffee/*.coffee']
    .pipe sourcemaps.init()
    .pipe coffee().on('error', gutil.log)
    .pipe order([
      "coffee/app.js",
      "coffee/*.js"
    ])
    .pipe concat('app.js')
    .pipe sourcemaps.write('./maps')
    .pipe gulp.dest('./js/')
  return

# watch
gulp.task 'watch', ->
  gulp.watch './stylus/*.styl', ['stylus']
  gulp.watch './jade/**/*.jade', ['jade']
  gulp.watch './coffee/*.coffee', ['coffee']

gulp.task 'default', ['stylus', 'jade', 'coffee']

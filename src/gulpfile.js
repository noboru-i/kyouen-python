var gulp = require('gulp');
var gutil = require('gulp-util');
var coffee = require('gulp-coffee');
var sourcemaps = require('gulp-sourcemaps');

gulp.task('coffee', function() {
  gulp.src('./coffee/*.coffee')
      .pipe(sourcemaps.init())
      .pipe(coffee({bare: false}).on('error', gutil.log))
      .pipe(sourcemaps.write('./maps'))
      .pipe(gulp.dest('./js/'))
});

gulp.task('default', ['coffee']);
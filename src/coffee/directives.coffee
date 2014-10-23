'use strict'

@KyouenApp
.directive 'recentStages', ()->
  restrict: 'E'
  replace: true
  require: '^ngModel'
  templateUrl: 'html/parts/recent_stages.html'

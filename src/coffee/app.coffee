'use strict'

@KyouenApp = angular.module('kyouenApp', [
  'ui.bootstrap'
])
.config(["$locationProvider", ($locationProvider) ->
  $locationProvider.html5Mode(true)
])

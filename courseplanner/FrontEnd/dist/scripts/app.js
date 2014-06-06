'use strict';

angular
  .module('coursePlannerApp', [
    'ngCookies',
    'ngResource',
    'ngSanitize',
    'ngRoute',
    'googlechart',
    'ui.bootstrap',
    'ngDragDrop',
    'angularFileUpload'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/dashboard.html',
        controller: 'DashboardCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  });

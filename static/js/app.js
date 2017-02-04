var CMMessagerApp = angular.module('CMMessagerApp', ['ngUpload']);


/**
Controllers
*/

//Send message controller
CMMessagerApp.controller('loginController', ['$scope','$window','CMMessagerAPIDelegate', function($scope, $window, CMMessagerAPIDelegate) {

  this.server = "smtp.gmail.com:587";

  //Uploads a file throught the use of a web service REST.
  this.login = function login() {

    console.log("Login in user: " + this.userName);

    //tries to log a user onto his mailing service.

    CMMessagerAPIDelegate.loginMail(this.userName, this.passWord, this.server);

  };

}]);

//Send message controller
CMMessagerApp.controller('SendController', ['$scope','$window','CMMessagerAPIDelegate', function($scope, $window, CMMessagerAPIDelegate) {
  self = this;

  this.listInboxOpen=false;
  this.message = {};
  $scope.messageForm = {selectedItems:null, subject:"", message:"", fileName:""}; //This initiates the object for the entire form to collect the data for the controller.

  // Private function - This interchanges the upload and import button, conviniently.
  function changeUploadButtons() {

    if ($('#import').prop('disabled')){

      $('#import').prop('disabled', false);
      $('#import').attr('class', 'btn btn-primary'); //toggleClass('btn-primary');

      $('#btnUpload').attr('class', 'btn btn-secondary'); //.toggleClass('btn-secondary');
      $('#btnUpload').prop('disabled', true);

    }else{

      $('#import').prop('disabled', true);
      $('#import').attr('class', 'btn btn-secondary'); //toggleClass('btn-primary');

      $('#btnUpload').attr('class', 'btn btn-primary'); //.toggleClass('btn-secondary');
      $('#btnUpload').prop('disabled', false);

    }

  };

  //Imports a previously uploaded file with contacts' information in it.
   this.importContacts = function importContacts() {

      console.log($scope.messageForm);
      //TODO: need to change it for a promise.
      $('#statusMessages').text("Importing the file...");

      //Freezing the buttons.
      changeUploadButtons();

      //adding the file to form data TODO refactor this, to make it compatible with older browsers.
      result = CMMessagerAPIDelegate.importDataFile($scope.messageForm);

  };

  //Uploads a file throught the use of a web service REST.
  $scope.uploadFile = function uploadFile(content) {
    //TODO: this has to be refactored to make it specific to the given form.

    if(content["code"]==200){

      console.log("Uploaded file: " + content["resultado"]);

      $scope.messageForm.fileName=content["resultado"];

      //Reseting the front-end.
      $('#fileAttachment').text(content["resultado"]);
      changeUploadButtons();
      $('#statusMessages').text("File successfully uploaded; import it.");

    }else{

      console.log("Error meanwhile the file uploading: " + content["resultado"] + ", Code: " + content["code"]);
      $('#statusMessages').text(content["resultado"]);
      $('#import').prop('disabled', true);

    }

  };

  //Shows the list of possible message inboxes.
  this.addressToReceive = function addressToReceive() {
    this.listInboxOpen=!this.listInboxOpen;
  };

  //Sends the message, as a fact. Handles the recepies and attachments (forms the JSON object to interchange)
   this.sendMessage = function sendMessage() {

      console.log($scope.messageForm);

      //adding the file to form data TODO refactor this, to make it compatible with older browsers.
      CMMessagerAPIDelegate.sendMessage($scope.messageForm);

    };

}]);

// This inbox controller allows the management of the receivers on screen and by AJAX, this is core functionality.
CMMessagerApp.controller("InboxCtrl", ["$scope", "CMMessagerAPIDelegate", function($scope, CMMessagerAPIDelegate) {

  self = this;

  // Here goes the call to the service that will, eventually, connect with the LinkedIn API.
  this.loadInboxOptions = function() {

    //uses a promise to deliver the proper values to the frontend
    result = CMMessagerAPIDelegate.getContacts()
      .then(function(data) {
          $scope.inboxes = data;
          console.log($scope.inboxes);
      }, function(err) {
          $scope.inboxes = [];
          console.log($scope.inboxes);
      });

      return result;
  };

  //this makes the functionality for the checks and the unchecks of different inboxes.
  this.checkByTag = function(inboxTag) {

    inboxList = $scope.inboxes;

    //This is to set the checked
    if ($('.'+inboxTag).prop('checked')==false){
      $('.'+inboxTag).prop('checked', true);

      $('.'+inboxTag).each(
        function(i, obj){
          $scope.messageForm.selectedItems[obj.value] = obj.value;
        }
      );

    } else {
      $('.'+inboxTag).prop('checked', false);

      $('.'+inboxTag).each(
        function(i, obj){
          delete $scope.messageForm.selectedItems[obj.value];
        }
      );
    }

    //console.log("Click! on " + JSON.stringify($scope.messageForm.selectedItems));

  };

  //This uploads the checked data on the records
  this.checkByClick = function(userName) {

    if($scope.messageForm.selectedItems[userName]==undefined){
      $scope.messageForm.selectedItems[userName] = userName;
    } else {
      delete $scope.messageForm.selectedItems[userName];
    }

    console.log("Click! on " + JSON.stringify($scope.messageForm.selectedItems));
  };

}]);

/**
Configuration
**/

CMMessagerApp.config(function($sceDelegateProvider) {
  $sceDelegateProvider.resourceUrlWhitelist([
    // Allow same origin resource loads.
    'self',
    // Allow loading from outer templates domain.
    'http://localhost/**',
    'http://linkeddyn-messenger.azurewebsites.net/**'
  ]);
});

/**
Directives
*/


CMMessagerApp.directive("inboxSelection",  function(){

    //templateURL = "http://linkeddyn-messenger.azurewebsites.net/inboxSelection.html";
    templateURL = "../static/inboxSelection.html";
    //$sce.trustAsResourceUrl(templateURL);

    return {
      restrict: "E",
      templateUrl: templateURL,
      scope: false,
      require:'ngModel',
      link: function(scope, element, attrs, ctrl){
        scope.messageForm.selectedItems = {};
      },
    };
});


/***
SERVICES
***/

CMMessagerApp.factory('formDataObject', function() {
    return function(data) {
        var fd = new FormData();
        angular.forEach(data, function(value, key) {
            fd.append(key, value);
        });
        return fd;
    };
});

//REST API handler - this manages the calls to the web services.
CMMessagerApp.factory("CMMessagerAPIDelegate", ["$q","$http", "$httpParamSerializer", "Base64", function($q, $http, $httpParamSerializer, Base64){

  var CMMessagerAPIDelegate = {};

  //This returns a collection of functions
  CMMessagerAPIDelegate.getContacts = function(){

    result = $http({
        method: 'GET',
        url: 'http://localhost:5000/api/v1.0/contactos/all',
        withCredentials: false,
        contentType: false,
        data: $httpParamSerializer()
    })
    .then(
      function successCallback(response) {
          // contacts JSON structure retrieved.
          console.log(response.data);
          contacts = response.data;
          return contacts;
      },
      function errorCallback(response) {
          // Uploading incomplete
          //setting the status messages in order TODO: move this to the controller
          msg = "<strong> ERROR: Contacts can't be retrieved! </strong> <br>HTTP code: " +
                response.status +
                "<br/> message: " +
                response.statusText +
                "<br/> data: " +
                response.data +
                "<br/> headers: " +
                response.headers +
                "<br/> config: " +
                response.config;

        $("#statusMessages").html(msg);

        return $q.reject(response.data);
    });

    return result;
  };

  //Sends the mailing message to the web service to manage it, and finally, send each one...by one.
  CMMessagerAPIDelegate.importDataFile = function importDataFile(fileData){

    console.log("...calling the web service...");

    $http({
        method: 'POST',
        //url: 'http://localhost:5000/api/v1.0/contactos/load/linkedin' ,
        url: '/api/v1.0/contactos/load/linkedin' ,
        //withCredentials: false,
        //contentType: false,
        //transformRequest: angular.identity,
        headers: {
          //'Authorization': 'Basic ' + Base64.encode('admin:repasstea'),
          //'Accept':'multipart/form-data',
          //'Content-Type': undefined,
          'Content-Type': 'application/json',
          //'Content-Type': 'application/x-www-form-urlencoded',
          //'Content-Type': 'multipart/form-data',
        },
        data: fileData

    })
    .then(
    function successCallback(response) {
        // Uploading complete
        //setting the status messages in order TODO: move this to the controller
        msg = "<strong> Import successfully done! </strong> <br>";
        $('#statusMessages').html(msg);
        console.log(msg);

    },
    function errorCallback(response) {
        // Uploading incomplete
        //setting the status messages in order TODO: move this to the controller
        msg = "<strong> ERROR: File NOT imported! </strong> <br>HTTP code: " +
              response.status +
              "<br/> message: " +
              response.statusText +
              "<br/> data: " +
              response.data +
              "<br/> headers: " +
              response.headers +
              "<br/> config: " +
              response.config;

        console.log(msg);
        $('#statusMessages').html(msg);
    });

  };

  //Sends the mailing message to the web service to manage it, and finally, send each one...by one.
  CMMessagerAPIDelegate.sendMessage = function sendMessage(messageData){

    console.log("...calling the web service...");

    $http({
        method: 'POST',
        url: 'http://localhost:5000/api/v1.0/mailing/send',
        //withCredentials: false,
        //contentType: false,
        //transformRequest: angular.identity,
        headers: {
          //'Authorization': 'Basic ' + Base64.encode('admin:repasstea'),
          //'Accept':'multipart/form-data',
          //'Content-Type': undefined,
          'Content-Type': 'application/json',
          //'Content-Type': 'application/x-www-form-urlencoded',
          //'Content-Type': 'multipart/form-data',
        },
        data: messageData

    })
    .then(
    function successCallback(response) {
        // Uploading complete
        //setting the status messages in order TODO: move this to the controller
        msg = "<strong> Mail and attachments successfully sent! </strong> <br>";

        console.log(msg);

    },
    function errorCallback(response) {
        // Uploading incomplete
        //setting the status messages in order TODO: move this to the controller
        msg = "<strong> ERROR: Message NOT sent! </strong> <br>HTTP code: " +
              response.status +
              "<br/> message: " +
              response.statusText +
              "<br/> data: " +
              response.data +
              "<br/> headers: " +
              response.headers +
              "<br/> config: " +
              response.config;

        console.log(msg);
    });


  };

  //Tries to login into the user mailing service.
  CMMessagerAPIDelegate.loginMail = function loginMail(user, pass, server){

    console.log("...calling the web service...");

    $http({
        method: 'POST',
        url: 'http://localhost:5000/api/v1.0/mailing/login_try',
        //withCredentials: false,
        //contentType: false,
        //transformRequest: angular.identity,
        //headers: {
          //'Authorization': 'Basic ' + Base64.encode('admin:repasstea'),
          //'Accept':'multipart/form-data',
          //'Content-Type': undefined,
          'Content-Type': 'application/json',
          //'Content-Type': 'application/x-www-form-urlencoded',
          //'Content-Type': 'multipart/form-data',
        //},
        data: JSON.stringify({"user":user,"pass": pass,"server": server})

    })
    .then(
    function successCallback(response) {
       //Logins into the user's mailing system.

        console.log("Logged in with success!" + response.data);

    },
    function errorCallback(response) {
        //setting the status messages in order TODO: move this to the controller
        msg = "<strong> ERROR: Login failed! </strong> <br>HTTP code: " +
              response.status +
              "<br/> message: " +
              response.statusText +
              "<br/> data: " +
              response.data +
              "<br/> headers: " +
              response.headers +
              "<br/> config: " +
              response.config;

        console.log(msg);
    });


  };

  return CMMessagerAPIDelegate;
}]);

/**
The service for conversion of the credentials
*/
CMMessagerApp.factory('Base64', function () {

  /* jshint ignore:start */
    var keyStr = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';

    return {
        encode: function (input) {
            var output = "";
            var chr1, chr2, chr3 = "";
            var enc1, enc2, enc3, enc4 = "";
            var i = 0;

            do {
                chr1 = input.charCodeAt(i++);
                chr2 = input.charCodeAt(i++);
                chr3 = input.charCodeAt(i++);

                enc1 = chr1 >> 2;
                enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
                enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
                enc4 = chr3 & 63;

                if (isNaN(chr2)) {
                    enc3 = enc4 = 64;
                } else if (isNaN(chr3)) {
                    enc4 = 64;
                }

                output = output +
                    keyStr.charAt(enc1) +
                    keyStr.charAt(enc2) +
                    keyStr.charAt(enc3) +
                    keyStr.charAt(enc4);
                chr1 = chr2 = chr3 = "";
                enc1 = enc2 = enc3 = enc4 = "";
            } while (i < input.length);

            return output;
        },

        decode: function (input) {
            var output = "";
            var chr1, chr2, chr3 = "";
            var enc1, enc2, enc3, enc4 = "";
            var i = 0;

            // remove all characters that are not A-Z, a-z, 0-9, +, /, or =
            var base64test = /[^A-Za-z0-9\+\/\=]/g;
            if (base64test.exec(input)) {
                window.alert("There were invalid base64 characters in the input text.\n" +
                    "Valid base64 characters are A-Z, a-z, 0-9, '+', '/',and '='\n" +
                    "Expect errors in decoding.");
            }
            input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");

            do {
                enc1 = keyStr.indexOf(input.charAt(i++));
                enc2 = keyStr.indexOf(input.charAt(i++));
                enc3 = keyStr.indexOf(input.charAt(i++));
                enc4 = keyStr.indexOf(input.charAt(i++));

                chr1 = (enc1 << 2) | (enc2 >> 4);
                chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
                chr3 = ((enc3 & 3) << 6) | enc4;

                output = output + String.fromCharCode(chr1);

                if (enc3 != 64) {
                    output = output + String.fromCharCode(chr2);
                }
                if (enc4 != 64) {
                    output = output + String.fromCharCode(chr3);
                }

                chr1 = chr2 = chr3 = "";
                enc1 = enc2 = enc3 = enc4 = "";

            } while (i < input.length);

            return output;
        }
    };
    /* jshint ignore:end */
});

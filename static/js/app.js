var CMMessagerApp = angular.module('CMMessagerApp', []);


/**
Controllers
*/
CMMessagerApp.controller('SendController', ['$scope','CMMessagerAPIDelegate', function($scope, CMMessagerAPIDelegate) {
  self = this;

  this.listInboxOpen=false;
  this.message = {};
  $scope.messageForm = {}; //This initiates the object for the entire form to collect the data for the controller. TODO: we need to change this for a proper form.

  //Shows the list of possible message inboxes.
  this.addressToReceive = function addressToReceive() {
    this.listInboxOpen=!this.listInboxOpen;
  };

  //Sends the message, as a fact. Handles the recepies and attachments (forms the JSON object to interchange)
 this.sendMessage = function sendMessage() {

    console.log($scope.messageForm.selectedItems);

    this.message.inboxes = "INBOXES DE ANGULAR!";//$("#").val()); //TODO here we need to extract the inboxes from somewhere, and it cannot be the view.
    this.message.subject = $("#txtSubject").val();
    this.message.textBody = $("#txtDetails").val();
    this.message.attachedFile = $("#fileAttachment").val();

    //adding the file to form data TODO refactor this, to make it compatible with older browsers.
    CMMessagerAPIDelegate.sendMessage(this.message);

  };

}]);

// This inbox controller allows the management of the receivers on screen and by AJAX, this is core functionality.
CMMessagerApp.controller("InboxCtrl", ["$scope", "CMMessagerAPIDelegate", function($scope, CMMessagerAPIDelegate) {

  self = this;

  this.inboxes = [];
  //this.selectedInboxes = {};

  // Here goes the call to the service that will, eventually, connect with the LinkedIn API.
  this.loadInboxOptions = function() {
    this.inboxes = CMMessagerAPIDelegate.getContacts();
  };

  //this makes the functionality for the checks and the unchecks of different inboxes.
  this.checkByTag = function(inboxTag) {

    inboxList = this.inboxes;

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

CMMessagerApp.factory("CMMessagerAPIDelegate", ["$http", "$httpParamSerializer", "Base64", function($http, $httpParamSerializer, Base64){

  var CMMessagerAPIDelegate = {};

  //This returns a collection of functions
  CMMessagerAPIDelegate.getContacts = function(){
    //TODO Here goes the linkedin Magic
    return  [
        {
          userName: "AlmiranteBrown",
          name: "Almirante Brown",
          tagName: ""
        },
        {
          userName: "DoctorWho",
          name: "Doctor Who",
          tagName: "directors"
        },
        {
          userName: "LorenaPaola",
          name: "Lorena Paola",
          tagName: "rrhh"
        },
        {
          userName: "KatyAleman",
          name: "Katy Aleman",
          tagName: "rrhh"
        },
        {
          userName: "BobyFlores",
          name: "Boby Flores",
          tagName: "rrhh"
        },
        {
          userName: "DonovanLars",
          name: "Donovan Lars",
          tagName: "rrhh"
        }
    ];
  };

  //Sends the messages to linkedin's users
  CMMessagerAPIDelegate.sendMessage = function (message){
    var msg = "";

    console.log(JSON.stringify(message));

    //message.attachedFile = null;//TODO: this is wrong and must be fixed. The app must support files.

    $http({
        method: 'POST',
        url: 'http://localhost/linkeddyn_msgs/mock_api/',
        withCredentials: true,
        contentType: false,
        transformRequest: angular.identity,
        headers: {
          'Authorization': 'Basic ' + Base64.encode('admin:repasstea'),
          //'Accept':'multipart/form-data',
          //'Content-Type': undefined,
          //'Content-Type': 'application/json',
          //'Content-Type': 'application/x-www-form-urlencoded',
          'Content-Type': 'multipart/form-data',
        },
        data: $httpParamSerializer(message)

    })
    .then(
    function successCallback(response) {
        // Uploading complete
        //setting the status messages in order TODO: move this to the controller
        msg = "<strong> Message successfully sent! </strong> <br>";
        msg += "Subject: " + message.subject + " <br/> Details: <br/>" +
                  message.textBody + " <br/> Attachment: " +
                  message.attachedFile;

        $("#statusMessages").html(msg);

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

        $("#statusMessages").html(msg);
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

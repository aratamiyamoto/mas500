var splashRouter;

(function($){

var SplashRouter = Backbone.Router.extend({

    routes: {
      "": "home",
      "country/:country": "country",
    },
    
    initialize: function(){
        _.bindAll(this)
    },
     
    home: function() {
        console.log('home()');
        $('#gv-country').val();
    },

    country: function(country) {
        console.log('country()');
        $('#gv-country').val(country);
        splashView.lookupCountry2();
    }
});

splashRouter = new SplashRouter;

})(jQuery);


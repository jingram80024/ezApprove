(function($) {
    "use strict";
    var $WIN = $(window);

    $WIN.on('load', function() {
        var url = $(location).attr('href');
        if (url.search('/sold') != -1){
            set_nav_highlight('nav-sold');
        } else if (url.search('/approved') != -1) {
            set_nav_highlight('nav-approved');
        } else if (url.search('/denied') != -1) {
            set_nav_highlight('nav-denied');
        } else if (url.search('/kicked-back') != -1) {
            set_nav_highlight('nav-kicked-back');
        } else if ((url == 'http://127.0.0.1:8000/store') || (url == 'http://127.0.0.1:8000/store/') || (url == 'https://127.0.0.1:8000/store') || (url == 'https://127.0.0.1:8000/store/')) {
            set_nav_highlight('nav-pending');
        } else {
            console.log('error - url not as expected');
        }
    });
    
    function set_nav_highlight(nav_id) { /* alter to activate passed <a>*/
        console.log("-------");
        $('.topnav').children('a').each(function(){
            if ($(this).hasClass('active')){
                console.log(this.id, " is active");
            } else {
                console.log(this.id, " is inactive");
            }
        });
        console.log("-------");
    }
})(jQuery);
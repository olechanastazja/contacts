
        $(document).ready(function(){
            console.log('Czy to dziala?')
            $("#txtSearch").autocomplete({
                source: "/ajax_calls/search/",
                minLength: 2,
                open: function(){
                    setTimeout(function () {
                        $('.ui-autocomplete').css('z-index', 99);
                    }, 0);
                }
              });

        });
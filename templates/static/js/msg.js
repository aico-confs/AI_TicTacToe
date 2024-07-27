function reset () {
    $("#toggleCSS").attr("href", "/static/css/alertify/alertify.default.css");
    alertify.set({
        labels : {
            ok     : "OK",
            cancel : "Cancel"
        },
        delay : 5000,
        buttonReverse : false,
        buttonFocus   : "ok"
    });
}



allTds = $("table td");


function cross(obj){
    $(obj).addClass("beRed");
    $(obj).text("❌");
    $(obj).off("click");
    // $('#currData').attr('d', $('#currData').attr('d') + $(obj).attr('value'));

}

function mark(obj){
    $(obj).addClass("beBlue");
    $(obj).text("✔️");
    $(obj).off("click");
    // $('#currData').attr('d', $('#currData').attr('d') + $(obj).attr('value'))
}

function setSymbol(){

    allTds.each(function() {

    if($('#titleSelect').val() == '自由模式'){
        $(this).click(function(e) {
            $(this).removeClass("beRed");
            if ($(this).hasClass( "beBlue" )){
                $(this).text("");
            }else{
                $(this).text("✔️");
            }
            $(this).toggleClass("beBlue");
            
        });
        // 右鍵事件
        $(this).on("contextmenu", function(e) {
            // 阻止預設的右键菜單彈出
            e.preventDefault();
            $(this).removeClass("beBlue");
            if ($(this).hasClass( "beRed" )){
                $(this).text("");
            }else{
                $(this).text("❌");
            }
            $(this).toggleClass("beRed");
    
        });
        return ;
    // 自由模式結束
    }else{
    $(this).click(function(e) {
        value = $('#titleSelect').val();
        if (value == '先手' && !($(this).hasClass( "beRed" ))){

            mark(this);
            answer($(this).attr('value'));

        }else if(value == '後手' && !($(this).hasClass( "beBlue" ))){

            cross(this);
            answer($(this).attr('value'));

        }
    
    })        
    }



    });



}





function resetGame(){
    mode = $('#titleSelect').val();
    setMode(mode);
}

function setMode(mode) {
    //



    document.getElementById('pageTitle').textContent = mode;
    // document.getElementById('titleSelect').value = mode;
    
    // document.title = value;
    allTds.each(function() {
        $(this).text("");
        $(this).removeClass("beRed");
        $(this).removeClass("beBlue");
        // $('#currData').attr('d', '');
        $(this).off("click");
        $(this).off("contextmenu");
    });

    $.ajax({
        url: "reset_board", /*資料提交到calc處*/
        type: "POST",  /*採用POST方法提交*/
        async:false,
        data: { "mode":mode},  /*提交的資料（json格式），從輸入框中獲取*/
        /*result為后端函式回傳的json*/
        success: function (result) {
            
            if (result.message == "200") {
                // console.log('reset_board');
                if(mode == '後手'){
                    answer();
                }
            }
        }
    });
    setSymbol();
}


function answer(value){

    mode = $('#titleSelect').val();
    $.ajax({
        url: "calc", /*資料提交到calc處*/
        type: "POST",  /*採用POST方法提交*/
        async:false,
        data: { "value": value},  /*提交的資料（json格式），從輸入框中獲取*/
        /*result為后端函式回傳的json*/
        success: function (result) {
            
            if (result.message == "200") {
                ;
            }
            else {

                // alertify.alert(result.message);  
                alertify.success(result.message);

                allTds.each(function() {
                    $(this).off("click");
                });
            }

            if (mode == '先手'){
                cross('#id'+result.answer);
            }else{
                mark('#id'+result.answer);
            }

        }
    });
        
}


allTds = $("table td");


function cross(obj){
    $(obj).addClass("beRed");
    $(obj).text("❌");
    $('#currData').attr('d', $('#currData').attr('d') + $(obj).attr('value'));

}

function mark(obj){
    $(obj).addClass("beBlue");
    $(obj).text("✔️");
    $('#currData').attr('d', $('#currData').attr('d') + $(obj).attr('value'))
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
    }else{
    $(this).click(function(e) {
        currData = $('#currData').attr('d');
        value = $('#titleSelect').val();
        if (value == '先手' && !($(this).hasClass( "beRed" ))&&(currData.length %2 ==0)){

            mark(this);
            answer();

        }else if(value == '後手' && !($(this).hasClass( "beBlue" ))&&(currData.length %2 !=0)){

            

            cross(this);
            answer();

        }
    
    })        
    }



    });



}







function setMode(value) {
    document.getElementById('pageTitle').textContent = value;
    document.getElementById('titleSelect').value = value;
    
    document.title = value;
    allTds.each(function() {
        $(this).text("");
        $(this).removeClass("beRed");
        $(this).removeClass("beBlue");
        $('#currData').attr('d', '');
        $(this).off("click");
        $(this).off("contextmenu");
    });

    setSymbol();
    if(value == '後手'){
        answer();
    }
}


function answer(){

    mode = $('#titleSelect').val();

    let currData = $('#currData').attr('d');


    console.log(currData);
    $.ajax({
        url: "calc", /*資料提交到calc處*/
        type: "POST",  /*採用POST方法提交*/
        async:false,
        data: { "currData": currData, "mode":mode},  /*提交的資料（json格式），從輸入框中獲取*/
        /*result為后端函式回傳的json*/
        success: function (result) {
            
            if (result.message == "200") {
                if (currData.length %2){
                    cross('#id'+result.answer);
                }else{
                    mark('#id'+result.answer);
                }
            }
            else {
                alert(result.message)
            }

        }
    });
        
}


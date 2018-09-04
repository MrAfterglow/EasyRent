function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function () {
    $('#form-auth').submit(function (e) {
        e.preventDefault()
        var real_name=$('#real-name').val()
        var id_card =$('#id-card').val()

        $.ajax({
            url:'/user/auth/',
            type:'PATCH',
            dataType:'json',
            data:{
                  'real_name':real_name,
                'id_card':id_card
            },
            success:function (data) {
                if (data.code==200){
                    $('.btn-success').hide()
                }else{
                    alert(data.code)
                }
            }
        })
    })

    $.get('/user/auth_info/',function (data) {
        if (data.code==200){
            $('#real-name').val(data.user_info.id_name)
            $('#id-card').val(data.user_info.id_card)
            if (data.user_info.id_card) {
                $('.btn-success').hide()
            }
        }
    })
})
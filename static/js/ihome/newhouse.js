function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $.get('/house/area_facility/',function (data) {
        if (data.code==200){
            for (var i=0 ;i<data.area_info.length;++i){
                var option_str = '<option value="' + data.area_info[i].id + '">' + data.area_info[i].name +'</option>'
                $('#area-id').append(option_str)
            }

            for (var i=0 ; i<data.facility_info.length; ++i){
                var facility_str= '<li>'+ '<div class="checkbox">'+ '<label>' + '<input type="checkbox" name="facility" value="'
                                    +data.facility_info[i].id + '">' + data.facility_info[i].name + '</label></div></li>'
                $('.house-facility-list').append(facility_str)
            }
        }
    })

    $('#form-house-info').submit(function (e) {
        e.preventDefault()
        $(this).ajaxSubmit({
            url:'/house/new_house/',
            type:"POST",
            dataType:'json',
            success:function (data) {
                if (data.code==200) {
                    $('#form-house-image').show()
                    $('#form-house-info').hide()
                }
            }
        })

    })

    $('#form-house-image').submit(function (e) {
        console.log('aaa')
        e.preventDefault()
        $(this).ajaxSubmit({
            url: '/house/add_img/',
            type: 'PATCH',
            dataType: 'json',
            success:function (data) {
                console.log(data)
                if (data.code==200){
                    $('#img').attr('src','/static/media/'+data.img_path)
                    $('#post_img').hide()
                }
            }
        })
    })
})
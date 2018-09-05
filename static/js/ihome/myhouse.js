$(document).ready(function(){
    $(".auth-warn").show();
})

$(document).ready(function () {
    $.get('/house/house_info/',function (data) {
        if (data.code==200){
            $('.auth-warn').hide()
            $('#houses-list').show()
            for (var i=0 ; i<data.house_info.length ; ++i) {
                var house = '<li>'
                house += '<a href="/house/detail/?house_id='+data.house_info[i].id + '">'
                house += '<div class="house-title">'
                house += ' <h3>房屋ID:'+ data.house_info[i].id +'   房屋标题:   '+ data.house_info[i].title +'</h3>'
                house += '</div><div class="house-content">'
                house += '<img alt="" src="/static/media/'+data.house_info[i].image+'"><div class="house-text"><ul>'
                console.log('/static/media/'+data.house_info[i].image)
                house += '<li>位于：'+ data.house_info[i].area +'</li><li>价格：￥'+ data.house_info[i].price+'/晚</li>'
                house += '<li>发布时间：'+data.house_info[i].create_time + '</li></ul></div></div></a></li>'
                $('#houses-list').append(house)
            }

        } else {
            $('.auth-warn').show()
            $('#houses-list').hide()
        }
    })
})
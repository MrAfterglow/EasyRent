function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
    $(".book-house").show();

    var search_url = location.search
    var house_id = search_url.split('=')[1]
    $.get('/house/detail/'+house_id,function (data) {
        console.log(data)
        for (var i=0; i<data.detail.images.length; ++i){
            var imgs = '<li class="swiper-slide"><img  src="/static/media/'+ data.detail.images[i] + '"></li>'
            $('.swiper-wrapper').append(imgs)
        }
        var mySwiper = new Swiper ('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationType: 'fraction'
    })

        $('#money').html(data.detail.price)
        $('#user_img').attr('src','/static/media/'+data.detail.user_avatar)
        $('#user_name').html(data.detail.user_name)
        $('.house-title').html(data.detail.title)
        $('#address').html(data.detail.address)
        $('#fangjianshu').html(data.detail.room_count)
        $('#house_area').html(data.detail.acreage)
        $('#huxing').html(data.detail.unit)
        $('#capacity').html(data.detail.capacity)
        $('#deposit').html(data.detail.deposit)
        $('#beds').html(data.detail.beds)
        $('#min_days').html(data.detail.min_days)
        if (data.detail.max_days==0){
            $('#max_days').html('无限制')
        }else{
            $('#max_days').html(data.detail.max_days)
        }
        $('.book-house').attr('href','/house/booking/?house_id=' + house_id )
    })

})
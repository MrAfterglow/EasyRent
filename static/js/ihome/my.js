function logout() {
    $.get("/api/logout", function(data){
        if (0 == data.errno) {
            location.href = "/user/login/";
        }
    })
}


$(document).ready(function () {
    $.get('/user/my_info/',function (data) {
        console.log(data)
        if (data.code==200){
            $('#user-name').html(data.user_info.name)
            $('#user-mobile').html(data.user_info.phone)
            $('#user-avatar').attr('src','/static/media/'+data.user_info.avatar)
        }
    })
})
//1.$.ajax带json数据的异步请求  
var aj = $.ajax( {    
    url:'http://168.40.5.23:9999/apis/request_route_handler/user_apis/user_get_info',// 跳转到 action    
    data:{ 
    },    
    type:'post',    
    cache:false,    
    dataType:'json',    
    success:function(data) {    
        alert(data);
        if(data.msg =="true" ){    
            // view("修改成功！");    
            alert("修改成功！");    
            window.location.reload();    
        }else{    
            view(data.msg);    
        }    
     },    
    error:function(XMLHttpRequest, textStatus, errorThrown) {
       alert(XMLHttpRequest.status);
       alert(XMLHttpRequest.readyState);
       alert(textStatus);  
     }    
});  
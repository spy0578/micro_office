//1.$.ajax带json数据的异步请求  
var aj = $.ajax( {    
    url:'http://127.0.0.1:9999/apis/request_route_handler/user_apis/user_get_info',// 跳转到 action    
    data:{ 
    },    
    type:'get',    
    cache:false,    
    async : false,
    dataType:'json',    
    success:function(data ,textStatus, jqXHR) {  
        alert("1111");  
        console.log(data.header.code);
        if(data.msg =="true" ){    
            // view("修改成功！");    
            alert("修改成功！");    
            window.location.reload();    
        }else{    
            alert(data.msg);    
        }    
     },    
    error:function(XMLHttpRequest, textStatus, errorThrown) {
       alert(XMLHttpRequest.status);
       alert(XMLHttpRequest.readyState);
       alert(textStatus);  
     }    
});  
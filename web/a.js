//1.$.ajax��json���ݵ��첽����  
var aj = $.ajax( {    
    url:'http://168.40.5.23:9999/apis/request_route_handler/user_apis/user_get_info',// ��ת�� action    
    data:{ 
    },    
    type:'post',    
    cache:false,    
    dataType:'json',    
    success:function(data) {    
        alert(data);
        if(data.msg =="true" ){    
            // view("�޸ĳɹ���");    
            alert("�޸ĳɹ���");    
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
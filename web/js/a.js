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

function fetchData(cb) {
    // 通过 setTimeout 模拟异步加载
    setTimeout(function () {
        cb({
            categories: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"],
            data: [5, 20, 36, 10, 10, 20]
        });
    }, 1000);
}

// 初始 option
option = {
    title: {
        text: '异步数据加载示例'
    },
    tooltip: {},
    legend: {
        data:['销量']
    },
    xAxis: {
        data: []
    },
    yAxis: {},
    series: [{
        name: '销量',
        type: 'bar',
        data: []
    }]
};

fetchData(function (data) {
    myChart.setOption({
        xAxis: {
            data: data.categories
        },
        series: [{
            // 根据名字对应到相应的系列
            name: '销量',
            data: data.data
        }]
    });
});
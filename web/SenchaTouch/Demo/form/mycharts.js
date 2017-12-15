var myChart = echarts.init(document.getElementById('echart'));  
var option = {  
    tooltip : {  
        trigger: 'axis'  
    },  
    toolbox: {  
        show : false,  
        feature : {  
            mark : {show: true},  
            dataView : {show: true, readOnly: false},  
            magicType: {show: true, type: ['line']},  
            restore : {show: true},  
            saveAsImage : {show: true}  
        }  
    },  
    calculable : true,  
    legend: {  
        data:['投资数','投资金额']  
    },  
    xAxis : [  
        {  
            type : 'category',  
            data : ['2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']  
        }  
    ],  
    yAxis : [  
        {  
            type : 'value',  
            name : '投资数'  
  
        },  
        {  
            type : 'value',  
            name : '投资金额'  
  
        }  
    ],  
    series : [  
        {  
            name:'投资数',  
            type:'line',  
            data:[2, 28, 30, 23, 18, 50, 64,27,55,143,51]  
        },  
        {  
            name:'投资金额',  
            type:'line',  
            yAxisIndex: 1,  
            data:[87.32, 791.92, 665.61, 1122.64, 1307.27, 1888.82, 3629.25,1197.16,2919.29,3614.21,1146.22],  
        }  
    ]  
};  
// 为echarts对象加载数据  
myChart.setOption(option);  
window.onresize = myChart.resize;  
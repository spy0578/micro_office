Ext.require([
    'Ext.form.Panel',
    'Ext.field.Password',
    'Ext.field.Number',
    'Ext.field.Spinner',
    'Ext.field.Email',
    'Ext.field.Url',
    'Ext.field.TextArea',
    'Ext.field.Radio',
    'Ext.field.Select'
    ])
Ext.application({
    name: 'MyApp',
    icon: 'images/icon.png',
    glossOnIcon: false,
    phoneStartupScreen: 'images/phone_startup.png',
    tabletStartupScreen: 'images/tablet_startup.png',
    launch: function() {      
        Ext.Msg.defaultAllowedConfig.showAnimation = false;
        Ext.Msg.defaultAllowedConfig.hideAnimation = false;        

        Ext.define('genre', {
            extend: 'Ext.data.Model',
            config: {
                fields:[
                    {name:'id',type:'int'},
                    {name:'genre',type:'string'}
                ]
            }
        });
        var genreStore=Ext.create('Ext.data.Store', {
            model: 'genre',
            autoLoad: true,
            autoDestroy:true,
            proxy:{
                type: 'ajax',
                url :'/apis/request_route_handler/bus_data_apis/position_data',
                reader:{
                    type: 'json',
                    root: 'data'
                }
            }
        });     
        genreStore.load({
            callback: function(records, operation, success){
            console.log(records);
        }
        });

        var formPanel = Ext.create('Ext.form.Panel', {
            id:'formPanel',
            scrollable:'vertical',
            items: [
            {
                xtype: 'textfield',
                id:'txt_name',
                name : 'name',
                label: '姓名',
                placeHolder:'请输入姓名',
                required:true,
                clearIcon: true
            },
            {
                xtype: 'passwordfield',
                id:'txt_password',
                name : 'password',
                label: '密码',
                placeHolder:'请输入密码',
                required:true,
                clearIcon: true
            },
            {
                xtype: 'spinnerfield',
                id:'spn_age',
                name:'age',
                label:'年龄',
                minValue:0,
                maxValue:100,
                increment: 1
            },
            {
                xtype: 'emailfield',
                id:'txt_email',
                name:'email',
                label:'Email',
                placeHolder:'请输入有效的email地址',
                clearIcon:true
            },
            {
                xtype: 'urlfield',
                id:'txt_url',
                name:'url',
                label:'个人网址',
                placeHolder:'请输入有效的网址',
                clearIcon:true
            },
            {
                xtype: 'textareafield',
                id: 'txtarea_memo',
                name:'memo',
                placeHolder:'请输入100字个人简介',
                clearIcon:true,
                maxLength: 1000,
                maxRows:4
            },
            {
                xtype:'radiofield',
                id:'rb_sex1',
                name:'sex',
                label:'男性',
                value:'male',
                checked:true,
                listeners:{
                    check: function(item,e){
                        console.log('选取了男性');
                    }
                }
            },
            {
                xtype:'radiofield',
                id:'rb_sex2',
                name:'sex',
                label:'女性',
                value:'female',
                checked:false,
                listeners:{
                    check: function(item,e){
                        console.log('选取了女性');
                    }
                }
            },
            {
                xtype: 'fieldset',
                title:'拍摄国家',
                defaults:{
                    xtype:'radiofield'
                },
                items:[
                {
                    name: 'country',
                    label:'中国',
                    value:'china'
                },
                {
                    name: 'country',
                    label:'日本',
                    value:'japan'                   
                },
                {
                    name: 'country',
                    label:'美国',
                    value:'usa'                   
                }
                 
                ]
            },
            {
                xtype: 'selectfield',
                id:'sel_genre',
                name:'genre',
                label:'种类',
                valueField:'id',
                displayField:'genre',
                store:genreStore,
                listeners:{
                    change:function(select, newValue, oldValue){
                        switch(newValue.data.value){
                            case '1':
                                Ext.Msg.alert('选择喜剧片');
                                break;
                            case '2':
                                Ext.Msg.alert('选择文艺片');
                                break;                               
                            case '3':
                                Ext.Msg.alert('选择动作片');
                                break;                               
                        }
                    }
                }
            }

            ]
        });
        Ext.Viewport.add(formPanel);

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
    }
});


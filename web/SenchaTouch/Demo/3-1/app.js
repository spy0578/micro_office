Ext.require('Ext.Img');
Ext.application({

    name: 'MyApp',
    icon: '../images/icon.png',
    glossOnIcon: false,
    phoneStartupScreen: '../images/phone_startup.png',
    tabletStartupScreen: '../images/tablet_startup.png',
    launch: function() {          
        Ext.Msg.defaultAllowedConfig.showAnimation = false;
        Ext.Msg.defaultAllowedConfig.hideAnimation = false;
        var img=Ext.create('Ext.Img',{
             src: '../images/html51.jpg',
             width:118,
             height:150,
             listeners:{
                 tap:function(){
                     Ext.Msg.alert('您单击了图片');
                 }
             }
        });
        var panel = Ext.create('Ext.Panel', {
            id:'myPanel',
            cls:'bgColorPink',
            items:[img]
        });
        Ext.Viewport.add(panel);
    }
});

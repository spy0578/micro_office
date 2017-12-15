Ext.require('Ext.SegmentedButton');
Ext.application({
    name: 'MyApp',
    icon: 'images/icon.png',
    glossOnIcon: false,
    phoneStartupScreen: 'images/phone_startup.png',
    tabletStartupScreen: 'images/tablet_startup.png',
    launch: function() {    
        var segmentedButton =Ext.create('Ext.SegmentedButton', {
            allowMultiple: true,
            items:[
            {
                text:'按钮一'
            },
            {
                text: '按钮二'
            },
            {
                text:'按钮三'
            }],
            listeners: {
                toggle: function(container,button,pressed){
                    if(pressed)
                        console.log("用户按下了 '" + button.getText() + "' 按钮");
                     else
                        console.log("用户松开了 '" + button.getText() + "' 按钮");
                }
            }
        });
          
        var myToolbar = Ext.create('Ext.Toolbar', {
            id:'mytoolbar',
            docked : 'top',
            layout:{
                type:'hbox',
                pack:'end'
            },  
            items: [segmentedButton]
        });
        var myPanel = Ext.create('Ext.Panel', {
            id:'mypanel',
            items: [myToolbar],
            html:'测试面板'
        });
        Ext.Viewport.add(myPanel);
    }
});


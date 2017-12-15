Ext.application({
    name: 'MyApp',
    icon: 'images/icon.png',
    glossOnIcon: false,
    phoneStartupScreen: 'images/phone_startup.png',
    tabletStartupScreen: 'images/tablet_startup.png',
    launch: function() {          
        var panel = Ext.create('Ext.Panel', {
            layout:'fit',
            items:[{
                style: 'background-color:pink',
                html: '示例文字1',
            },
            {
                style: 'background-color:pink',
                html: '示例文字2',
            }]
        });
        Ext.Viewport.add(panel);
    }
});







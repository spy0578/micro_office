Ext.application({
    name: 'MyApp',
    icon: 'images/icon.png',
    glossOnIcon: false,
    phoneStartupScreen: 'images/phone_startup.png',
    tabletStartupScreen: 'images/tablet_startup.png',
    launch: function() {   
        var p1=Ext.create('Ext.Panel', {
            id:'panel1',
            style: 'background-color:pink',
            html: '示例面板1'
        });   
        var p2=Ext.create('Ext.Panel', {
            id:'panel2',
            style: 'background-color:pink',
            html: '示例面板2'
        });     
        var panel = Ext.create('Ext.Panel', {
            layout:'card',
            items: [p1,p2]
        });
        Ext.Viewport.add(panel);        
        panel.setActiveItem(p2);
    }
});










Ext.application({
    name: 'MyApp',
    icon: 'images/icon.png',
    glossOnIcon: false,
    phoneStartupScreen: 'images/phone_startup.png',
    tabletStartupScreen: 'images/tablet_startup.png',
    launch: function() {     
        var panel = Ext.create('Ext.Panel', { 
            layout: {
                type : 'vbox',
                align: 'stretch'
            },
            defaults: {
                flex:1
            },
            items: [
            {
                html:'子组件1',
                style: 'background-color:pink',  
            },
            {
                html:'子组件2',
                style: 'background-color:blue;color:white',
            }]

        });        
        Ext.Viewport.add(panel); 
    }
});













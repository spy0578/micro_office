Ext.require('Ext.Carousel');
Ext.application({
    name: 'MyApp',
    icon: 'images/icon.png',
    glossOnIcon: false,
    phoneStartupScreen: 'images/phone_startup.png',
    tabletStartupScreen: 'images/tablet_startup.png',
    launch: function() { 
        var panel = Ext.create('Ext.Panel', {
            defaults:{
                ui: 'dark',
                flex:1,
                xtype:'carousel',
                defaults:{
                    xtype:'panel'
                }
            }, 
            layout: {
                type : 'vbox',
                align: 'stretch'
            },
            items: [
            { 
                id:'carousel1',
                direction: 'horizontal',
                items: [
                {
                    html: '左面板',
                    style: 'background-color:pink'
                },
                {
                    html: '中面板',
                    style: 'background-color:red'
                },
                {
                    html: '右面板',
                    style: 'background-color:yellow'
                }]
            }, 
            {
                id:'carousel2',
                direction: 'vertical',
                items: [{
                    html: '上面板',
                    style: 'background-color:pink'
                },
                {
                    html: '中面板',
                    style: 'background-color:red'
                },
                {
                    html: '下面板',
                    style: 'background-color:yellow'
                }]
            }]
        });
        Ext.Viewport.add(panel);  
        panel.getComponent('carousel1').setActiveItem(1);
    }
});















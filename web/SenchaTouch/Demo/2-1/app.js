Ext.application({
    name: 'MyApp',
    icon: 'images/icon.png',
    glossOnIcon: false,
    phoneStartupScreen: '../images/phone_startup.png',
    tabletStartupScreen: '../images/tablet_startup.png',
    launch: function() {
        var panel = Ext.create('Ext.Panel', {
            id:'myPanel',
            style:'color:red',
            html: '一个简单的示例面板'
        });

        var subPanel = Ext.create('Ext.Panel',{
            id:'mySubPanel',
            html: '面板中的子面板'
        });
        Ext.Viewport.add(panel);
        Ext.ComponentManager.get('myPanel').add(subPanel);
    }
});

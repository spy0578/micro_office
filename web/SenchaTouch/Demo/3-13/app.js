Ext.require('Ext.NavigationView')
Ext.application({
    name: 'MyApp',
    icon: 'images/icon.png',
    glossOnIcon: false,
    phoneStartupScreen: 'images/phone_startup.png',
    tabletStartupScreen: 'images/tablet_startup.png',
    launch: function() {     
        var view = Ext.create('Ext.NavigationView', {
            navigationBar: {
                ui: 'pink',
                docked: 'top'
            },
            //useTitleForBackButtonText:true,
            items: [{
                title: '标题一',
                html:'组件1'
            },
            {
                title: '标题二二',
                html:'组件22'
            }]
        });
        panel=Ext.create('Ext.Panel',{
            title: '标题二',
            html:'组件2'
        });
        Ext.Viewport.add(view); 
        view.push(panel);
        panel=Ext.create('Ext.Panel',{
            title: '标题三',
            html:'组件3'
        });
        view.push(panel);
        view.pop();
    }
}); 














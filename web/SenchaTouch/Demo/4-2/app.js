Ext.require('Ext.form.Panel')
Ext.application({
    name: 'MyApp',
    icon: 'images/icon.png',
    glossOnIcon: false,
    phoneStartupScreen: 'images/phone_startup.png',
    tabletStartupScreen: 'images/tablet_startup.png',
    launch: function() {      
        var formPanel = Ext.create('Ext.form.Panel', {
            id:'formPanel',
            scrollable:'vertical'
        });
        for(var i=0;i<15;i++)
        {
            var field = Ext.create('Ext.form.Text', {
                id:'txt_field'+i,
                label:'标签'+i,
                value:'示例文字'+i
            });
            formPanel.add(field);
        }
        Ext.Viewport.add(formPanel);
        formPanel.getScrollable().getScroller().setFps(100);
        formPanel.getScrollable().getScroller().scrollTo(0,200);
        formPanel.getScrollable().getScroller().scrollToEnd();        
    }
});
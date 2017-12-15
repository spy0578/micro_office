Ext.require(['Ext.form.Panel','Ext.form.FieldSet'])
Ext.application({
    name: 'MyApp',
    icon: 'images/icon.png',
    glossOnIcon: false,
    phoneStartupScreen: 'images/phone_startup.png',
    tabletStartupScreen: 'images/tablet_startup.png',
    launch: function() {          
        var formPanel = Ext.create('Ext.form.Panel', {
            id:'formPanel',
            baseCls:'bgPink',
            //cls:'smallfont',
            scrollable:'vertical',
            items: [{
                xtype:'fieldset',
                title:'电影信息',
                instructions:'请填写电影信息',
                defaults:{
                    labelwidth:'20%'
                },
                items: [
                {
                    xtype: 'textfield',
                    id:'txt_title',
                    name : 'title',
                    label: '标题',
                    placeHolder:'请输入电影标题',
                    required:true,
                    clearIcon: true,
                    listeners:{
                        change:function(item, newValue, oldValue){
                            console.log("修改前的值为："+oldValue);
                            console.log("修改后的值为："+newValue);
                        }
                    }
                },
                {
                    xtype: 'textfield',
                    id:'txt_director',
                    name : 'director',
                    label: '导演',
                    placeHolder:'请输入导演名称',
                    clearIcon: true,
                    disabled:true,
                    disabledCls:'disabled'
                }]
            }]
        });
        Ext.Viewport.add(formPanel);
    }
});

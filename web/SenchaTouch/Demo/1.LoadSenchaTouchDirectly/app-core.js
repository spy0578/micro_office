
Ext.Loader.setPath({
    'Ext': '../../SenchaTouch/2.0.0/src'
});

Ext.require(['Ext.form.FieldSet', 'Ext.picker.Picker', 'Ext.TitleBar']);


Ext.application({
    name: 'Demo',
    viewport: {
        autoMaximize: true // 该属性可以设置页面自动最大化（隐藏地址栏）
    },

    launch: function () {
        Ext.create("Ext.Panel", {
            fullscreen: true,
            items: [
				{
				    xtype: 'fieldset',
				    margin: 10,
				    title: '文本框与Picker结合实例',
				    items: [
						{
						    xtype: 'textfield',
						    name: 'aTextField',
						    id: 'aTextField',
						    readOnly: true,         // 把文本框设为只读，禁止输入
						    label: '取值结果',
						    clearIcon: true,
						    listeners: {
						        // 侦听文本框的focus事件，获取到焦点时触发
						        focus: function () {
						            this.disable();                 // 先禁用文本框，防止系统调出软键盘
						            Ext.getCmp('aPicker').show();   // 显示用来选择内容的Picker
						        }
						    }
						}
					]
				}
			]
        });

        // 定义一个Picker供文本框联动
        aPicker = Ext.create('Ext.Picker', {
            name: 'aPicker',
            id: 'aPicker',
            hidden: true,
            listeners: {
                // 侦听change事件，Picker的值改变同时也设定文本框的值
                change: function () {
                    Ext.getCmp('aTextField').setValue(aPicker.getValue().question);
                },
                // 侦听hide事件，当Picker消失时将文本框状态设为enable
                hide: function () {
                    Ext.getCmp('aTextField').enable();
                }
            },
            slots: [
				{
				    name: 'question',
				    data: [
						{
						    text: '无',
						    value: ''
						},
						{
						    text: '最喜欢的颜色',
						    value: 'color'
						},
						{
						    text: '最喜欢的运动',
						    value: 'sport'
						},
						{
						    text: '最喜欢的明星',
						    value: 'star'
						}
					]
				}
			]
        });

        // 前面定义的Picker控件必须显式加入Viewport，否则无法被调用显示
        // Ext.Viewport是Sencha Touch自动创建的一个最顶级容器
        Ext.Viewport.add(aPicker);
    }
});
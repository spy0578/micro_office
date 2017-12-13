    Ext.application({  
        name: 'sample',  
      
        launch: function() {  
            Ext.Msg.defaultAllowedConfig.showAnimation = false;
            Ext.Msg.defaultAllowedConfig.hideAnimation = false;
            var tabPanel = Ext.create("Ext.tab.Panel", {
                fullscreen: true,
                tabBarPosition: 'bottom',

                defaults: {  
                    styleHtmlContent: true,  
                    tabBarPosition: 'bottom',  
                },  
              
                layout: {  
                    type: 'card',  
                    animation: {  
                        type: 'fade'  
                    }  
                },      
                
                items: [  
                    {  
                        title: 'Home',  
                        iconCls: 'home',  
                        html: 'Home Screen'  
                    },  
                    {  
                        title: 'Contact',  
                        iconCls: 'user',  
                        html: 'Contact Screen'  
                    }  
                ]              
            });        
            var formPanel = Ext.create('Ext.form.Panel', {  
                title: 'presidents',
                iconCls: 'team',

                items: [{  
                    xtype: 'fieldset',  
                    items: [  
                        {  
                            xtype: 'textfield',  
                            name : 'name',  
                            label: 'Name'  
                        },  
                        {  
                            xtype: 'emailfield',  
                            name : 'email',  
                            label: 'Email'  
                        },  
                        {  
                            xtype: 'passwordfield',  
                            name : 'password',  
                            label: 'Password'  
                        }  
                    ]  
                }]  
            });  
            
            console.log("FFFF");
            
            formPanel.add({  
                xtype: 'toolbar',  
                docked: 'bottom',  
                layout: { pack: 'center' },  
                items: [  
                    {  
                        xtype: 'button',  
                        text: 'Set Data',  
                        handler: function() {  
                            formPanel.setValues({  
                                name: 'Ed',  
                                email: 'ed@sencha.com',  
                                password: 'secret'  
                            })  
                        }  
                    },  
                    {  
                        xtype: 'button',  
                        text: 'Get Data',  
                        handler: function() {  
                            Ext.Msg.alert('Form Values', JSON.stringify(formPanel.getValues(), null, 2));  
                        }  
                    },  
                    {  
                        xtype: 'button',  
                        text: 'Clear Data',  
                        handler: function() {  
                            formPanel.reset();  
                        }  
                    },  
                    {  
                        xtype: 'button',  
                        text: 'Submit',  
                        handler: function() {  
                            console.log('username:'+formPanel.getValues()['name']);
                            Ext.Ajax.request({  
                                url: '/apis/request_route_handler/user_apis/user_get_info',  
                                method: 'POST', 
                                params: {
                                    name: formPanel.getValues()['name'],
                                    password: formPanel.getValues()['password']
                                }, 
                                success: function(response) {  
                                    console.log(response);
                                    Ext.Msg.alert("fff");
                                },
                                failure: function(response, opts) {  
                                    console.log(response);
                                    //alert('form submitted successfully!');  
                                }    
                            });  
                        }  
                    }  
                ]  
            });  
            tabPanel.add(formPanel);
        }  
    });  
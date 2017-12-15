    Ext.application({  
        name: 'sample',  
      
        launch: function() {  
            Ext.Msg.defaultAllowedConfig.showAnimation = false;
            Ext.Msg.defaultAllowedConfig.hideAnimation = false;
            var tabPanel = Ext.create("Ext.tab.Panel", {
                fullscreen: true,
                tabBarPosition: 'top',

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
                
                /*
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
                */             
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

            Ext.define('Name',{
                extend:'Ext.data.Model',  
                config:{
                    fields: ['firstName', 'lastName']
                }
            });

            var store = Ext.create('Ext.data.Store', {
                model: 'Name',//Store创建的时候会根据模型，对数据进行加工处理。
                data: [     //直接把数组作为数据配置项。这些数据会被加工处理，最终形成record数组。
                    {firstName: 'Tommy', lastName: 'Maintz'},
                    {firstName: 'Ed', lastName: 'Spencer'},
                    {firstName: 'Jamie', lastName: 'Avins'},
                    {firstName: 'Aaron', lastName: 'Conran'},
                    {firstName: 'Dave', lastName: 'Conran'},
                    {firstName: 'Michael', lastName: 'Mullany'},
                    {firstName: 'Abraham', lastName: 'Elias'},
                    {firstName: 'Jay', lastName: 'Robinson'},
                    {firstName: 'Tommy', lastName: 'Maintz'},
                    {firstName: 'Ed', lastName: 'Spencer'},
                    {firstName: 'Jamie', lastName: 'Avins'},
                    {firstName: 'Aaron', lastName: 'Conran'},
                    {firstName: 'Ape', lastName: 'Evilias'},
                    {firstName: 'Dave', lastName: 'Kaneda'}
                ]
            });

            var nameList = Ext.create('Ext.dataview.List', {
                title: 'namelist',  
                iconCls: 'home',
                itemTpl: '{firstName} {lastName}',
                store: store //通过配置项实现store的绑定。
            });

            tabPanel.add(nameList);

            //定义一个Model  
            Ext.define('BookInfo',{  
             extend:'Ext.data.Model',  
             config:{  
                 fields:['image_url','book_name','author','description']  
             }  
            });  

            //存储类（Store）封装了一个客户端缓存的模型对象,通过proxy来加载数据  
            var bookStore=Ext.create('Ext.data.Store',{  
                model:'BookInfo',  
                autoLoad:true,  
                proxy:{  
                  type:'ajax',  
                  url:'bookInfo.json',  
                  reader:{  
                       type:'json',  
                       rootProperty:'books'  //这里的 books是传递过来JSON数据的一个books节点，里面是bookInfo对象数组,如果上面还有节点,就是xxx.books  
                  }  
                }  
            });  

            //定义一个tpl模板,用来在页面显示数据  
            var bookTempalte=new Ext.XTemplate(  
                    '<tpl for=".">',  
                    '<div class="Book_img"><img src={image_url} /></div>',  
                    '<div class="Book_info">',  
                    '<h2>{book_name}</h2><br><h3>作者:{author}</h3>',  
                    '<p>{description:ellipsis(40)}</p>',  
                    '</div>',  
                    '</tpl>'  
            );  

            //dataview  
            var dataview=Ext.create('Ext.DataView',{  
                title: 'data',  
                iconCls: 'home',  
                store:bookStore,  
                itemTpl:bookTempalte,  
                baseCls:'Book'     //指的是Book-item样式  
            });     
             
            tabPanel.add(dataview);
         
        }  
    });  
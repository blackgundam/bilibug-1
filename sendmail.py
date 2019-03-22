from google.appengine.api import mail
mail.send_mail('blackgundamwyr@gmail.com',
       'wyr629@hotmail.com',
       u'发现红包', #中文必须写成unicode，不然会变成乱码
       'rt',
       html = u'<a href="http://bbs.kidfanschannel.net/discuz/plugin.php?identifier=get_money&module=money&action=money_get&hid=2">领取红包</a>')

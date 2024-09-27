updateissendisInacrive = """ update Notification set issend = 1 where id in {0} """

emailaccount = """ Select Host,Port,EnableSSL,FromMail,DisplayName,UserName,Password From Prod.EmailConfig Where SuperId = {0} and IsActive = 1"""

insertmailqueue = """ Insert into dbo.EmailQueue(SuperId,ToAddress,Subject,Message,CreatedOn) values ({0},'{1}','{2}','{3}',GetDate()) """

emailqueue = """ select Top {0} * from dbo.V_MailQueue WHERE createdon >= DATEADD(HOUR, -24, GETDATE());"""
updatemailqueue = """ Update dbo.EmailQueue set IsProcessed = 1 where Id in ({0})"""

whatsappaccount = """ Select HostUrl,APIKey From Prod.Whatsappconfig Where SuperId = {0} and IsActive = 1"""

smsaccount = """ Select APIUrl,APIKey,SenderId,UserName From Prod.SMSconfig Where SuperId = {0} and IsActive = 1"""

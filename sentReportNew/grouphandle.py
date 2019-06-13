import codecs
from sentReportNew import models
import itchat
from wxpy import *


class groupinfo:

    ibot = None

    def __init__(self, currentbot):
        self.ibot = currentbot
        return

    def getUserGroup(self, msg):

        mygroup = self.ibot.groups().search(msg.chat.name)[0]

        for val in mygroup:
            # print(val)
            try:
                models.SGroupInfo.objects.create(
                    robot_id='R001',
                    chatroom_id=mygroup.puid,
                    chatroom_name=msg.chat.name,
                    user_name=val.name,
                    user_status='1',
                    user_id=val.puid)
            except Exception as err:
                print(err)

        return

    def addUserinfo(self, msg, addname):

        mygroup = self.ibot.groups().search(msg.chat.name)[0]
        mygroup.update_group(members_details=False)

        for val in mygroup:
            if val.name == addname:
                try:
                    models.SGroupInfo.objects.create(
                        robot_id='R001',
                        chatroom_id=mygroup.puid + '@chatroom',
                        chatroom_name=msg.chat.name,
                        user_name=val.name,
                        user_status='1',
                        user_id='wxid_' + val.puid)
                except Exception as err:
                    print(err)
        return
    def recordMsg(self, msg, groupName, senderName):
        try:
            models.SGroupMsg.objects.create(
                chatroom_id='1',
                user_name=senderName,
                message=msg.text,
                chatroom_name=groupName)
        except Exception as err:
            print(err)

        return

    def removeMember(self, msg, name):
        mygroup = self.ibot.groups().search(msg.chat.name)[0]

        for val in mygroup:
            if val.name == name:
                try:
                    models.SGroupOutInfo.objects.create(
                        community_id='',
                        community_name='',
                        chatroom_id=mygroup.puid + '@chatroom',
                        chatroom_name=msg.chat.name,
                        user_name=val.name,
                        user_id='wxid_' + val.puid)
                    models.SGroupInfo.objects.filter(chatroom_name=msg.chat.name,user_name=val.name).delete()
                except Exception as err:
                    print(err)
        return

    def loginCallback(self):
        print("***登录成功***")

    def exitCallback(self):
        print("***已退出***")

    def grouplivevoice(self, groupname, sendername, msg):  # 直播

        # 转发语音
        mygroup = self.ibot.groups().search("社群技术小组")[0]
        msg.forward(mygroup, prefix='老板发言')

        return

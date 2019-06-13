from wxpy import *
import json, sys, requests
from sentReportNew.city import cityname
from sentReportNew.weather import weather
import pkuseg
import re
import chardet

from sentReportNew.grouphandle import groupinfo

bot = Bot(console_qr=0, cache_path="botoo.pkl")
bot.enable_puid()

def SentChatRoomsMsg(name, msg):
    name='社群技术小组'
    userName=''
    itchat=bot.core
    itchat.get_chatrooms(update=True)
    iRoom = itchat.search_chatrooms(name)
    for room in iRoom:
        fcode=chardet.detect(room['NickName'])
        print(fcode)
        if room['NickName'] == name:
            userName = room['UserName']
            break
    itchat.send_msg('hello', userName)
    return

def setMsgToGroup():
    setreport('北京')
    return
def setreport(cityname,groupname):
    print("开始")

    # 搜索名称含有 "游否" 的男性深圳好友
    my_friend = bot.groups().search(groupname)[0]
    # 发送文本给好友
    newweather=weather()
    my_friend.send(newweather.getwehther(cityname))
    print("完成")
    return

def tulin_reply(text):
    url = "http://www.tuling123.com/openapi/api"
    api_key = "ffc83115b4014e80b5d1c6c22c6db11a"
    payload = {
                     "key": api_key,
                     "info": text,
                 }
    # 接口要求传json格式字符串,返回数据是json格式
    result= requests.post(url, data=json.dumps(payload)).json()
    # result = json.loads(r.text)
    return result["text"]
def getcityname(text):
    seg = pkuseg.pkuseg()   #以默认配置加载模型
    srcArray = seg.cut(text)    #进行分词
    print(srcArray)

    for val in cityname:
        if val in srcArray:
            print('faxian'+val)
            return val
    print('not find')
    return None
@bot.register([Group],NOTE)
def welcome(msg):
    print("收到提示信息")
    print(msg.text)
    pattern = re.compile('邀请"(.*)"加入')
    text = msg.text
    invitename=pattern.findall(text)
    print(invitename)
    if '邀请你加入了群聊' in msg.text:
        grp = groupinfo(bot)
        grp.getUserGroup(msg)
        return

    if '加入' in text:
        grp = groupinfo(bot)
        grp.addUserinfo(msg,invitename[0])
        return "热烈欢迎"+invitename[0]+"加入本群！"
    if '移出' in text:
        pattern1 = re.compile('将"(.*)"移出')
        grp = groupinfo(bot)
        grp.removeMember(msg, invitename[0])
        return
    else:
        print("不是邀请！")

    return None
##@bot.register()
@bot.register([Group],TEXT,PICTURE,VIDEO,RECORDING)
def auto_reply(msg):
    print("收到消息")
    print(msg)
    grp=groupinfo(bot)
    grp.recordMsg(msg,msg.sender.name,msg.member.name)
    # grp.grouplivevoice(msg.sender.name,msg.member.display_name,msg)
    SentChatRoomsMsg('aa','bb')
    '''
    print("start")
    # 启用 puid 属性，并指定 puid 所需的映射数据保存/载入路径
    bot.enable_puid('wxpy_puid.pkl')

    # 指定一个好友
    my_friend = bot.friends().search('尤亚伟')[0]

    # 查看他的 puid
    print(my_friend.puid)
    '''
    # 如果是群聊，但没有被 @，则不回复
    if isinstance(msg.chat, Group) and not msg.is_at:
            if u"姿美堂扯淡" in msg.text:
                print(msg.chat)
                grp.removeMember(msg.sender.name,"乐逍遥")
                return '警告，请各位注意言行！'
            return
    else:
            # 回复消息内容和类型
            if u'天气' in msg.text:
                newcity=getcityname(msg.text)
                if newcity == None:
                    return "抱歉，您要求城市不在服务序列"
                else:
                    return  setreport(newcity,msg.sender.name)
            else:
                return tulin_reply(msg.text)

embed()

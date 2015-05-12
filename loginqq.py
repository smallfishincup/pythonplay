import urllib.parse, urllib.request, http.cookiejar, hashlib, re, json, os, tempfile


"""cookie"""
cookie=http.cookiejar.CookieJar()
chandle=urllib.request.HTTPCookieProcessor(cookie)

def get(url, header = False):
    if header:
        r = urllib.request.Request(url, headers = header)
    else:
        r = urllib.request.Request(url)
    opener = urllib.request.build_opener(chandle)
    u = opener.open(r)
    data = u.read()
    try:
        data = data.decode('utf-8')
    except:
        data = data.decode('gbk', 'ignore')
    return data

def post(url, data, header = False):
    data = urllib.parse.urlencode(data)
    data = bytes(data,'utf-8')
    if header:
        r = urllib.request.Request(url, data, headers = header)
    else:
        r = urllib.request.Request(url, data)
    opener = urllib.request.build_opener(chandle)
    u = opener.open(r)
    data = u.read()
    try:
        data = data.decode('utf-8')
    except:
        data = data.decode('gbk', 'ignore')
    return data

class QQ:
    num         = ""
    pwd         = ""
    login_sig     = ""
    appid         = 549000912
    qzreferrer     = ""

    def __init__(self, num, pwd):
        self.num = num
        self.pwd = pwd
        self.check()
        self.login()

    def check(self):
        par = {
            'appid'                : self.appid,
            'daid'                : 5,
            'hide_title_bar'    : 1,
            'link_target'        : "blank",
            'low_login'            : 0,
            'no_verifyimg'        : 1,
            'proxy_url'            : "http://qzs.qq.com/qzone/v6/portal/proxy.html",
            'pt_qr_app'            : "手机QQ空间",
            'pt_qr_help_link'    : "http://z.qzone.com/download.html",
            'pt_qr_link'        : "http://z.qzone.com/download.html",
            'pt_qzone_sig'        : 1,
            'qlogin_auto_login'    : 1,
            's_url'                : "http://qzs.qq.com/qzone/v5/loginsucc.html?para=izone",
            'self_regurl'        : "http://qzs.qq.com/qzone/v6/reg/index.html",
            'style'                : 22,
            'target'            : "self"
        }
        url = "http://xui.ptlogin2.qq.com/cgi-bin/xlogin?%s" % urllib.parse.urlencode(par)
        self.login_sig = re.findall('login_sig:"([^"]+)"', get(url))[0]
        par = {
            'appid'                : self.appid,
            'js_type'            : 1,
            'js_ver'            : 10076,
            'login_sig'            : self.login_sig,
            'r'                    : 0.8861454421075537,
            'regmaster'            : "",
            'u1'                : "http://qzs.qq.com/qzone/v5/loginsucc.html?para=izone",
            'uin'                : self.num
        }
        url = 'http://check.ptlogin2.qq.com/check?%s' % urllib.parse.urlencode(par)
        li =  re.findall("'([^']+)'", get(url))
        print(li)
        if len(li) == 4:
            self.flag, self.vcode, self.uin, _ = li
        elif len(li) == 3:
            self.flag, self.vcode, self.uin    = li
        else:
            print("不按套路出牌啊...")

        if self.flag == "1":
            self.getCode()

    def getPwd(self):
        str = hashlib.md5(self.pwd.encode())
        str = str.digest()
        str = hashlib.md5((str + int(self.num).to_bytes(8, "big")))
        str = str.hexdigest().upper()
        str = hashlib.md5((str + self.vcode.upper()).encode())
        return str.hexdigest().upper()

    def getCode(self):
        par = {
            'uin'        : self.num,
            'aid'        : self.appid,
            'cap_cd'    : self.vcode
        }
        url = 'http://captcha.qq.com/getimage?%s' % urllib.parse.urlencode(par)
        r = urllib.request.Request(url)
        opener = urllib.request.build_opener(chandle)
        u = opener.open(r)
        data = u.read()
        tmp = tempfile.mkstemp(suffix='.png')
        os.write(tmp[0], data)
        os.close(tmp[0])
        os.startfile(tmp[1])
        self.vcode = input("验证码：")


    def login(self):
        par = {
            'action'            : "5-20-1314",
            'aid'                : self.appid,
            'daid'                : 5,
            'from_ui'            : 1,
            'g'                    : 1,
            'h'                    : 1,
            'js_type'            : 1,
            'js_ver'            : 10076,
            'login_sig'            : self.login_sig,
            'p'                    : self.getPwd(),
            'pt_qzone_sig'        : 1,
            'pt_rsa'            : 0,
            'ptlang'            : 2052,
            'ptredirect'        : 0,
            't'                    : 1,
            'u'                    : self.num,
            'u1'                : "http://qzs.qq.com/qzone/v5/loginsucc.html?para=izone",
            'verifycode'        : self.vcode
        }

        url = "http://ptlogin2.qq.com/login?%s" % urllib.parse.urlencode(par)
        header = {
            'Host'            : "ptlogin2.qq.com",
            'User-Agent'    : "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0"
        }
        s = get(url, header)
        print(s)
        li = re.findall("'([^']+)'", get(url))

        if not int(li[0]):
            self.qzreferrer = li[2]
            print("你好，%s" % li[len(li) - 1])
            return True
        else:
            return False


    def gtk(self):
        for x in cookie:
            if x.name == "skey":
                hash = 5381;
                for c in x.value:
                    hash += (hash << 5) + ord(c)
                return hash & 0x7fffffff;


    def feed(self, txt, pic = False):
        url = "http://taotao.qq.com/cgi-bin/emotion_cgi_publish_v6?g_tk=%d" % self.gtk()
        par = {
            'code_version'        : 1,
            'con'                : txt,
            'feedversion'        : 1,
            'format'            : "fs",
            'hostuin'            : self.num,
            'paramstr'            : 1,
            'pic_template'        : "",
            'qzreferrer'        : self.qzreferrer,
            'richtype'            : "",
            'richval'            : "",
            'special_url'        : "",
            'subrichtype'        : "",
            'syn_tweet_verson'    : 1,
            'to_sign'            : 0,
            'to_tweet'            : 0,
            'ugc_right'            : 1,
            'ver'                : 1,
            'who'                : 1
        }
        if not int(re.findall('"subcode":([\d\-]+)', post(url, par))[0]):
            return True
        else:
            return False

    def friend(self):
        par = {
            'uin'             : self.num,
            'rd'            : 0.5437208298024628,
            'do'            : 1,
            'fupdate'        : 1,
            'clean'            : 1,
            'g_tk'            : self.gtk()
        }
        url = "http://r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?%s" % urllib.parse.urlencode(par)
        s = get(url)
        uin = re.findall('"uin":(\d+)[,\s]+"name":"([^"]+)"', s)

        for x in uin:
            print(x) #有些好友的名字可能无法输出，涉及utf8与gbk编码问题，可自行注释

    def getFeed(self):

        par = {
            'uin'                    : 2672873136,
            'ftype'                    : 0,
            'sort'                    : 0,
            'pos'                    : 0,
            'num'                    : 20,
            'replynum'                : 100,
            'g_tk'                    : self.gtk(),
            'callback'                : "_preloadCallback",
            'code_version'            : 1,
            'format'                : "jsonp",
            'need_private_comment'    : 1
        }

        js = json.loads(re.findall(r'{.+}', get('http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?%s' % urllib.parse.urlencode(par)))[0])
account = input("帐号：")
password = input("密码：")
qq = QQ(account, password)
os.system("pause")
# qq.feed("I'm Spider-Man")
# qq.friend()

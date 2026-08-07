# -*- coding: utf-8 -*-
"""
英文 -> (美式IPA音标, 中文谐音) 引擎
基于 CMU 发音词典(ARPABET, 通用美音)，而不是拼写猜测。
"""
import re, cmudict

CMU = cmudict.dict()

# ---------------------------------------------------------------- ARPABET -> IPA
IPA = {
    'AA':'ɑ','AE':'æ','AH0':'ə','AH':'ʌ','AO':'ɔ','AW':'aʊ','AY':'aɪ',
    'EH':'ɛ','ER0':'ɚ','ER':'ɝ','EY':'eɪ','IH':'ɪ','IY':'i','OW':'oʊ',
    'OY':'ɔɪ','UH':'ʊ','UW':'u',
    'B':'b','CH':'tʃ','D':'d','DH':'ð','F':'f','G':'ɡ','HH':'h','JH':'dʒ',
    'K':'k','L':'l','M':'m','N':'n','NG':'ŋ','P':'p','R':'r','S':'s','SH':'ʃ',
    'T':'t','TH':'θ','V':'v','W':'w','Y':'j','Z':'z','ZH':'ʒ',
}
VOWELS = {'AA','AE','AH','AO','AW','AY','EH','ER','EY','IH','IY','OW','OY','UH','UW'}

def base(p):
    return re.sub(r'\d$', '', p)

def stress(p):
    m = re.search(r'(\d)$', p)
    return int(m.group(1)) if m else -1

def sym(p):
    b, s = base(p), stress(p)
    if b == 'AH' and s == 0:   return IPA['AH0']
    if b == 'ER' and s == 0:   return IPA['ER0']
    return IPA[b]

# ---------------------------------------------------------------- 音节切分
LEGAL_ONSET = {
 ('P','L'),('B','L'),('K','L'),('G','L'),('F','L'),('S','L'),
 ('P','R'),('B','R'),('T','R'),('D','R'),('K','R'),('G','R'),('F','R'),('TH','R'),('SH','R'),
 ('S','P'),('S','T'),('S','K'),('S','M'),('S','N'),('S','W'),('T','W'),('K','W'),('D','W'),('G','W'),
 ('P','Y'),('B','Y'),('K','Y'),('F','Y'),('M','Y'),('V','Y'),('HH','Y'),('N','Y'),('L','Y'),('T','Y'),('D','Y'),
}
LEGAL_ONSET3 = {('S','P','L'),('S','P','R'),('S','T','R'),('S','K','R'),('S','K','W'),('S','K','L')}

def syllabify(phones):
    """返回 [(onset[], nucleus, coda[]), ...]"""
    vi = [i for i, p in enumerate(phones) if base(p) in VOWELS]
    if not vi:
        return [(list(phones), None, [])] if phones else []
    syls = []
    for k, v in enumerate(vi):
        if k == 0:
            onset = list(phones[0:v])
        else:
            run = list(phones[vi[k-1]+1:v])
            n = len(run)
            take = 0
            if n >= 3 and tuple(base(x) for x in run[-3:]) in LEGAL_ONSET3: take = 3
            elif n >= 2 and tuple(base(x) for x in run[-2:]) in LEGAL_ONSET:  take = 2
            elif n >= 1: take = 1
            onset = run[n-take:] if take else []
            syls[-1] = (syls[-1][0], syls[-1][1], syls[-1][2] + run[:n-take])
        coda = list(phones[v+1:]) if k == len(vi)-1 else []
        syls.append((onset, phones[v], coda))
    return syls

def to_ipa(phones):
    syls = syllabify(phones)
    res, idx = [], 0
    multi = len(syls) > 1
    for onset, nuc, coda in syls:
        n = len(onset) + (1 if nuc is not None else 0) + len(coda)
        chunk = ''.join(sym(phones[idx + k]) for k in range(n))
        if multi and nuc is not None:
            st = stress(nuc)
            if st == 1: chunk = 'ˈ' + chunk
            elif st == 2: chunk = 'ˌ' + chunk
        res.append(chunk)
        idx += n
    return ''.join(res)

# ---------------------------------------------------------------- 谐音
V2F = {'AA':'a','AE':'ai','AH1':'a','AH2':'a','AH0':'e','AO':'ao','AW':'ao',
       'AY':'ai','EH':'ai','ER':'e','EY':'ei','IH':'i','IY':'i','OW':'ou',
       'OY':'o','UH':'u','UW':'u'}
MERGE_N  = {'AA','AE','AH0','AH1','AH2','EH','IH','IY','AO','UH'}
FIN_N  = {'a':'an','ai':'an','e':'en','ao':'ang','i':'in','u':'un'}
FIN_NG = {'a':'ang','ai':'ang','e':'eng','ao':'ang','i':'ing','u':'ong'}

def vkey(p):
    b, s = base(p), stress(p)
    if b == 'AH': return 'AH0' if s == 0 else 'AH1'
    return b

C2I = {'B':'b','P':'p','M':'m','F':'f','V':'w','D':'d','T':'t','N':'n','L':'l',
       'G':'g','K':'k','HH':'h','S':'s','Z':'z','TH':'s','DH':'z','SH':'sh',
       'ZH':'r','CH':'ch','JH':'zh','R':'r','W':'w','Y':'y'}
C_SOLO_ONSET = {'B':'布','P':'普','M':'姆','F':'夫','V':'夫','D':'德','T':'特','N':'恩',
                'L':'勒','G':'格','K':'克','HH':'赫','S':'斯','Z':'兹','TH':'斯','DH':'兹',
                'SH':'什','ZH':'日','CH':'奇','JH':'吉','R':'尔','W':'乌','Y':'伊','NG':'恩'}
C_SOLO_CODA  = dict(C_SOLO_ONSET)
C_SOLO_CODA.update({'L':'尔','R':'尔','NG':'恩','HH':''})

PY = {
'a':{'b':'巴','p':'帕','m':'马','f':'法','d':'达','t':'塔','n':'那','l':'拉','g':'嘎','k':'卡','h':'哈',
     'zh':'扎','ch':'查','sh':'沙','r':'拉','z':'扎','c':'擦','s':'萨','y':'亚','w':'瓦','':'阿'},
'ai':{'b':'拜','p':'派','m':'麦','f':'费','d':'戴','t':'泰','n':'奈','l':'莱','g':'盖','k':'凯','h':'海',
     'zh':'杰','ch':'切','sh':'谢','r':'瑞','z':'在','c':'猜','s':'塞','y':'耶','w':'歪','':'艾'},
'ei':{'b':'贝','p':'佩','m':'梅','f':'飞','d':'戴','t':'泰','n':'内','l':'雷','g':'给','k':'凯','h':'黑',
     'zh':'哲','ch':'车','sh':'谢','r':'瑞','z':'贼','c':'测','s':'赛','y':'耶','w':'威','':'诶'},
'i':{'b':'比','p':'皮','m':'米','f':'菲','d':'迪','t':'提','n':'尼','l':'里','g':'吉','k':'基','h':'希',
     'zh':'吉','ch':'奇','sh':'希','r':'瑞','z':'兹','c':'齐','s':'西','y':'伊','w':'威','':'伊'},
'u':{'b':'布','p':'普','m':'木','f':'夫','d':'杜','t':'图','n':'努','l':'鲁','g':'古','k':'酷','h':'胡',
     'zh':'朱','ch':'初','sh':'书','r':'如','z':'租','c':'粗','s':'苏','y':'优','w':'伍','':'乌'},
'ou':{'b':'波','p':'颇','m':'摸','f':'佛','d':'都','t':'透','n':'诺','l':'洛','g':'购','k':'扣','h':'侯',
     'zh':'周','ch':'抽','sh':'收','r':'罗','z':'走','c':'凑','s':'搜','y':'哟','w':'沃','':'欧'},
'ao':{'b':'包','p':'泡','m':'毛','f':'福','d':'道','t':'套','n':'闹','l':'劳','g':'高','k':'考','h':'好',
     'zh':'招','ch':'超','sh':'少','r':'绕','z':'早','c':'草','s':'扫','y':'要','w':'沃','':'奥'},
'e':{'b':'伯','p':'珀','m':'默','f':'弗','d':'德','t':'特','n':'呢','l':'勒','g':'格','k':'克','h':'赫',
     'zh':'哲','ch':'彻','sh':'舍','r':'惹','z':'泽','c':'策','s':'瑟','y':'耶','w':'沃','':'额'},
'o':{'b':'波','p':'坡','m':'摩','f':'佛','d':'多','t':'托','n':'诺','l':'罗','g':'果','k':'阔','h':'火',
     'zh':'卓','ch':'戳','sh':'说','r':'若','z':'左','c':'搓','s':'索','y':'哟','w':'沃','':'奥'},
'an':{'b':'班','p':'潘','m':'曼','f':'凡','d':'丹','t':'坦','n':'南','l':'兰','g':'甘','k':'坎','h':'汉',
     'zh':'占','ch':'产','sh':'山','r':'然','z':'赞','c':'参','s':'散','y':'言','w':'万','':'安'},
'en':{'b':'本','p':'喷','m':'门','f':'芬','d':'登','t':'腾','n':'嫩','l':'冷','g':'根','k':'肯','h':'很',
     'zh':'真','ch':'陈','sh':'神','r':'仁','z':'怎','c':'岑','s':'森','y':'言','w':'温','':'恩'},
'in':{'b':'宾','p':'品','m':'民','f':'芬','d':'丁','t':'听','n':'您','l':'林','g':'金','k':'金','h':'欣',
     'zh':'金','ch':'亲','sh':'心','r':'林','z':'津','c':'亲','s':'辛','y':'因','w':'温','':'因'},
'ang':{'b':'邦','p':'旁','m':'忙','f':'方','d':'当','t':'汤','n':'囊','l':'朗','g':'刚','k':'康','h':'航',
     'zh':'张','ch':'昌','sh':'商','r':'让','z':'脏','c':'仓','s':'桑','y':'扬','w':'汪','':'昂'},
'eng':{'b':'崩','p':'彭','m':'蒙','f':'风','d':'登','t':'疼','n':'能','l':'冷','g':'更','k':'坑','h':'恒',
     'zh':'正','ch':'成','sh':'生','r':'仍','z':'增','c':'层','s':'僧','y':'英','w':'翁','':'嗯'},
'ing':{'b':'冰','p':'平','m':'明','f':'风','d':'丁','t':'听','n':'宁','l':'灵','g':'京','k':'金','h':'兴',
     'zh':'京','ch':'清','sh':'星','r':'林','z':'京','c':'青','s':'星','y':'英','w':'温','':'英'},
'ong':{'b':'蓬','p':'蓬','m':'蒙','f':'风','d':'东','t':'通','n':'农','l':'龙','g':'工','k':'空','h':'红',
     'zh':'中','ch':'冲','sh':'松','r':'荣','z':'总','c':'从','s':'松','y':'永','w':'翁','':'翁'},
'un':{'b':'本','p':'喷','m':'门','f':'芬','d':'顿','t':'吞','n':'嫩','l':'伦','g':'滚','k':'昆','h':'混',
     'zh':'准','ch':'春','sh':'顺','r':'润','z':'尊','c':'村','s':'孙','y':'云','w':'温','':'温'},
}

# 辅音 + /juː/ 的合并读法（new / beautiful / computer / cute ...）
YU = {'N':'纽','D':'丢','L':'柳','M':'缪','K':'丘','G':'纠','HH':'休','T':'秋','S':'休','Z':'休',
      'B':'比优','P':'普优','F':'菲优','V':'维优','TH':'休','SH':'休','CH':'秋','JH':'纠','R':'柳'}
# /kw/ 的合并读法（quality / question / equal ...）
KW = {'a':'夸','ai':'快','ei':'奎','i':'奎','e':'阔','ao':'夸','an':'宽','ang':'匡',
      'in':'昆','en':'困','u':'酷','ou':'阔','o':'阔','eng':'困','ing':'昆','ong':'空','un':'昆'}

def pin(initial, final):
    tbl = PY.get(final)
    if not tbl: return '?'
    return tbl.get(initial) or tbl.get('') or '?'

OVERRIDE = {
 'the':'泽','a':'呃','of':'奥夫','to':'图','and':'安德','in':'因','is':'伊兹','it':'伊特',
 'you':'优','that':'拽特','he':'希','was':'沃兹','for':'佛','on':'昂','are':'阿','as':'艾兹',
 'with':'维兹','his':'黑兹','they':'贼','i':'爱','at':'艾特','be':'比','this':'迪斯',
 'have':'哈夫','from':'弗拉姆','or':'奥','one':'万','had':'哈德','by':'拜','but':'巴特',
 'not':'纳特','what':'沃特','all':'奥尔','were':'沃','we':'维','when':'温','your':'尤尔',
 'can':'坎','said':'赛德','there':'贼尔','an':'安','each':'伊奇','which':'维奇','she':'希',
 'do':'杜','how':'好','their':'贼尔','if':'伊夫','will':'维尔','up':'阿普','other':'阿泽',
 'about':'额包特','out':'奥特','many':'梅尼','then':'贼恩','them':'贼姆','these':'贼兹',
 'so':'搜','some':'萨姆','her':'赫','would':'伍德','make':'梅克','like':'莱克','him':'黑姆',
 'into':'因图','time':'太姆','has':'哈兹','look':'路克','two':'图','more':'莫尔','go':'购',
 'see':'西','no':'诺','way':'维','could':'库德','people':'皮坡','my':'麦','than':'赞',
 'first':'佛斯特','water':'沃特','been':'宾','who':'胡','now':'闹','find':'凡德','long':'朗',
 'down':'道恩','day':'戴','did':'迪德','get':'盖特','come':'卡姆','made':'梅德','may':'梅',
 'world':'沃尔德','hello':'喝喽','work':'沃克','new':'纽','use':'尤兹','because':'比考兹',
 'very':'费瑞','over':'欧沃','think':'辛克','also':'奥搜','after':'阿夫特','back':'拜克',
 'good':'古德','well':'威尔','year':'伊尔','through':'思路','before':'比佛','little':'里透',
 'want':'旺特','give':'吉夫','most':'莫斯特','us':'阿斯','life':'莱夫','only':'欧恩利',
 'know':'诺','take':'泰克','just':'贾斯特','our':'奥尔','any':'安尼','learn':'勒恩',
 'thing':'辛','where':'外尔','much':'马奇','never':'耐沃','same':'赛姆','right':'瑞特',
 'car':'卡尔','here':'希尔','both':'伯斯','why':'外','system':'西斯特姆','data':'戴特',
 'model':'马斗','human':'休门','safety':'赛夫提','sensor':'森瑟','computer':'康普优特','computers':'康普优特兹',
 'value':'瓦柳','values':'瓦柳兹','news':'纽兹','sensors':'森瑟兹','server':'瑟沃','servers':'瑟沃兹',
 'above':'额巴夫','under':'安德','again':'额根','against':'额根斯特','always':'奥维兹','around':'额绕恩德',
 'every':'艾夫瑞','without':'维兹奥特','something':'萨姆辛','nothing':'那辛','everything':'艾夫瑞辛',
 'today':'图戴','together':'图盖泽','course':'考尔斯','course':'考尔斯','early':'厄利','easy':'伊兹',
 'idea':'爱迪尔','ideas':'爱迪尔兹','area':'艾瑞额','real':'瑞尔','really':'瑞利','usually':'尤茹利',
}

def word_xieyin(word, phones):
    return ''.join(word_parts(word, phones))

def word_parts(word, phones):
    """逐音节谐音；人工覆盖的多音节词返回整体一段"""
    w = re.sub(r"[^a-z']", '', word.lower())
    if w in OVERRIDE:
        return [OVERRIDE[w]] if len(syllabify(phones)) == 1 else [OVERRIDE[w]]
    syls = syllabify(phones)
    # r 连读：ER 音节后面若跟一个零声母音节，把 /r/ 交给后一个音节做声母
    for i in range(len(syls) - 1):
        if syls[i][1] is not None and base(syls[i][1]) == 'ER' and not syls[i+1][0]:
            syls[i+1] = (['R'], syls[i+1][1], syls[i+1][2])
    out = []
    for onset, nuc, coda in syls:
        s = ''
        ini = ''
        head = None                       # 已合并处理的“声母+韵母”整字
        if onset:
            ob = [base(c) for c in onset]
            if len(ob) >= 2 and ob[-1] == 'Y' and nuc is not None and vkey(nuc) in ('UW','UH') and ob[-2] in YU:
                for c in ob[:-2]: s += C_SOLO_ONSET.get(c, '')
                head = YU[ob[-2]]
            elif len(ob) >= 2 and ob[-1] == 'W' and ob[-2] == 'K':
                for c in ob[:-2]: s += C_SOLO_ONSET.get(c, '')
                head = 'KW'
            else:
                for c in ob[:-1]: s += C_SOLO_ONSET.get(c, '')
                ini = C2I.get(ob[-1], '')
        if nuc is None:
            out.append(s); continue
        vk = vkey(nuc)
        fin = V2F[vk]
        rest = list(coda)
        if rest and vk in MERGE_N:
            b0 = base(rest[0])
            if b0 == 'N' and fin in FIN_N:
                fin = FIN_N[fin]; rest = rest[1:]
            elif b0 == 'NG' and fin in FIN_NG:
                fin = FIN_NG[fin]; rest = rest[1:]
        if head == 'KW':
            s += KW.get(fin, pin('k', fin))
        elif head:
            s += head
        elif ini == '' and vk == 'ER' and stress(nuc) == 0:
            s += '尔'                      # layer / paper 词尾的 -er
        else:
            s += pin(ini, fin)
        for c in rest:
            s += C_SOLO_CODA.get(base(c), '')
        out.append(s)
    return out

# ---------------------------------------------------------------- 对外接口
# CMU 词典里没有、或首选读音不合适的词，人工给 ARPABET
MANUAL = {
 'neural':      ['N','Y','UH1','R','AH0','L'],
 'neuron':      ['N','Y','UH1','R','AA2','N'],
 'neurons':     ['N','Y','UH1','R','AA2','N','Z'],
 'linux':       ['L','IH1','N','AH0','K','S'],
 'kernel':      ['K','ER1','N','AH0','L'],
 'app':         ['AE1','P'],
 'apps':        ['AE1','P','S'],
 'dataset':     ['D','EY1','T','AH0','S','EH2','T'],
 'datasets':    ['D','EY1','T','AH0','S','EH2','T','S'],
 'lidar':       ['L','AY1','D','AA2','R'],
 'gpu':         ['JH','IY1','P','IY1','Y','UW1'],
 'gpus':        ['JH','IY1','P','IY1','Y','UW1','Z'],
 'cpu':         ['S','IY1','P','IY1','Y','UW1'],
 'ssh':         ['EH1','S','EH1','S','EY1','CH'],
 'sudo':        ['S','UW1','D','OW0'],
 'chatbot':     ['CH','AE1','T','B','AA2','T'],
 'chatbots':    ['CH','AE1','T','B','AA2','T','S'],
 'uptime':      ['AH1','P','T','AY2','M'],
 'reboot':      ['R','IY0','B','UW1','T'],
 'reboots':     ['R','IY0','B','UW1','T','S'],
 'rebooting':   ['R','IY0','B','UW1','T','IH0','NG'],
 'transformer': ['T','R','AE0','N','S','F','AO1','R','M','ER0'],
 'transformers':['T','R','AE0','N','S','F','AO1','R','M','ER0','Z'],
 'chatgpt':     ['CH','AE1','T','JH','IY1','P','IY1','T','IY1'],
 'tokenizer':   ['T','OW1','K','AH0','N','AY2','Z','ER0'],
 'firewall':    ['F','AY1','ER0','W','AO2','L'],
 'firewalls':   ['F','AY1','ER0','W','AO2','L','Z'],
 'cron':        ['K','R','AA1','N'],
 'crontab':     ['K','R','AA1','N','T','AE2','B'],
 'sensor':      ['S','EH1','N','S','ER0'],
 'sensors':     ['S','EH1','N','S','ER0','Z'],
 'radar':       ['R','EY1','D','AA2','R'],
 'radars':      ['R','EY1','D','AA2','R','Z'],
 'autopilot':   ['AO1','T','OW0','P','AY2','L','AH0','T'],
 'nvidia':      ['EH0','N','V','IH1','D','IY0','AH0'],
 'ubuntu':      ['UW0','B','UW1','N','T','UW0'],
 'gigabytes':   ['G','IH1','G','AH0','B','AY2','T','S'],
 'terabytes':   ['T','EH1','R','AH0','B','AY2','T','S'],
 'megabytes':   ['M','EH1','G','AH0','B','AY2','T','S'],
 'server':      ['S','ER1','V','ER0'],
 'servers':     ['S','ER1','V','ER0','Z'],
 'backup':      ['B','AE1','K','AH2','P'],
 'backups':     ['B','AE1','K','AH2','P','S'],
 'overfitting': ['OW1','V','ER0','F','IH2','T','IH0','NG'],
 'gradient':    ['G','R','EY1','D','IY0','AH0','N','T'],
 'gradients':   ['G','R','EY1','D','IY0','AH0','N','T','S'],
 'perception':  ['P','ER0','S','EH1','P','SH','AH0','N'],
 'localization':['L','OW2','K','AH0','L','AH0','Z','EY1','SH','AH0','N'],
 'redundancy':  ['R','IY0','D','AH1','N','D','AH0','N','S','IY0'],
 'ok':          ['OW2','K','EY1'],
 'backpropagation':['B','AE2','K','P','R','AA2','P','AH0','G','EY1','SH','AH0','N'],
 'df':          ['D','IY1','EH1','F'],
 'runtime':     ['R','AH1','N','T','AY2','M'],
}

def _plural(p):
    b = base(p[-1])
    if b in {'S','Z','SH','ZH','CH','JH'}: return p + ['IH0','Z']
    if b in {'P','T','K','F','TH'}:        return p + ['S']
    return p + ['Z']

def lookup(word):
    w = re.sub(r"[^a-zA-Z']", '', word).lower()
    if not w: return None
    if w in MANUAL: return list(MANUAL[w])
    if w in CMU:    return list(CMU[w][0])
    for suf, add in (("n't", ['AH0','N','T']), ("'ll", ['AH0','L']), ("'re", ['ER0']),
                     ("'ve", ['V']), ("'d", ['D']), ("'m", ['M'])):
        if w.endswith(suf) and w[:-len(suf)] in CMU:
            return list(CMU[w[:-len(suf)]][0]) + add
    if w.endswith("'s") and w[:-2] in CMU:
        return _plural(list(CMU[w[:-2]][0]))
    if w.endswith("s") and w[:-1] in CMU:
        return _plural(list(CMU[w[:-1]][0]))
    return None

TOKEN = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?|[^\sA-Za-z]+|\s+")

def annotate(sentence):
    toks, missing = [], []
    for m in TOKEN.finditer(sentence):
        s = m.group(0)
        if re.match(r"^[A-Za-z]", s):
            ph = lookup(s)
            if ph is None:
                missing.append(s.lower())
                toks.append({'t': s, 'w': 1, 'p': '', 'c': ''})
            else:
                toks.append({'t': s, 'w': 1, 'p': to_ipa(ph), 'c': word_xieyin(s, ph)})
        else:
            # 空白和标点都原样保留，这样英文行和谐音行的间距才正确
            toks.append({'t': s, 'w': 0})
    return toks, missing

def sent_xieyin(toks):
    return ''.join(t['c'] if t['w'] else t['t'] for t in toks)

if __name__ == '__main__':
    tests = ["Hello world.",
             "The neural network learns from data.",
             "A self-driving car uses sensors to see the road.",
             "Check the system logs when the server is slow.",
             "Four score and seven years ago our fathers brought forth on this continent a new nation.",
             "Two roads diverged in a yellow wood.",
             "Ask not what your country can do for you."]
    for s in tests:
        toks, miss = annotate(s)
        print(s)
        print('   谐音:', sent_xieyin(toks))
        print('   音标:', ' '.join('/%s/' % t['p'] for t in toks if t['w'] and t['p']))
        if miss: print('   MISSING:', miss)
        print()

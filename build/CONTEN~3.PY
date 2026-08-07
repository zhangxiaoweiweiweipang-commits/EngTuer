# -*- coding: utf-8 -*-
"""拼读规则闯关（7 关）+ 单词拆音标题库"""

LEVELS = [
{
 "id":"L1","title":"第 1 关 · 闭音节短元音","goal":"看到「元音+辅音结尾」，元音读短音。这是英语里最常见的情况。",
 "rules":[
  {"p":"a","s":"/æ/","ex":["cat","map","bad","hand","black"],"note":"下巴要掉下来，比中文的“唉”开得多。"},
  {"p":"e","s":"/ɛ/","ex":["bed","pen","ten","get","help"],"note":"嘴半开就够，别开太大。"},
  {"p":"i","s":"/ɪ/","ex":["sit","big","ship","wind","list"],"note":"极短，嘴完全放松。"},
  {"p":"o","s":"/ɑ/","ex":["hot","box","stop","lock","not"],"note":"美音读“啊”，英音读“奥”。"},
  {"p":"u","s":"/ʌ/","ex":["cup","bus","run","sun","much"],"note":"短促发闷，像被掐断的“啊”。"},
 ],
 "quiz":[
  {"q":"map 里的 a 读什么？","opts":["/æ/ 哎","/eɪ/ 诶伊","/ɑ/ 啊","/ə/ 呃"],"a":0},
  {"q":"下面哪个词的元音和 bed 一样？","opts":["send","bead","bee","bird"],"a":0},
  {"q":"ship 里的 i 读什么？","opts":["/ɪ/ 短衣","/i/ 长衣","/aɪ/ 啊伊","/ɝ/ 儿"],"a":0},
  {"q":"cup 的元音是？","opts":["/ʌ/ 短啊","/u/ 乌","/ʊ/ 短乌","/ɔ/ 奥"],"a":0},
  {"q":"哪个词不符合“闭音节读短音”？","opts":["hope","hop","hot","hand"],"a":0},
 ]},
{
 "id":"L2","title":"第 2 关 · 魔法 e（开音节长元音）","goal":"词尾有个不发音的 e，它会让前面的元音「读自己的字母名」。",
 "rules":[
  {"p":"a_e","s":"/eɪ/","ex":["name","cake","late","make","game"],"note":"a 读它的字母名 A。"},
  {"p":"i_e","s":"/aɪ/","ex":["time","like","nine","ride","white"],"note":"i 读它的字母名 I。"},
  {"p":"o_e","s":"/oʊ/","ex":["home","note","hope","those","stone"],"note":"o 读它的字母名 O。"},
  {"p":"u_e","s":"/u/ 或 /ju/","ex":["use","cute","tube","huge","rule"],"note":"多数读“优”，r/l 后面读“乌”。"},
  {"p":"e_e","s":"/i/","ex":["these","complete","theme"],"note":"这一组比较少。"},
 ],
 "quiz":[
  {"q":"hop 加上 e 变成 hope，元音怎么变？","opts":["/ɑ/ 变 /oʊ/","不变","/ɑ/ 变 /ɔ/","/oʊ/ 变 /ɑ/"],"a":0},
  {"q":"kite 里的 i 读什么？","opts":["/aɪ/ 啊伊","/ɪ/ 短衣","/i/ 长衣","/ɝ/ 儿"],"a":0},
  {"q":"哪个词的 e 不发音？","opts":["make","he","she","be"],"a":0},
  {"q":"tub 和 tube 的区别在？","opts":["元音从 /ʌ/ 变成 /u/","没有区别","辅音变了","重音变了"],"a":0},
  {"q":"下面哪个是「魔法 e」的例外？","opts":["have","gave","save","wave"],"a":0},
 ]},
{
 "id":"L3","title":"第 3 关 · 元音字母组合","goal":"两个元音字母在一起时，常常「第一个说话，第二个不出声」，但也有一批需要单独记。",
 "rules":[
  {"p":"ai / ay","s":"/eɪ/","ex":["rain","wait","day","play","train"],"note":"ay 一般在词尾。"},
  {"p":"ee / ea","s":"/i/","ex":["see","tree","meat","read","beach"],"note":"ea 也可能读 /ɛ/：bread、head、ready。"},
  {"p":"oa / ow","s":"/oʊ/","ex":["boat","road","snow","know","slow"],"note":"ow 也可能读 /aʊ/，见下一条。"},
  {"p":"oo","s":"/u/ 或 /ʊ/","ex":["food","moon","school","book","good"],"note":"没有规律，只能一个一个记：食物类多长音，书本类多短音。"},
  {"p":"ou / ow","s":"/aʊ/","ex":["out","house","about","now","down"],"note":"ou 也可能读 /ʌ/：country、young、touch。"},
  {"p":"oi / oy","s":"/ɔɪ/","ex":["coin","voice","boy","join","enjoy"],"note":"oy 一般在词尾。"},
  {"p":"au / aw","s":"/ɔ/","ex":["because","cause","saw","law","draw"],"note":"美音这个音正在向 /ɑ/ 靠拢。"},
 ],
 "quiz":[
  {"q":"road 和 loud 里的元音一样吗？","opts":["不一样：/oʊ/ 和 /aʊ/","一样","都读 /ɔ/","都读 /u/"],"a":0},
  {"q":"book 和 food 里的 oo 一样吗？","opts":["不一样：/ʊ/ 和 /u/","一样","都是短音","都是长音"],"a":0},
  {"q":"bread 里的 ea 读什么？","opts":["/ɛ/","/i/","/eɪ/","/ɪ/"],"a":0},
  {"q":"enjoy 里的 oy 读什么？","opts":["/ɔɪ/ 奥伊","/oʊ/ 欧","/aɪ/ 啊伊","/ɔ/ 奥"],"a":0},
  {"q":"country 里的 ou 读什么？","opts":["/ʌ/ 短啊","/aʊ/ 啊乌","/u/ 乌","/oʊ/ 欧"],"a":0},
 ]},
{
 "id":"L4","title":"第 4 关 · r 控制音节","goal":"元音后面跟着 r，元音就被 r「吃掉」了，变成卷舌音。这是美音最明显的特征。",
 "rules":[
  {"p":"ar","s":"/ɑr/","ex":["car","star","park","hard","large"],"note":"啊 + 卷舌。"},
  {"p":"or","s":"/ɔr/","ex":["for","born","short","more","story"],"note":"奥 + 卷舌。"},
  {"p":"er / ir / ur","s":"/ɝ/","ex":["her","bird","turn","first","nurse"],"note":"这三个拼法读同一个音，非常好记。"},
  {"p":"词尾 -er / -or / -ar","s":"/ɚ/","ex":["teacher","doctor","dollar","water","never"],"note":"轻读的卷舌，几乎所有「做…的人/物」都这样结尾。"},
  {"p":"w + or","s":"/ɝ/（例外）","ex":["work","word","world","worse"],"note":"w 后面的 or 不读 /ɔr/，要特别记。"},
 ],
 "quiz":[
  {"q":"bird、her、turn 的元音一样吗？","opts":["一样，都是 /ɝ/","都不一样","两个一样","都是 /ɔr/"],"a":0},
  {"q":"work 里的 or 读什么？","opts":["/ɝ/ 儿","/ɔr/ 奥尔","/ɑr/ 啊尔","/oʊ/ 欧"],"a":0},
  {"q":"teacher 词尾的 -er 读什么？","opts":["/ɚ/ 轻卷舌","/ɝ/ 重卷舌","/ɛ/ 唉","/ə/ 呃"],"a":0},
  {"q":"美音里 car 该怎么读？","opts":["卡尔（卷舌）","卡（不卷舌）","开尔","库尔"],"a":0},
  {"q":"哪个词的元音和 park 不同？","opts":["short","hard","large","star"],"a":0},
 ]},
{
 "id":"L5","title":"第 5 关 · 辅音字母组合","goal":"两个辅音字母合起来变成一个全新的音，不是两个音相加。",
 "rules":[
  {"p":"th","s":"/θ/ 或 /ð/","ex":["think","three","this","mother","the"],"note":"实词多读 /θ/，虚词（the/this/that/they）多读 /ð/。都要咬舌。"},
  {"p":"sh","s":"/ʃ/","ex":["she","fish","should","wash","English"],"note":"嘴要撅。"},
  {"p":"ch","s":"/tʃ/","ex":["chair","much","teach","China","check"],"note":"例外：school/christmas 读 /k/，machine 读 /ʃ/。"},
  {"p":"ph","s":"/f/","ex":["phone","photo","graph","physics"],"note":"来自希腊语的词。"},
  {"p":"wh","s":"/w/","ex":["what","when","where","white","why"],"note":"例外：who、whose、whole 读 /h/。"},
  {"p":"ck","s":"/k/","ex":["back","duck","black","check","quick"],"note":"永远只发一个 /k/。"},
  {"p":"ng","s":"/ŋ/","ex":["sing","long","thing","strong","during"],"note":"结尾不要多加一个“格”。"},
  {"p":"qu","s":"/kw/","ex":["quick","question","quality","quiet","equal"],"note":"q 后面永远跟 u。"},
 ],
 "quiz":[
  {"q":"school 里的 ch 读什么？","opts":["/k/ 克","/tʃ/ 奇","/ʃ/ 什","/dʒ/ 吉"],"a":0},
  {"q":"who 里的 wh 读什么？","opts":["/h/ 喝","/w/ 乌","/hw/","不发音"],"a":0},
  {"q":"question 里的 qu 读什么？","opts":["/kw/ 阔","/k/ 克","/kju/ 丘","/w/ 乌"],"a":0},
  {"q":"this 和 think 里的 th 一样吗？","opts":["不一样：/ð/ 和 /θ/","一样","都读 /s/","都读 /d/"],"a":0},
  {"q":"sing 结尾应该？","opts":["鼻腔收住，不加“格”","加一个“格”音","读成 /n/","读成 /m/"],"a":0},
 ]},
{
 "id":"L6","title":"第 6 关 · 词尾后缀","goal":"认识几个高频词尾，长单词一下子就不吓人了。",
 "rules":[
  {"p":"-tion","s":"/ʃən/ 神","ex":["nation","action","attention","information","education"],"note":"重音永远落在 -tion 前面那个音节。"},
  {"p":"-sion","s":"/ʒən/ 或 /ʃən/","ex":["vision","decision","mission","discussion"],"note":"元音后读 /ʒən/，辅音后读 /ʃən/。"},
  {"p":"-ture","s":"/tʃɚ/ 彻","ex":["nature","future","picture","culture","structure"],"note":"不是“图尔”。"},
  {"p":"-ous","s":"/əs/ 额斯","ex":["famous","dangerous","serious","nervous"],"note":"读得很轻。"},
  {"p":"-le","s":"/əl/ 欧","ex":["table","people","simple","little","possible"],"note":"e 不发音，l 自己成音节。"},
  {"p":"词尾 -y","s":"/i/ 衣","ex":["happy","city","safety","quality","memory"],"note":"两个音节以上时，词尾 y 读 /i/。"},
  {"p":"-ed 三种读法","s":"/t/ /d/ /ɪd/","ex":["worked","played","wanted","asked","needed"],"note":"清辅音后 /t/，浊音后 /d/，t/d 后才读 /ɪd/。"},
  {"p":"-s 三种读法","s":"/s/ /z/ /ɪz/","ex":["books","dogs","buses","cats","pages"],"note":"和 -ed 同理。"},
 ],
 "quiz":[
  {"q":"information 的重音在哪个音节？","opts":["-ma-","in-","-for-","-tion"],"a":0},
  {"q":"picture 词尾读什么？","opts":["/tʃɚ/ 彻","/tʊr/ 图尔","/tɚ/ 特","/ʃɚ/ 舍"],"a":0},
  {"q":"worked 的 -ed 读什么？","opts":["/t/","/d/","/ɪd/","不发音"],"a":0},
  {"q":"wanted 的 -ed 读什么？","opts":["/ɪd/","/t/","/d/","不发音"],"a":0},
  {"q":"dogs 的 -s 读什么？","opts":["/z/ 兹","/s/ 斯","/ɪz/ 伊兹","不发音"],"a":0},
 ]},
{
 "id":"L7","title":"第 7 关 · 不发音字母","goal":"英语里有一批「哑巴字母」，认出来就不会读错。",
 "rules":[
  {"p":"kn-","s":"k 不发音","ex":["know","knee","knife","knock"],"note":"只读 /n/。"},
  {"p":"wr-","s":"w 不发音","ex":["write","wrong","wrap","wrist"],"note":"只读 /r/。"},
  {"p":"-mb","s":"b 不发音","ex":["climb","comb","lamb","thumb"],"note":"只读 /m/。"},
  {"p":"-gh","s":"多数不发音","ex":["light","night","high","though","eight"],"note":"但 laugh、enough、cough 里读 /f/。"},
  {"p":"gn","s":"g 不发音","ex":["sign","design","foreign","campaign"],"note":"但 signal、designer 里 g 又发音了。"},
  {"p":"-st-","s":"t 不发音","ex":["listen","castle","fasten","whistle"],"note":"s 和 le/en 之间的 t。"},
  {"p":"其他","s":"零散记","ex":["debt","doubt","island","half","talk","walk"],"note":"debt/doubt 的 b、island 的 s、half/talk/walk 的 l 都不发音。"},
 ],
 "quiz":[
  {"q":"know 怎么读？","opts":["/noʊ/ 诺","/knoʊ/ 克诺","/naʊ/ 闹","/koʊ/ 扣"],"a":0},
  {"q":"enough 里的 gh 读什么？","opts":["/f/","不发音","/ɡ/","/k/"],"a":0},
  {"q":"listen 里的 t？","opts":["不发音","读 /t/","读 /d/","读 /θ/"],"a":0},
  {"q":"climb 结尾读什么？","opts":["/m/","/mb/","/b/","不发音"],"a":0},
  {"q":"walk 里哪个字母不发音？","opts":["l","w","a","k"],"a":0},
 ]},
]

# 单词拆音标练习题库（按难度分组）
WORDBANK = [
 {"id":"W1","title":"第 1 组 · 最高频 60 词","desc":"这些词占了日常英语一半以上的篇幅，读准它们收益最大。",
  "words":"""the be to of and a in that have I it for not on with he as you do at this but his by from
  they we say her she or an will my one all would there their what so up out if about who get which go me
  when make can like time no just him know take people into year""".split()},
 {"id":"W2","title":"第 2 组 · 常用动词与形容词","desc":"开口说话最需要的一批词。",
  "words":"""think want give use find tell ask work seem feel try leave call need become mean keep let begin
  help talk turn start show hear play run move live believe bring happen write sit stand lose pay meet include
  continue set learn change lead understand watch follow stop create speak read spend grow open walk win teach
  offer remember consider appear buy serve send build stay fall reach kill remain""".split()},
 {"id":"W3","title":"第 3 组 · 音标陷阱词","desc":"拼写和读音差距最大的一批词，专治「看着会读，其实读错」。",
  "words":"""answer bury busy comfortable determine develop enough example favorite February foreign heart
  height iron island knowledge laugh listen minute mountain often once purpose recipe salmon scissors sew
  station suite subtle sword sugar though thorough through tongue vegetable Wednesday women worry yacht
  choir colonel debt doubt guitar""".split()},
 {"id":"W4","title":"第 4 组 · 技术词汇","desc":"AI、Linux、自动驾驶三个方向里出现频率最高的词。",
  "words":"""algorithm attention automatic autonomous backup bandwidth camera cluster command compute
  configure container data database dependency deploy device directory driver encrypt engine environment
  execute feature framework function gradient hardware image inference install interface kernel language
  latency layer library machine memory model module monitor network neural node output package parameter
  password pattern performance permission pipeline platform predict process protocol quality queue radar
  recognition redundancy register release remote request resource response route runtime safety scale schedule
  script security sensor server service session signal software source storage stream structure system
  threshold token traffic training transfer trigger update upgrade vehicle version virtual volume""".split()},
]

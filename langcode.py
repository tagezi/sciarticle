#     This code is a part of program Science Jpurnal
#     Copyright (C) 2021  Valerii Goncharuk (aka tagezi)
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

def get_lang_by_code(code):
    if code == "eng" or code == "en":
        return "английский"
    if code == "ru" or code == "rus" or code == "рус" or code == "570":
        return "русский"
    if code == "zu" or code == "zul" or code == "зул" or code == "195":
        return "зулу"
    if code == "zh" or code == "chi" or code == "zho" or code == "кит" or code == "315":
        return "китайский"
    if code == "za" or code == "zha" or code == "чжу" or code == "791":
        return "чжуанский"
    if code == "yo" or code == "yor" or code == "йор" or code == "245":
        return "йоруба"
    if code == "yi" or code == "yid" or code == "иди" or code == "202":
        return "идиш"
    if code == "xh" or code == "xho" or code == "коа" or code == "340":
        return "коса"
    if code == "wo" or code == "wol" or code == "воф" or code == "138":
        return "волоф"
    if code == "vo" or code == "vol" or code == "вол" or code == "137":
        return "волапюк"
    if code == "vi" or code == "vie" or code == "вье" or code == "140":
        return "вьетнамский"
    if code == "ve" or code == "ven" or code == "вед" or code == "134":
        return "венда"
    if code == "uz" or code == "uzb" or code == "узб" or code == "710":
        return "узбекский"
    if code == "ur" or code == "urd" or code == "урд" or code == "730":
        return "урду"
    if code == "uk" or code == "ukr" or code == "укр" or code == "720":
        return "украинский"
    if code == "ug" or code == "uig" or code == "уйг" or code == "715":
        return "уйгурский"
    if code == "ty" or code == "tah" or code == "тая" or code == "647":
        return "таитянский"
    if code == "tt" or code == "tat" or code == "тви" or code == "670":
        return "тви"
    if code == "tat" or code == "тар" or code == "660":
        return "татарский"
    if code == "ts" or code == "tso" or code == "тсо" or code == "689":
        return "тсонга"
    if code == "tr" or code == "tur" or code == "тур" or code == "693":
        return "турецкий"
    if code == "to" or code == "ton" or code == "тон" or code == "686":
        return "тонганский"
    if code == "to" or code == "ton" or code == "тон" or code == "686":
        return "тсвана"
    if code == "tn" or code == "tsn" or code == "тсн" or code == "688":
        return "тонганский"
    if code == "tl" or code == "tgl" or code == "таг" or code == "636":
        return "тагальский"
    if code == "tk" or code == "tuk" or code == "тук" or code == "695":
        return "туркменский"
    if code == "tk" or code == "tir" or code == "тир" or code == "683":
        return "тигринья"
    if code == "th" or code == "tha" or code == "таи" or code == "645":
        return "тайский"
    if code == "tg" or code == "tgk" or code == "тад" or code == "640":
        return "таджикский"
    if code == "te" or code == "tel" or code == "тел" or code == "675":
        return "телугу"
    if code == "sw" or code == "swa" or code == "суа" or code == "631":
        return "суахили"
    if code == "sv" or code == "sve" or code == "swe" or code == "шве" or code == "805":
        return "шведский"
    if code == "su" or code == "sun" or code == "сун" or code == "633":
        return "сунданский"
    if code == "st" or code == "sot" or code == "сот" or code == "618":
        return "южный сото"
    if code == "ss" or code == "ssw" or code == "сва" or code == "584":
        return "свази"
    if code == "sr" or code == "scc" or code == "srp":
        return "сербский"
    if code == "sq" or code == "alb" or code == "sqi" or code == "алб" or code == "30":
        return "албанский"
    if code == "so" or code == "som" or code == "сом" or code == "615":
        return "сомали"
    if code == "sn" or code == "sna" or code == "шон" or code == "807":
        return "шона"
    if code == "sm" or code == "smo" or code == "смо" or code == "578":
        return "самоанский"
    if code == "sl" or code == "slv" or code == "слв" or code == "610":
        return "словенский"
    if code == "sk" or code == "slk" or code == "slo" or code == "сло" or code == "605":
        return "словацкий"
    if code == "si" or code == "sin" or code == "син" or code == "599":
        return "сингальский"
    if code == "sg" or code == "sag" or code == "саг" or code == "579":
        return "санго"
    if code == "sd" or code == "snd" or code == "снд" or code == "600":
        return "синдхи"
    if code == "sc" or code == "srd" or code == "срд" or code == "583":
        return "сардинский"
    if code == "sa" or code == "san" or code == "сан" or code == "581":
        return "санскрит"
    if code == "rw" or code == "kin" or code == "кин" or code == "304":
        return "руанда"
    if code == "sd" or code == "snd" or code == "снд" or code == "600":
        return "синдхи"
    if code == "sd" or code == "snd" or code == "снд" or code == "600":
        return "синдхи"
    if code == "" or code == "английский":
        return "английский"



# румынский    ro    ron / rum    ron    ron / rum    рум    565
# рунди    rn    run    run    run    рун    567    ретороманский    rm    roh    roh    —    рет    560    кечуа
# qu    que    que    que    кеч    300    португальский    pt    por    por    роr    пор    545    пушту    ps
# pus    pus    pus    пуш    550    польский    pl    pol    pol    pol    пол    540    пали    pi    pli    pli
# pli    пли    527    пенджабский    pa    pan    pan    pan    пан    530    осетинский    os    oss    oss    oss
# ост    524    ория or ori    ori    ori    ори    520    оромо    om    orm    orm    orm    орм    522    оджибве
# oj    oji    oji    oji    одж    515    окситанский    oc    oci    oci    oci    окс    517    ньянджа    ny
# nya    nya    nya    нян    510    навахо    nv    nav    nav    nav    нав    470    ндебеле    южный    nr    nbl
# nbl    nbl    нбл    474    норвежский    no    nor    nor    nor    нор    506    нюнорск(новонорвежский)    nn
# nno    nno    nno    нно    513    нидерландский(голландский)    nl    dut / nld    nld    dut / ndl    нид    495
# ндунга    ng    ndo    ndo    ndo    нду    475    непальский    ne    nep    nep    nep    неп    485    ндебеле
# северный    nd    nde    nde    nde    нде    473    науру    na    nau    nau    nau    нау    472    бирманский
# my    bur / mya    mya    bur / mya    бир    105    мальтийский    mt    mlt    mlt    mlt    млт    430
# малайский    ms    may / msa    msa    may / msa    маз    420    маратхи    mr    mar    mar    mar    мар    440
# монгольский    mn    mon    mon    mon    мон    463    малаялам    ml    mal    mal    mal    мал    425
# македонский    mk    mac / mkd    mkd    mac / mke    маа    415    маори    mi    mao / mri    mri    mao / mri
# мао    437    маршалльский    mh    mah    mah    mah    маш    446    малагасийский    mg    mlg    mlg    mlg
# млг    418    мерянский    me    mer    mer    —    мер    —    молдавский    md    md    md    mol    мол    460
# латышский    lv    lav    lav    lav    лаш    385    луба - катанга    lu    lub    lub    lub    луб    404
# литовский    lt    lit    lit    lit    лит    400    лаосский    lo    lao    lao    lao    лао    375    лингала
# ln    lin    lin    lin    лин    395    ганда    lg    lug    lug    lug    ган    148    люксембургский    lb
# ltz    ltz    ltz    люк    409    латинский    la    lat    lat    lat    лат    380    киргизский    ky    kir
# kir    kyr    кир / кыр    305    корнский    kw    cor    cor    cor    кор    332    коми    kv    kom    kom
# kom    кои    320    курдский    ku    kur    kur    kur    кур    350    кашмири    ks    kas    kas    kas    каш
# 294    канури    kr    kau    kau    kau    кау    267    корейский    ko    kor    kor    kor    коо    330
# каннада    kn    kan    kan    kan    кан    265    кхмерский    km    khm    khm    khm    кхм    360
# гренландский    kl    kal    kal    kal    эсм    843    казахский    kk    kaz    kaz    kaz    каз    255
# киньяма    kj    kua    kua    kua    кия    303    кикуйю    ki    kik    kik    kik    кик    302    конго    kg
# kon    kon    kon    кон    326    грузинский    ka    geo / kat    kat    geo / kat    гру    158    яванский
# jv    jav / jaw    jav    jav / jaw    ява    860    японский    ja    jpn    jpn    jpn    япо    870    инуктитут
# iu    iku    iku    iku    инк    217    итальянский    it    ita    ita    ita    ита    235    исландский is ice
# / isl    isl    ice / isl    исл    225    инупиак    ik    ipk    ipk    ipk    инп    218    игбо    ig    ibo
# ibo    ibo    ибо    199    интерлингве    ie    ile    ile    ile    ине    216    индонезийский    id    ind
# ind    ind    инд    210    интерлингва    ia    ina    ina    ina    ина    215    гереро    hz    her    her
# her    гер    149    армянский    hy    arm / hye    hye / axm / xcl    arm / hye    арм    55    венгерский    hu
# hun    hun    hun    вен    133    хорватский    hr    hrv / scr    hrv    —    —    —    хиримоту    ho    hmo
# hmo    hmo    хмо    772    хинди    hi    hin    hin    hin    хин    770    иврит    he    heb    heb    heb
# ивр    198    хауса    ha    hau    hau    hau    хау    761    мэнский(мэнкский)    gv    glv    glv    max    мэн
# 469    гуджарати    gu    guj    guj    guj    гуд    165    гуарани    gn    grn    grn    grn    гуа    160
# галисийский    gl    glg    glg    glg    гал    147    гэльский    gd    gla    gla    gae / gdh    гэл    170
# ирландский    ga    gle    gle    gai / iri    ирл    220    фризский    fy    fry    fry    fry    фри    750
# французский    fr    fra / fre    fra    fra / fre    фра    745    фарерский    fo    fao    fao    fao    фар
# 735    филиппинский    fl    fil    fil    tgl    таг    636    фиджи    fj    fij    fij    fij    фид    737
# финский(suomi)    fi    fin    fin    fin    фин    740    фулах    ff    ful    ful    ful    фул    752
# персидский    fa    fas / per    fas    fas / per    пер    535    баскский    eu    baq / eus    eus    baq / eus
# бак    85    эстонский    et    est    est    est    эст    850    испанский    es    esl / spa    spa    esl / spa
# исп    230    эсперанто    eo    epo    epo    epo    эсп    845    английский    en    eng    eng    eng    анг
# 45    греческий(новогреческий)    el    ell / gre    ell    ell / gre    гре    157    эве    ee    ewe    ewe
# ewe    эве    820    дзонг - кэ    dz    dzo    dzo    dzo    дзо    183    дивехи(мальдивский)    dv    div    div
# div    див    180    немецкий    de    deu / ger    deu    deu / ger    нем    481    датский    da    dan    dan
# dan    дат    178    валлийский    cy    cym / wel    cym    cym / wel    вал    130    чувашский    cv    chv
# chv    chv    чув    795    церковнославянский(старославянский)    cu    chu    chu    chu    цер    777    чешский
# cs    ces / cze    ces    ces / cze    чеш    790    корсиканский    co    cos    cos    cos    кос    334
# чаморро    ch    cha    cha    cha    чам    782    чеченский    ce    che    che    che    чеч    785
# каталанский    ca    cat    cat    cat    кат    290    боснийский    bs    bos    bos    —    бос    —
# бретонский    br    bre    bre    bre    бре    120    тибетский    bo    bod / tib    bod    bod / tib    тиб
# 680    бенгальский    bn    ben    ben    ben    бен    100    бамбара    bm    bam    bam    bam    бам    80
# бислама    bi    bis    bis    bis    бис    107    болгарский    bg    bul    bul    bul    бол    115
# белорусский    be    bel    bel    bel    бел    90    башкирский    ba    bak    bak    bak    баш    86
# азербайджанский    az    aze    aze    aze    азе    25    аймара    ay    aym    aym    aym    айм    26
# аварский    av    ava    ava    ava    ава    14    ассамский as asm    asm    asm    аса    60    арабский    ar
# ara    ara    ara    ара    50    амхарский    am    amh    amh    amh    амх    40    акан    ak    aka    aka
# aka    ака    27    африкаанс    af    afr    afr    afr    афр    70    авестийский    ae    ave    ave    ave
# аве    16    абхазский    ab    abk    abk    abk    абх    10    афарский    aa    aar    aar    aar    афа    68
# абазинский    —    —    abq    aba    аба    5    авадхи    —    awa    awa    awa    авд    12    адангме    —
# ada    ada    ada    ада    18    адыгейский    —    ady    ady    ady    ады    20    айну    —    ain    ain    —
# —    —    аккадский    —    akk    akk    akk    акк    28    алеутский    —    ale    ale    ale    але    33
# алтайский    —    alt    alt    alt    алт    35    аравакский    —    arw    arw    arw    арв    51    арамейский
# —    arc    arc    —    арс    52    арапахо    —    arp    arp    arp    арп    53    арауканский    —    arn
# arn    arn    арн    54    ассирийский    —    —    aii    ass    асс    65    атапачские    —    —    ath    ath
# ата    67    африхили    —    afh    afh    afh    афх    73    ахвахский    —    akv    akv    akh    ахв    74
# ацтекский    —    —    nah    —    ацт    75    ачехский    —    ace    ace    ace    аче    76    ачоли    —
# ach    ach    ach    ачо    77    балийский    —    ban    ban    ban    бал    78    банда    —    bad    bad
# bad    бан    82    баса    —    bas    bas    bas    бас    84    беджа    —    bej    bej    bej    бед    87
# белуджский    —    bal    bal    bal    беу    95    бемба    —    bem    bem    bem    бем    97    бикольский
# —    bik / bcl    bik    bik    бик    103    бини    —    bin    bin    bin    бин    104    брауи    —    —
# brh    bra    бра    117    бугийский    —    bug    bug    bug    буг    123    бурятский    —    bua    bua
# bua    бур    125    бходжпури    —    bho    bho    bho    бхо    126    ваи    —    vai    vai    vai    ваи
# 127    варай    —    war    war    war    вар    131    вашо    —    was    was    was    ваш    132    вепсский
# —    —    vep    vep    веп    135    воламо    —    wal    wal    wal    воа    136    га    —    gaa    gaa
# gaa    гаа    142    гавайский    —    haw    haw    haw    гав    143    гагаузский    —    —    gag    gag    гаг
# 145    гайо    —    gay    gay    gay    гай    146    геэз    —    gez    gez    gez    гез    151    гилбертский
# —    gil    gil    gil    гил    152    гонди    —    gon    gon    gon    гон    153    готский    —    got    got
# got    гот    154    гребо    —    grb    grb    grb    грб    155    дакота    —    dak    dak    dak    дак
# 173    даргинский    —    dar    dar    dag    даг    175    дари    —    prs    prs    —    —    639 - 3
# делавэрский    —    del    del    del дел    179    динка    —    din    din    din    дин    181    диула(дьюла)
# —    dyu    dyu    dyu    диу    182    догри    —    doi    doi    doi    дои    184    древнегреческий    —
# grc    grc    grc    дрг    186    древнеегипетский    —    egy    egy    egy    дре    187    древнерусский    —
# —    orv    rua    дрр    188    древнесаксонский    —    —    osx    —    —    —    дуала    —    dua    dua
# dua    дуа    190    дунганский    —    —    dng    dun    дун    191    еврейско - арабский    —    jrb    jrb
# jrb    еар    192    еврейско - персидский    —    jpr    jpr    jpr    епе    193    зенагский    —    zen    zen
# zen    зен    194    зуньи    —    zun    zun    zun    зун    196    ибанский    —    iba    iba    iba    иба
# 197    илоко    —    ilo    ilo    ilo    ило    203    ингушский    —    inh    inh    ing    инг    205
# ительменский    —    —    itl    ite    ите    240    кабардино - черкесский    —    kbd    kbd    kad    каа
# 250    кабильский    —    kab    kab    kab    каб    251    кави    —    kaw    kaw    kaw    каг    252    каддо
# —    cad    cad    cad    кад    254    калмыцкий    —    xal    xal    kak    кал    260    камба    —    kam
# kam    kam    кам    263    караимский    —    —    kdr    kai    каи    270    каракалпакский    —    kaa    kaa
# kaa    кап    275    карачаево - балкарский    —    krc    krc    kah    као    280    карельский    —    krl
# krl    kae    кас    285    кариб    —    car    car    car    кар    288    качинский    —    kac    kac    kac
# кач    293    коми - пермяцкий    —    —    koi    pem    ком    325    конкани    —    kok    kok    kok    кок
# 327    коптский    —    cop    cop    cop    коп    328    корякский    —    —    kpy    koy    коя    335
# кпелле    —    kpe    kpe    kpe    кпе    341    крик    —    mus    mus    mus    крк    344    крымско -
# татарский    —    crh    crh    cri    кры    347    кумыкский    —    kum    kum    kum    кум    349    курух
# —    kru    kru    kru    куу    352    кусайе    —    kos    kos    kus    кус    353    кутенай    —    kut
# kut    kut    кут    354    кхаси    —    kha    kha    kha    кха    357    ладино    —    lad    lad    lad
# лад    363    лакский    —    —    lbe    lak    лак    370    ламба    —    lam    lam    lam    лам    373
# лахнда    —    lah    lah    lah    лах    387    лезгинский    —    lez    lez    lez    лез    390    лози    —
# loz    loz    loz    лоз    402    луисеньо    —    lui    lui    lui    луи    406    лунда    —    lun    lun
# lun    лун    407    луо    —    luo    luo    luo    луо    408    магахи    —    mag    mag    mag    маг    410
# мадурский    —    mad    mad    mad    мад    411    майтхили    —    mai    mai    mai    май    412
# макассарский    —    mak    mak    mak    мак    414    мандинго    —    man    man    man    маи    432
# манипури    —    mni    mni    mni    мни    433    мансийский(вогульский)    —    —    mns    vog    ман    435
# марвари    —    mwr    mwr    mwr    мвр    443    марийский(черемисский)    —    chm    chm    chm    мач    445
# масаи    —    mas    mas    mas    мас    447    менде    —    men    men    men    мен    451    микмак    —
# mic    mic    mic    мик    452    минангкабау    —    min    min    min    мин    453    мокшанский    —    mdf
# mdf    mok    мок    455    монго    —    lol    lol    lol    мог    462    мооре    —    mos    mos    mos    мос
# 466    мохаук    —    moh    moh    moh    мох    467    нанайский(гольдский)    —    —    gld    —    нан    471
# неварский    —    new    new    new    нев    478    неидентифицированный    —    und    und    und    унд    480
# ненецкий(юрако - самоедский)    —    —    yrk    yur    нен    482    нзима    —    nzi    nzi    nzi    нзи    487
# нивхский(гиляцкий)    —    —    niv    giy    нив    490    нидерландский    средневековый    —    dum    dum
# dum    нис    496    ниуэ    —    niu    niu    niu    ниу    498    ногайский    —    nog    nog    nog    ног
# 505    ньоро    —    nyo    nyo    nyo    ньо    508    ньямвези    —    nym    nym    nym    ням    509
# ньянколе    —    nyn    nyn    nyn    нья    512    оседжи    —    osa    osa    osa    осе    523    палау    —
# pau    pau    pau    пал    526    пампанга    —    pam    pam    pam    пам    528    пангасинан    —    pag
# pag    pag    паг    529    папьяменто    —    pap    pap    pap    пап    533    пехлевийский    —    pal    pal
# pal    пех    537    понапе    —    pon    pon    pon    пон    542    раджастхани    —    raj    raj    raj    рад
# 555    разных    семей    языки    —    mul    mul    mul    мул    556    раротонга    —    rar    rar    rar
# рар    557    рутульский    —    —    rut    —    рут    —    саамский    —    smi    smi    smi    саа    575
# самаритянский    арамейский    —    sam    sam    sam    сам    577    сандаве    —    sad    sad    sad    сад
# 580    сапотекский    —    zap    zap    zap    сап    582    себуано    —    ceb    ceb    ceb    себ    587
# селькупский    —    sel    sel    sel    сел    590    серер    —    srr    srr    srr    срр    596    сидама    —
# sid    sid    sid    сид    597    сиксика    —    bla    bla    bla    сик    598    сирийский    —    syr    syr
# syr    сир    602    согдийский    —    sog    sog    sog    сог    613    сото    северный    —    nso    nso
# nso    сос    617    среднеанглийский    —    enm    enm    enm    сра    619    средневерхненемецкий    —    gmh
# gmh    gmh    срн    620    среднеирландский    —    mga    mga    mga    сеи    621    среднефранцузский    —
# frm    frm    frm    срф    622    староанглийский    —    ang    ang    ang    ста    623    староверхненемецкий
# —    goh    goh    goh    свн    624    староирландский    —    sga    sga    sga    сти    625    старонорвежский
# —    non    non    non    стн    626    староперсидский    —    peo    peo    peo    стп    627
# старопровансальский    —    pro    pro    pro    спр    628    старотурецкий    —    ota    ota    ota    стт
# 629    старофранцузский    —    fro    fro    fro    стф    630    сукума    —    suk    suk    suk    сук    632
# сусу    —    sus    sus    sus    сус    634    табасаранский    —    —    tab    tab    таб    635    талышский
# —    —    tly    tal    тал    650    тамашек    —    tmh    tmh    tmh    тмш    653    темне    —    tem    tem
# tem    тем    677    терено    —    ter    ter    ter    тер    678    тиви    —    tiw    tiw    tiv    тив    681
# тигре    —    tig    tig    tig    тиг    682    тлингит    —    tli    tli    tli    тли    684    тонга(ньяса)
# —    tog    tog    tog    тог    685    трукский    —    —    chk    tru    тру    687    тувинский    —    tyv
# tyv    tyv    тув    690    тумбука    —    tum    tum    tum    тум    692    угаритский    —    uga    uga    uga
# уга    697    удмуртский(вотяцкий)    —    udm    udm    vot    удм    700    удэгейский    —    —    ude    ude
# удэ    705    ульчский    —    —    ulc    ulc    уль    725    умбунду    —    umb    umb    umb    умб    727
# фанг    —    fan    fan    fan    фан    732    фанти    —    fat    fat    fat    фат    733    финикийский    —
# phn    phn    phn    фик    738    фон    —    fon    fon    fon    фон    743    хайда    —    hai    hai    hai
# хай    753    хакасский    —    —    kjh    khk    хак    755    хантыйский(остяцкий)    —    —    kca    ost
# хан    760    хилигайнон    —    hil    hil    hil    хил    762    хотанский    —    kho    kho    kho    хот
# 773    хупа    —    hup    hup    hup    хуп    774    цахурский    —    —    tkr    tsa    цах    775    цимшиан
# —    tsi    tsi    tsi    цим    778    цыганский    —    rom    rom    rom    цыг    780    чагатайский    —
# chg    chg    chg    чаг    781    шайенн(чейенн)    —    chy    chy    chy    чей    783    чероки    —    chr
# chr    chr    чер    784    чибча    —    chb    chb    chb    чиб    792    чинук    жаргон    —    chn    chn
# chn    чин    793    чоктав    —    cho    cho    cho    чок    794    чукотский    —    —    ckt    chk    чук
# 800    шанский    —    shn    shn    shn    шан    803    шорский    —    —    cjs    sho    шор    810
# шотландский(англо - шотландский)    —    sco    sco    —    —    —    шугнанский    —    —    sgh    shu    шуг
# 815    шумерский    —    sux    sux    sux    шум    817    эвенкийский(тунгусский)    —    —    evn    tum    эвк
# 825    эвондо ewo    экаджук eka    эламский elx    эрзянский myv    эфик efi    якутский(саха) sah    яо  yao
# яп yap    клингонский tlh
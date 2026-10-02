# 167번: 30번·29번 레벨1 틀 재작성 (선생님 승인: 30번 15문항·29번 20문항, 29번은 기초 문법 추가)
#   · 정답 번호는 그대로. 레벨1 기준(단문, 접속사 없음, 기초 생활 어휘)에 맞춤. correctWord(틀렸을 때 보여 주는 말)도 새 문항에 맞춤
AUTO_SYNC = False
E = {}
C = '①②③④⑤'; CH = list(C)

# ───────────────────────── 30번 (낱말 쓰임) ─────────────────────────
def item30(n, ans, sents, marks, cw, vocab):
    # sents: [(영어 문장, 한글 해석)] / marks: [(낱말, 뜻, 이유)] 5개 — 정답 자리의 이유는 '왜 어울리지 않는지' / cw: (맞는 낱말, 뜻)
    text = ' '.join(e for e, k in sents); ko = ' '.join(k for e, k in sents)
    assert all(text.count(c) == 1 for c in C), n
    cn = []
    for k, (w, m, why) in enumerate(marks):
        assert (C[k] + w) in text, (n, k, w)
        if k == ans: cn.append("정답이에요! %s %s(%s) — %s 원래는 %s(%s)가 알맞아요." % (C[k], w, m, why, cw[0], cw[1]))
        else: cn.append("%s %s(%s) — %s" % (C[k], w, m, why))
    e, kk = [x for x in sents if C[ans] in x[0]][0]
    walk = ("① 낱말 쓰임 문제는 ①~⑤ 낱말이 앞뒤 내용과 맞는지 하나씩 확인해요. 답은 문맥과 반대되거나 어울리지 않는 낱말이에요.\n"
            "② 표시 %s번이 든 문장을 보세요.\n\"%s\" (%s)\n→ %s 원래는 %s(%s)가 알맞아요.\n"
            "③ 나머지 네 낱말은 모두 문맥에 맞아요. 그러니까 정답은 %s번이에요.\n📌 낱말: %s") % (C[ans], e, kk, marks[ans][2], cw[0], cw[1], C[ans], vocab)
    E[('30', '1', n)] = {'passage_ok': True, 'ans_ok': True, 'rewrite': {'text': text, 'choices': CH, 'ko': ko, 'walk': walk, 'cn': cn, 'cw': cw[0]}}

item30(3, 1, [("Ice ①melts in the sun.", "얼음은 햇볕에서 녹는다."), ("A cold box keeps it ②warm.", "아이스박스는 얼음을 따뜻하게(→ 차갑게) 유지한다."), ("A lid ③stops the warm air.", "뚜껑은 따뜻한 공기를 막는다."), ("A towel around the box ④helps too.", "상자를 감싼 수건도 도움이 된다."), ("Ice in a good box ⑤lasts all day.", "좋은 상자에 든 얼음은 하루 종일 간다.")],
  [("melts", "녹는다", "햇볕에서 얼음이 녹으니 맞아요."), ("warm", "따뜻한", "얼음이 오래가게 하는 상자이니 따뜻하게 유지한다는 것은 반대예요."), ("stops", "막는다", "뚜껑이 따뜻한 공기를 막으니 맞아요."), ("helps", "도움이 된다", "수건이 열을 막아 주니 맞아요."), ("lasts", "오래간다", "좋은 상자에서는 얼음이 오래가니 맞아요.")],
  ("cold", "차가운"), "melt 녹다 / lid 뚜껑 / last 오래가다")
item30(4, 1, [("Jun ①missed the bus this morning.", "준은 오늘 아침 버스를 놓쳤다."), ("He walked to school in the ②sun.", "그는 햇볕(→ 비) 속에 학교까지 걸어갔다."), ("His shoes were ③wet.", "그의 신발은 젖었다."), ("His friend ④lent him dry socks.", "그의 친구가 마른 양말을 빌려주었다."), ("Jun ⑤thanked him.", "준은 그에게 고마워했다.")],
  [("missed", "놓쳤다", "버스를 놓쳐서 걸어갔으니 맞아요."), ("sun", "햇볕", "신발이 젖고 마른 양말을 빌렸으니 햇볕 속을 걸었다는 것은 어울리지 않아요."), ("wet", "젖은", "빗속을 걸었으니 맞아요."), ("lent", "빌려주었다", "젖은 친구에게 마른 양말을 빌려주니 맞아요."), ("thanked", "고마워했다", "도움을 받았으니 맞아요.")],
  ("rain", "비"), "miss 놓치다 / lend 빌려주다 / sock 양말")
item30(5, 1, [("A candle ①needs air.", "양초에는 공기가 필요하다."), ("A glass over it ②helps the flame.", "그 위에 덮은 유리잔은 불꽃을 돕는다(→ 막는다)."), ("The flame ③gets smaller.", "불꽃은 점점 작아진다."), ("It ④dies in a minute.", "그것은 1분이면 꺼진다."), ("Fire cannot ⑤burn without air.", "불은 공기 없이 탈 수 없다.")],
  [("needs", "필요로 한다", "불은 공기가 있어야 타니 맞아요."), ("helps", "돕는다", "유리잔을 덮으면 불꽃이 작아지다 꺼진다고 했으니 불꽃을 돕는다는 것은 반대예요."), ("gets", "~해진다", "공기가 줄어 불꽃이 작아지니 맞아요."), ("dies", "꺼진다", "공기가 없어 꺼지니 맞아요."), ("burn", "타다", "공기 없이는 탈 수 없으니 맞아요.")],
  ("stops", "막는다"), "candle 양초 / flame 불꽃 / air 공기")
item30(6, 3, [("Mina ①lost her umbrella on Monday.", "미나는 월요일에 우산을 잃어버렸다."), ("A boy ②found it in the library.", "한 남자아이가 도서관에서 그것을 찾았다."), ("He ③took it to the office.", "그는 그것을 사무실에 가져다주었다."), ("Mina was ④sad to get it back.", "미나는 그것을 되찾아 슬펐다(→ 기뻤다)."), ("She ⑤thanked the boy.", "그녀는 그 아이에게 고마워했다.")],
  [("lost", "잃어버렸다", "나중에 되찾았으니 잃어버린 것이 맞아요."), ("found", "찾았다", "남자아이가 찾아 주었으니 맞아요."), ("took", "가져다주었다", "사무실에 맡겼으니 맞아요."), ("sad", "슬픈", "잃어버린 우산을 되찾고 고마워했으니 슬펐다는 것은 반대예요."), ("thanked", "고마워했다", "우산을 찾아 주었으니 맞아요.")],
  ("happy", "기쁜"), "lose 잃어버리다 / find 찾다 / office 사무실")
item30(8, 3, [("Cats ①see well at night.", "고양이는 밤에 잘 본다."), ("Their eyes ②open wide in the dark.", "고양이의 눈은 어둠 속에서 크게 열린다."), ("Whiskers ③feel things nearby.", "수염은 가까이 있는 것을 느낀다."), ("A cat walks ④loudly on soft feet.", "고양이는 부드러운 발로 시끄럽게(→ 조용히) 걷는다."), ("Mice rarely ⑤hear it.", "쥐는 그 소리를 거의 듣지 못한다.")],
  [("see", "보다", "밤에 사냥하는 동물이니 맞아요."), ("open", "열리다", "어두울 때 눈이 크게 열리니 맞아요."), ("feel", "느끼다", "수염으로 가까운 것을 느끼니 맞아요."), ("loudly", "시끄럽게", "부드러운 발로 걷고 쥐가 듣지 못한다고 했으니 시끄럽게 걷는다는 것은 반대예요."), ("hear", "듣다", "조용히 걸으니 쥐가 듣지 못해요. 맞아요.")],
  ("quietly", "조용히"), "whisker 수염 / nearby 가까이 / rarely 거의 ~않다")
item30(10, 3, [("Sora ①planted beans in May.", "소라는 5월에 콩을 심었다."), ("She ②watered them every day.", "그녀는 날마다 물을 주었다."), ("Green leaves ③came up in a week.", "일주일 만에 초록 잎이 올라왔다."), ("The plants grew ④short by July.", "7월이 되자 그 식물은 작게(→ 크게) 자랐다."), ("They ⑤reached the top of the fence.", "그것들은 울타리 꼭대기까지 닿았다.")],
  [("planted", "심었다", "콩을 심어 길렀으니 맞아요."), ("watered", "물을 주었다", "날마다 돌보았으니 맞아요."), ("came", "나왔다", "잎이 올라왔으니 맞아요."), ("short", "작은", "울타리 꼭대기까지 닿았다고 했으니 작게 자랐다는 것은 반대예요."), ("reached", "닿았다", "크게 자라 울타리 꼭대기에 닿았으니 맞아요.")],
  ("tall", "큰"), "plant 심다 / fence 울타리 / reach 닿다")
item30(16, 0, [("A wet road is ①safe for bicycles.", "젖은 길은 자전거에 안전하다(→ 위험하다)."), ("Tyres ②slip on water.", "타이어는 물 위에서 미끄러진다."), ("Brakes ③work slowly in rain.", "브레이크는 빗속에서 느리게 듣는다."), ("A rider should ④slow down.", "타는 사람은 속도를 줄여야 한다."), ("Bright clothes ⑤help drivers see.", "밝은 옷은 운전자가 보는 데 도움이 된다.")],
  [("safe", "안전한", "타이어가 미끄러지고 브레이크가 느리게 듣는다고 했으니 안전하다는 것은 반대예요."), ("slip", "미끄러지다", "물 위에서 타이어가 미끄러지니 맞아요."), ("work", "작동하다", "비가 오면 브레이크가 느리게 들으니 맞아요."), ("slow", "속도를 줄이다", "위험하니 천천히 가야 해요. 맞아요."), ("help", "돕다", "밝은 옷이 눈에 잘 띄니 맞아요.")],
  ("dangerous", "위험한"), "tyre 타이어 / slip 미끄러지다 / brake 브레이크")
item30(21, 4, [("Kai ①woke up late on Sunday.", "카이는 일요일에 늦게 일어났다."), ("He ②ran to the bus stop.", "그는 버스 정류장으로 달려갔다."), ("The bus ③left without him.", "버스는 그를 태우지 않고 떠났다."), ("He ④waited twenty minutes for the next one.", "그는 다음 버스를 20분 동안 기다렸다."), ("He got to the match ⑤early.", "그는 경기에 일찍(→ 늦게) 도착했다.")],
  [("woke", "일어났다", "늦게 일어나서 서두른 것이니 맞아요."), ("ran", "달렸다", "늦어서 달려갔으니 맞아요."), ("left", "떠났다", "버스를 놓쳐 다음 버스를 기다렸으니 맞아요."), ("waited", "기다렸다", "다음 버스를 기다렸으니 맞아요."), ("early", "일찍", "늦게 일어나고 버스도 놓쳤으니 일찍 도착했다는 것은 어울리지 않아요.")],
  ("late", "늦게"), "wake up 일어나다 / bus stop 버스 정류장 / match 경기")
item30(23, 4, [("A ①full bag is heavy.", "가득 찬 가방은 무겁다."), ("Heavy bags ②hurt the back.", "무거운 가방은 허리를 아프게 한다."), ("Two straps ③share the weight.", "두 개의 끈은 무게를 나눈다."), ("A small bag ④holds less.", "작은 가방에는 덜 들어간다."), ("A light bag is ⑤worse for a child.", "가벼운 가방이 아이에게 더 나쁘다(→ 더 좋다).")],
  [("full", "가득 찬", "가득 차면 무거우니 맞아요."), ("hurt", "아프게 하다", "무거운 가방이 허리에 해로우니 맞아요."), ("share", "나누다", "끈이 두 개면 무게가 나뉘니 맞아요."), ("holds", "담는다", "작은 가방에는 덜 들어가니 맞아요."), ("worse", "더 나쁜", "무거운 가방이 허리를 아프게 한다고 했으니 가벼운 가방이 더 나쁘다는 것은 반대예요.")],
  ("better", "더 좋은"), "strap 끈 / weight 무게 / hold 담다")
item30(24, 2, [("Birds ①fly south in autumn.", "새들은 가을에 남쪽으로 날아간다."), ("The north gets ②cold.", "북쪽은 추워진다."), ("Food there becomes ③easy to find.", "그곳에서는 먹이를 찾기가 쉬워진다(→ 어려워진다)."), ("The south stays ④warm.", "남쪽은 따뜻하게 유지된다."), ("The birds ⑤return in spring.", "새들은 봄에 돌아온다.")],
  [("fly", "날아가다", "가을에 남쪽으로 떠나니 맞아요."), ("cold", "추운", "추워져서 떠나는 것이니 맞아요."), ("easy", "쉬운", "새들이 추운 북쪽을 떠난다고 했으니 먹이를 찾기 쉬워진다는 것은 반대예요."), ("warm", "따뜻한", "따뜻한 남쪽으로 가는 것이니 맞아요."), ("return", "돌아오다", "봄이 되면 돌아오니 맞아요.")],
  ("hard", "어려운"), "south 남쪽 / autumn 가을 / return 돌아오다")
item30(25, 2, [("Dana ①baked a cake for her mother.", "다나는 어머니를 위해 케이크를 구웠다."), ("She ②forgot the sugar.", "그녀는 설탕을 넣는 것을 잊었다."), ("The cake tasted ③great.", "케이크는 맛이 훌륭했다(→ 나빴다)."), ("Her mother ④laughed kindly.", "어머니는 다정하게 웃었다."), ("They ⑤added jam on top.", "그들은 위에 잼을 얹었다.")],
  [("baked", "구웠다", "케이크를 만든 이야기이니 맞아요."), ("forgot", "잊었다", "설탕을 빠뜨려서 잼을 얹은 것이니 맞아요."), ("great", "훌륭한", "설탕을 빠뜨리고 나중에 잼을 얹었으니 맛이 훌륭했다는 것은 어울리지 않아요."), ("laughed", "웃었다", "어머니가 다정하게 웃어넘겼으니 맞아요."), ("added", "더했다", "단맛을 내려고 잼을 얹었으니 맞아요.")],
  ("bad", "나쁜"), "bake 굽다 / forget 잊다 / taste 맛이 나다")
item30(26, 2, [("Snow ①falls in winter.", "겨울에는 눈이 내린다."), ("Children ②build snowmen.", "아이들은 눈사람을 만든다."), ("The sun comes out.", "해가 나온다."), ("The snowmen get ③bigger.", "눈사람은 점점 커진다(→ 작아진다)."), ("Only hats ④stay on the grass.", "풀밭에는 모자만 남는다."), ("The children ⑤wait for more snow.", "아이들은 눈이 더 오기를 기다린다.")],
  [("falls", "내린다", "겨울에 눈이 내리니 맞아요."), ("build", "만들다", "눈으로 눈사람을 만드니 맞아요."), ("bigger", "더 큰", "해가 나오고 모자만 남았다고 했으니 눈사람이 커진다는 것은 반대예요."), ("stay", "남다", "눈이 녹아 모자만 남으니 맞아요."), ("wait", "기다리다", "눈사람이 녹았으니 눈을 다시 기다려요. 맞아요.")],
  ("smaller", "더 작은"), "snowman 눈사람 / grass 풀밭 / wait 기다리다")
item30(27, 2, [("Minho ①studied hard for the test.", "민호는 시험을 위해 열심히 공부했다."), ("He ②slept early the night before.", "그는 전날 밤 일찍 잤다."), ("The questions looked ③hard to him.", "문제들은 그에게 어려워(→ 쉬워) 보였다."), ("He ④finished first.", "그는 가장 먼저 끝냈다."), ("His score was ⑤high.", "그의 점수는 높았다.")],
  [("studied", "공부했다", "열심히 준비했으니 맞아요."), ("slept", "잤다", "전날 일찍 자고 준비했으니 맞아요."), ("hard", "어려운", "열심히 공부했고 가장 먼저 끝내 점수도 높았으니 문제가 어려워 보였다는 것은 어울리지 않아요."), ("finished", "끝냈다", "문제가 쉬워 먼저 끝냈으니 맞아요."), ("high", "높은", "잘 준비했으니 점수가 높아요. 맞아요.")],
  ("easy", "쉬운"), "test 시험 / question 문제 / score 점수")
item30(28, 2, [("A hot bath ①warms the body.", "뜨거운 목욕은 몸을 따뜻하게 한다."), ("Warm muscles ②relax.", "따뜻해진 근육은 풀어진다."), ("Sleep comes ③slowly after a bath.", "목욕 뒤에는 잠이 천천히(→ 빨리) 온다."), ("People ④feel calm.", "사람들은 마음이 차분해진다."), ("A bath before bed ⑤helps.", "자기 전의 목욕은 도움이 된다.")],
  [("warms", "따뜻하게 한다", "뜨거운 물이 몸을 데우니 맞아요."), ("relax", "풀어지다", "따뜻하면 근육이 풀리니 맞아요."), ("slowly", "천천히", "몸이 풀리고 차분해져서 자기 전 목욕이 도움이 된다고 했으니 잠이 천천히 온다는 것은 반대예요."), ("feel", "느끼다", "목욕 뒤에 마음이 차분해지니 맞아요."), ("helps", "도움이 된다", "잠드는 데 도움이 되니 맞아요.")],
  ("quickly", "빨리"), "bath 목욕 / muscle 근육 / calm 차분한")
item30(29, 2, [("Yuna ①moved to a new school.", "유나는 새 학교로 전학했다."), ("She ②knew nobody there.", "그녀는 그곳에 아는 사람이 없었다."), ("The first day felt ③short.", "첫날은 짧게(→ 길게) 느껴졌다."), ("A girl ④shared her lunch with her.", "한 여자아이가 자기 점심을 나누어 주었다."), ("Yuna ⑤smiled at last.", "유나는 마침내 웃었다.")],
  [("moved", "옮겼다", "새 학교에 온 이야기이니 맞아요."), ("knew", "알았다", "아는 사람이 없어 외로웠으니 맞아요."), ("short", "짧은", "아는 사람이 없었고 '마침내' 웃었다고 했으니 첫날이 짧게 느껴졌다는 것은 어울리지 않아요."), ("shared", "나누어 주었다", "친구가 점심을 나누어 주었으니 맞아요."), ("smiled", "웃었다", "친구가 생겨 웃었으니 맞아요.")],
  ("long", "긴"), "move 옮기다 / nobody 아무도 / at last 마침내")

# ───────────────────────── 29번 (어법) ─────────────────────────
HINT = {
 'agree': ("이 글은 '누가 하는 일인지(주어)'를 보고 동사 모양을 살펴보면 돼요.\n· 주어가 하나(He, She, It, 이름 등) → 동사에 -s (has, is, likes)\n· 주어가 여럿(They 등) → 동사 원형 (have, are, like)",
           "주어가 하나(He, She, It, 이름 등)면 동사에 -s (has, is, likes) / 주어가 여럿(They 등)이면 동사 원형 (have, are, like)"),
 'past':  ("이 글은 '언제 일인지'를 보고 동사 모양을 살펴보면 돼요.\n· 지난 일(yesterday, last ~, ~ ago) → 과거형 (went, came, was)",
           "지난 일(yesterday, last ~, ~ ago)은 동사를 과거형으로 써요 (go → went, come → came, open → opened)"),
 'modal': ("이 글은 can·will 뒤에 오는 동사 모양을 살펴보면 돼요.\n· can, cannot, will 뒤 → 주어가 누구든 동사 원형 (can swim, will come)",
           "can, cannot, will 뒤에는 주어가 누구든 동사 원형을 써요 (can swim, will come)"),
 'plural':("이 글은 '하나인지 여럿인지'를 보고 이름 말(명사)의 모양을 살펴보면 돼요.\n· 둘 이상 → -s를 붙여요 (two beds)\n· 하나 → 붙이지 않아요 (a bed, each student)",
           "둘 이상을 말할 때는 명사에 -s를 붙여요 (two beds, three cats) / 하나일 때는 붙이지 않아요 (a bed, one cat)"),
 'pron':  ("이 글은 사람을 가리키는 말(I, he, she …)이 놓인 자리를 살펴보면 돼요.\n· 주어 자리 → I, he, she, we, they\n· 동사나 to·with 뒤 → me, him, her, us, them",
           "주어 자리에는 I, he, she, we, they를 쓰고, 동사나 to·with 뒤에는 me, him, her, us, them을 써요"),
}
def item29(n, ans, kind, sents, marks, right, vocab):
    # marks: [(낱말, 설명)] 5개 — 정답 자리의 설명은 '왜 틀렸는지'(끝에 "틀린 꼴 (×) → 맞는 꼴 (○)"가 자동으로 붙음) / right: 맞는 꼴
    text = ' '.join(e for e, k in sents); ko = ' '.join(k for e, k in sents)
    assert all(text.count(c) == 1 for c in C), n
    cn = []
    for k, (w, note) in enumerate(marks):
        assert (C[k] + w) in text, (n, k, w)
        if k == ans: cn.append("정답이에요! %s %s — %s %s (×) → %s (○)" % (C[k], w, note, w, right))
        else: cn.append("%s %s — %s" % (C[k], w, note))
    e, kk = [x for x in sents if C[ans] in x[0]][0]
    hint, rule = HINT[kind]
    walk = ("① 어법 문제는 밑줄 친 부분이 문장 안에서 맞는 형태인지 하나씩 확인해요. %s\n"
            "② 표시 %s번이 든 문장을 보세요.\n\"%s\" (%s)\n→ %s %s (×) → %s (○)\n"
            "③ 나머지 네 곳은 모두 맞아요. 그러니까 정답은 %s번이에요.\n📌 문법: %s\n📌 낱말: %s") % (hint, C[ans], e, kk, marks[ans][1], marks[ans][0], right, C[ans], rule, vocab)
    E[('29', '1', n)] = {'passage_ok': True, 'ans_ok': True, 'rewrite': {'text': text, 'choices': CH, 'ko': ko, 'walk': walk, 'cn': cn, 'cw': right}}

# ── 과거 시제 ──
item29(1, 2, 'past', [("Jina ①went to the market yesterday.", "지나는 어제 시장에 갔다."), ("She ②bought three apples.", "그녀는 사과 세 개를 샀다."), ("She ③come home at noon.", "그녀는 정오에 집에 왔다."), ("Her mother ④made a pie.", "그녀의 어머니는 파이를 만들었다."), ("It ⑤was sweet.", "그것은 달았다.")],
  [("went", "어제(yesterday) 일: 과거형 went (○)"), ("bought", "어제 일: 과거형 bought (○)"), ("come", "어제 일이니 과거형으로 써야 해요."), ("made", "어제 일: 과거형 made (○)"), ("was", "어제 일: 과거형 was (○)")], "came", "market 시장 / noon 정오 / sweet 단")
item29(7, 3, 'past', [("Minsu ①was sick last week.", "민수는 지난주에 아팠다."), ("He ②stayed in bed for two days.", "그는 이틀 동안 침대에 누워 있었다."), ("His friend ③brought his homework.", "그의 친구가 숙제를 가져다주었다."), ("Minsu ④feel better on Friday.", "민수는 금요일에 몸이 나아졌다."), ("He ⑤went back to school.", "그는 학교로 돌아갔다.")],
  [("was", "지난주(last week) 일: 과거형 was (○)"), ("stayed", "지난주 일: 과거형 stayed (○)"), ("brought", "지난주 일: 과거형 brought (○)"), ("feel", "지난주 일이니 과거형으로 써야 해요."), ("went", "지난주 일: 과거형 went (○)")], "felt", "sick 아픈 / stay 머무르다 / bring 가져오다")
item29(9, 1, 'past', [("Hana ①got a letter yesterday.", "하나는 어제 편지를 받았다."), ("She ②open it at the door.", "그녀는 문 앞에서 그것을 열었다."), ("Her aunt ③wrote it in Busan.", "그녀의 이모가 부산에서 그것을 썼다."), ("A photo ④fell out.", "사진 한 장이 떨어졌다."), ("Hana ⑤put it on her desk.", "하나는 그것을 책상 위에 놓았다.")],
  [("got", "어제(yesterday) 일: 과거형 got (○)"), ("open", "어제 일이니 과거형으로 써야 해요."), ("wrote", "지난 일: 과거형 wrote (○)"), ("fell", "어제 일: 과거형 fell (○)"), ("put", "어제 일: put은 과거형도 모양이 같아요. put (○)")], "opened", "letter 편지 / aunt 이모 / photo 사진")
item29(12, 4, 'past', [("It ①rained all day last Sunday.", "지난 일요일에는 하루 종일 비가 왔다."), ("We ②stayed at home.", "우리는 집에 있었다."), ("My father ③cooked noodles.", "아버지가 국수를 만들었다."), ("We ④watched a film.", "우리는 영화를 보았다."), ("Everybody ⑤sleep early.", "모두 일찍 잤다.")],
  [("rained", "지난 일요일(last Sunday) 일: 과거형 rained (○)"), ("stayed", "지난 일요일 일: 과거형 stayed (○)"), ("cooked", "지난 일요일 일: 과거형 cooked (○)"), ("watched", "지난 일요일 일: 과거형 watched (○)"), ("sleep", "지난 일요일 일이니 과거형으로 써야 해요.")], "slept", "rain 비가 오다 / noodle 국수 / film 영화")
item29(23, 0, 'past', [("We ①visit the zoo two days ago.", "우리는 이틀 전에 동물원에 갔다."), ("A monkey ②took my hat.", "원숭이 한 마리가 내 모자를 가져갔다."), ("A keeper ③gave it back.", "사육사가 그것을 돌려주었다."), ("My sister ④laughed.", "내 여동생은 웃었다."), ("I ⑤was red in the face.", "나는 얼굴이 빨개졌다.")],
  [("visit", "이틀 전(two days ago) 일이니 과거형으로 써야 해요."), ("took", "이틀 전 일: 과거형 took (○)"), ("gave", "이틀 전 일: 과거형 gave (○)"), ("laughed", "이틀 전 일: 과거형 laughed (○)"), ("was", "이틀 전 일: 과거형 was (○)")], "visited", "zoo 동물원 / keeper 사육사 / face 얼굴")
# ── can·will 뒤 동사 원형 ──
item29(3, 2, 'modal', [("My sister ①is six.", "내 여동생은 여섯 살이다."), ("She can ②ride a bike.", "그녀는 자전거를 탈 수 있다."), ("She can ③swims too.", "그녀는 수영도 할 수 있다."), ("She cannot ④cook yet.", "그녀는 아직 요리는 할 수 없다."), ("I ⑤help her in the kitchen.", "나는 부엌에서 그녀를 돕는다.")],
  [("is", "주어 My sister: 하나(단수) → is (○)"), ("ride", "can 뒤: 동사 원형 ride (○)"), ("swims", "can 뒤에는 주어가 누구든 동사 원형을 써야 해요."), ("cook", "cannot 뒤: 동사 원형 cook (○)"), ("help", "주어 I → help (○)")], "swim", "ride 타다 / yet 아직 / kitchen 부엌")
item29(8, 3, 'modal', [("Birds ①have wings.", "새는 날개가 있다."), ("Most birds can ②fly.", "대부분의 새는 날 수 있다."), ("A penguin ③is a bird too.", "펭귄도 새이다."), ("It cannot ④flies.", "그것은 날 수 없다."), ("It can ⑤swim very fast.", "그것은 아주 빨리 헤엄칠 수 있다.")],
  [("have", "주어 Birds: 여럿(복수) → have (○)"), ("fly", "can 뒤: 동사 원형 fly (○)"), ("is", "주어 A penguin: 하나(단수) → is (○)"), ("flies", "cannot 뒤에는 주어가 누구든 동사 원형을 써야 해요."), ("swim", "can 뒤: 동사 원형 swim (○)")], "fly", "wing 날개 / penguin 펭귄 / fast 빨리")
item29(13, 4, 'modal', [("Our dog ①is very clever.", "우리 개는 아주 영리하다."), ("He can ②open the door.", "그는 문을 열 수 있다."), ("He can ③find my shoes.", "그는 내 신발을 찾을 수 있다."), ("He will ④wait at the gate.", "그는 대문에서 기다릴 것이다."), ("He cannot ⑤reads, of course.", "물론 그는 글을 읽을 수는 없다.")],
  [("is", "주어 Our dog: 하나(단수) → is (○)"), ("open", "can 뒤: 동사 원형 open (○)"), ("find", "can 뒤: 동사 원형 find (○)"), ("wait", "will 뒤: 동사 원형 wait (○)"), ("reads", "cannot 뒤에는 주어가 누구든 동사 원형을 써야 해요.")], "read", "clever 영리한 / gate 대문 / of course 물론")
item29(24, 1, 'modal', [("Tomorrow ①is Sunday.", "내일은 일요일이다."), ("My uncle will ②comes at ten.", "삼촌이 열 시에 올 것이다."), ("We will ③go to the lake.", "우리는 호수에 갈 것이다."), ("He can ④catch big fish.", "그는 큰 물고기를 잡을 수 있다."), ("I ⑤want to learn.", "나는 배우고 싶다.")],
  [("is", "주어 Tomorrow: 하나(단수) → is (○)"), ("comes", "will 뒤에는 주어가 누구든 동사 원형을 써야 해요."), ("go", "will 뒤: 동사 원형 go (○)"), ("catch", "can 뒤: 동사 원형 catch (○)"), ("want", "주어 I → want (○)")], "come", "uncle 삼촌 / lake 호수 / catch 잡다")
# ── 복수형 ──
item29(4, 2, 'plural', [("I ①have two brothers.", "나는 형제가 둘 있다."), ("We ②share one room.", "우리는 방 하나를 함께 쓴다."), ("There are three ③bed in it.", "그 안에는 침대가 세 개 있다."), ("My ④desk is by the window.", "내 책상은 창가에 있다."), ("Our ⑤books are on one shelf.", "우리 책들은 한 선반에 있다.")],
  [("have", "주어 I → have (○)"), ("share", "주어 We: 여럿(복수) → share (○)"), ("bed", "three 뒤이니 여럿을 나타내는 -s를 붙여야 해요."), ("desk", "책상이 하나: desk (○)"), ("books", "책이 여럿(뒤에 are): books (○)")], "beds", "share 함께 쓰다 / shelf 선반 / window 창문")
item29(10, 3, 'plural', [("A spider ①has eight legs.", "거미는 다리가 여덟 개다."), ("An ant has six ②legs.", "개미는 다리가 여섯 개다."), ("A bird has two ③wings.", "새는 날개가 두 개다."), ("A cat has four ④leg.", "고양이는 다리가 네 개다."), ("A snake ⑤has none.", "뱀은 하나도 없다.")],
  [("has", "주어 A spider: 하나(단수) → has (○)"), ("legs", "six 뒤: 여럿 → legs (○)"), ("wings", "two 뒤: 여럿 → wings (○)"), ("leg", "four 뒤이니 여럿을 나타내는 -s를 붙여야 해요."), ("has", "주어 A snake: 하나(단수) → has (○)")], "legs", "spider 거미 / ant 개미 / snake 뱀")
item29(14, 4, 'plural', [("Our class ①has twenty students.", "우리 반에는 학생이 스무 명 있다."), ("Ten ②girls sit by the window.", "여학생 열 명은 창가에 앉는다."), ("Ten ③boys sit by the door.", "남학생 열 명은 문가에 앉는다."), ("Each ④student has a desk.", "학생마다 책상이 하나씩 있다."), ("We need twenty ⑤chair.", "우리에게는 의자가 스무 개 필요하다.")],
  [("has", "주어 Our class: 하나(단수) → has (○)"), ("girls", "Ten 뒤: 여럿 → girls (○)"), ("boys", "Ten 뒤: 여럿 → boys (○)"), ("student", "Each 뒤: 한 명씩 말하므로 student (○)"), ("chair", "twenty 뒤이니 여럿을 나타내는 -s를 붙여야 해요.")], "chairs", "class 반 / each 각각의 / need 필요하다")
item29(25, 0, 'plural', [("Mina has three ①cat.", "미나에게는 고양이가 세 마리 있다."), ("One ②cat is white.", "한 마리는 하얗다."), ("Two ③cats are black.", "두 마리는 검다."), ("They ④sleep on her bed.", "그들은 그녀의 침대에서 잔다."), ("She ⑤loves them all.", "그녀는 그들을 모두 사랑한다.")],
  [("cat", "three 뒤이니 여럿을 나타내는 -s를 붙여야 해요."), ("cat", "One 뒤: 하나 → cat (○)"), ("cats", "Two 뒤: 여럿 → cats (○)"), ("sleep", "주어 They: 여럿(복수) → sleep (○)"), ("loves", "주어 She: 하나(단수) → loves (○)")], "cats", "white 하얀 / black 검은 / bed 침대")
# ── 대명사 ──
item29(5, 2, 'pron', [("Jisu ①has a little brother.", "지수에게는 어린 남동생이 있다."), ("②He is four years old.", "그는 네 살이다."), ("She reads to ③he every night.", "그녀는 매일 밤 그에게 책을 읽어 준다."), ("④They like animal stories.", "그들은 동물 이야기를 좋아한다."), ("The stories make ⑤them laugh.", "그 이야기들은 그들을 웃게 한다.")],
  [("has", "주어 Jisu: 하나(단수) → has (○)"), ("He", "문장의 주어 자리: He (○)"), ("he", "to 뒤는 주어 자리가 아니에요. '그에게'는 him으로 써야 해요."), ("They", "문장의 주어 자리: They (○)"), ("them", "make 뒤(~을/를 자리): them (○)")], "him", "little 어린 / every night 매일 밤 / laugh 웃다")
item29(15, 1, 'pron', [("My grandmother ①lives in the country.", "우리 할머니는 시골에 사신다."), ("②Her has a small garden.", "할머니에게는 작은 정원이 있다."), ("③She grows tomatoes.", "할머니는 토마토를 기르신다."), ("I visit ④her in summer.", "나는 여름에 할머니를 찾아뵌다."), ("She gives ⑤me a big bag of them.", "할머니는 나에게 토마토를 큰 봉지 가득 주신다.")],
  [("lives", "주어 My grandmother: 하나(단수) → lives (○)"), ("Her", "문장의 주어 자리이니 She로 써야 해요."), ("She", "문장의 주어 자리: She (○)"), ("her", "visit 뒤(~을/를 자리): her (○)"), ("me", "gives 뒤(~에게 자리): me (○)")], "She", "country 시골 / garden 정원 / grow 기르다")
item29(26, 1, 'pron', [("Tom and ①I are in the same class.", "톰과 나는 같은 반이다."), ("②Us sit together.", "우리는 함께 앉는다."), ("The teacher knows ③us well.", "선생님은 우리를 잘 아신다."), ("④She gives us hard questions.", "선생님은 우리에게 어려운 문제를 내신다."), ("⑤We like them.", "우리는 그 문제들을 좋아한다.")],
  [("I", "'Tom and I'가 문장의 주어 자리: I (○)"), ("Us", "문장의 주어 자리이니 We로 써야 해요."), ("us", "knows 뒤(~을/를 자리): us (○)"), ("She", "문장의 주어 자리: She (○)"), ("We", "문장의 주어 자리: We (○)")], "We", "same 같은 / together 함께 / question 문제")
item29(27, 0, 'pron', [("①Me have a new friend.", "나에게는 새 친구가 있다."), ("②Her name is Sora.", "그녀의 이름은 소라이다."), ("③She lives next door.", "그녀는 옆집에 산다."), ("We walk to school with ④her dog.", "우리는 그녀의 개와 함께 학교까지 걸어간다."), ("Sora tells ⑤me funny stories.", "소라는 나에게 재미있는 이야기를 해 준다.")],
  [("Me", "문장의 주어 자리이니 I로 써야 해요."), ("Her", "name 앞('~의' 자리): Her (○)"), ("She", "문장의 주어 자리: She (○)"), ("her", "dog 앞('~의' 자리): her (○)"), ("me", "tells 뒤(~에게 자리): me (○)")], "I", "next door 옆집에 / walk 걷다 / funny 재미있는")
# ── 수 일치(새 상황) ──
item29(21, 4, 'agree', [("The sun ①rises in the east.", "해는 동쪽에서 뜬다."), ("Farmers ②get up early.", "농부들은 일찍 일어난다."), ("A rooster ③wakes the village.", "수탉이 마을을 깨운다."), ("Children ④walk to school.", "아이들은 학교까지 걸어간다."), ("The bus ⑤come at eight.", "버스는 여덟 시에 온다.")],
  [("rises", "주어 The sun: 하나(단수) → rises (○)"), ("get", "주어 Farmers: 여럿(복수) → 동사 원형 get (○)"), ("wakes", "주어 A rooster: 하나(단수) → wakes (○)"), ("walk", "주어 Children: 여럿(복수) → 동사 원형 walk (○)"), ("come", "주어 The bus: 하나(단수) → 동사에 -s를 붙여야 해요.")], "comes", "east 동쪽 / rooster 수탉 / village 마을")
item29(28, 0, 'agree', [("My parents ①works in a hospital.", "우리 부모님은 병원에서 일하신다."), ("My mother ②is a nurse.", "어머니는 간호사이다."), ("My father ③drives an ambulance.", "아버지는 구급차를 운전하신다."), ("They ④come home late.", "두 분은 늦게 집에 오신다."), ("I ⑤cook dinner on Fridays.", "나는 금요일마다 저녁을 만든다.")],
  [("works", "주어 My parents: 여럿(복수) → -s를 붙이지 않아요."), ("is", "주어 My mother: 하나(단수) → is (○)"), ("drives", "주어 My father: 하나(단수) → drives (○)"), ("come", "주어 They: 여럿(복수) → 동사 원형 come (○)"), ("cook", "주어 I → cook (○)")], "work", "hospital 병원 / nurse 간호사 / ambulance 구급차")
item29(29, 0, 'agree', [("There ①is two parks in my town.", "우리 마을에는 공원이 두 개 있다."), ("One ②has a pond.", "하나에는 연못이 있다."), ("Ducks ③swim there.", "오리들이 그곳에서 헤엄친다."), ("The other ④is near my house.", "다른 하나는 우리 집 가까이에 있다."), ("I ⑤play football in it.", "나는 그곳에서 축구를 한다.")],
  [("is", "뒤에 오는 two parks가 여럿(복수)이므로 are로 써야 해요."), ("has", "주어 One: 하나(단수) → has (○)"), ("swim", "주어 Ducks: 여럿(복수) → 동사 원형 swim (○)"), ("is", "주어 The other: 하나(단수) → is (○)"), ("play", "주어 I → play (○)")], "are", "park 공원 / pond 연못 / duck 오리")

# 168번: 44번 레벨3 틀 재작성 — 같은 틀("X가 ~를 운영했다 … (a) 몇 년 운영 (b) 먼저 ~ (c)/(d) … (e) 지금은 ~" + "주인에게 말했다"가 늘 정답)이던
#   28문항 가운데 20문항을 짧은 이야기글로 새로 씀. 정답 번호는 그대로.
#   · 두 인물을 같은 성별로 두어 모양(he/she)으로는 가릴 수 없게 하고, 누구인지는 앞뒤 내용으로만 알 수 있게 함
#   · 가리키는 말의 꼴(he·him·his / she·her)과 '혼자 다른 사람'의 구실(돕는 사람·주인공)을 섞음
AUTO_SYNC = False
E = {}
L = ['(a)', '(b)', '(c)', '(d)', '(e)']
def josa(name):   # 받침이 있으면 '이에요', 없으면 '예요'
    c = ord(name[-1]); return '이에요' if (0xAC00 <= c <= 0xD7A3 and (c - 0xAC00) % 28) else '예요'
def item(n, ans, A, B, sents, refs, vocab):
    # A: 넷이 가리키는 사람 / B: 혼자 다른 사람 / sents: [(영어, 한글)] / refs: [이유] 5개((a)~(e) 순서)
    text = ' '.join(e for e, k in sents); ko = ' '.join(k for e, k in sents)
    assert all(text.count(x) == 1 and ko.count(x) == 1 for x in L), n
    cn = []
    for k, why in enumerate(refs):
        if k == ans: cn.append("정답이에요! %s → %s. %s 나머지 넷은 모두 %s%s." % (L[k], B, why, A, josa(A)))
        else: cn.append("%s → %s. %s" % (L[k], A, why))
    e, kk = [x for x in sents if L[ans] in x[0]][0]
    walk = ("① 이 문제는 (a)~(e)가 각각 누구를 가리키는지 확인해요. 넷은 같은 사람이고, 하나만 다른 사람이에요.\n"
            "② %s 문장을 보세요.\n\"%s\" (%s)\n→ %s\n③ 나머지 넷은 모두 %s%s. 그러니까 정답은 %s예요.\n📌 낱말: %s") % (L[ans], e, kk, refs[ans], A, josa(A), L[ans], vocab)
    E[('44', '3', n)] = {'passage_ok': True, 'ans_ok': True, 'rewrite': {'text': text, 'choices': list(L), 'ko': ko, 'walk': walk, 'cn': cn}}

item(3, 2, '다니엘', '할아버지',
 [("Daniel wanted to learn chess, so (a)he asked his grandfather to teach him.", "다니엘은 체스를 배우고 싶어서 (a)그는 할아버지에게 가르쳐 달라고 부탁했다."),
  ("Every Sunday (b)he carried the board to the old man's flat.", "일요일마다 (b)그는 체스판을 들고 할아버지의 아파트로 갔다."),
  ("His grandfather was patient, and (c)he never laughed at a bad move.", "할아버지는 참을성이 있었고, (c)그는 나쁜 수를 두어도 결코 웃지 않았다."),
  ("After a year (d)he beat the old man for the first time.", "1년 뒤 (d)그는 처음으로 할아버지를 이겼다."),
  ("That night (e)he could not sleep because he was so proud.", "그날 밤 (e)그는 너무 뿌듯해서 잠을 이루지 못했다.")],
 ["가르쳐 달라고 부탁한 사람은 다니엘이에요.", "체스판을 들고 할아버지 댁으로 간 사람은 다니엘이에요.", "바로 앞에서 '할아버지는 참을성이 있었다'고 했으니, 나쁜 수에도 웃지 않은 사람은 할아버지예요.", "할아버지(the old man)를 이긴 사람은 다니엘이에요.", "뿌듯해서 잠을 못 이룬 사람은 다니엘이에요."],
 "patient 참을성 있는 / move (체스의) 수 / proud 뿌듯한")
item(4, 2, '유나', '보라',
 [("Yuna forgot her lunch on the day of the school trip, and (a)she was too shy to tell anyone.", "유나는 소풍날 점심을 잊고 왔는데, (a)그녀는 너무 수줍어서 아무에게도 말하지 못했다."),
  ("At noon (b)she sat a little away from the group.", "정오에 (b)그녀는 무리에서 조금 떨어져 앉았다."),
  ("Bora saw this, and (c)she quietly cut her own sandwich in half.", "보라가 이것을 보았고, (c)그녀는 조용히 자기 샌드위치를 반으로 잘랐다."),
  ("Yuna thanked her, and (d)she promised to bring fruit for both of them next time.", "유나는 고맙다고 했고, (d)그녀는 다음에는 둘이 먹을 과일을 가져오겠다고 약속했다."),
  ("Since that day (e)she has never forgotten her lunch again.", "그날 이후로 (e)그녀는 다시는 점심을 잊지 않았다.")],
 ["수줍어서 말하지 못한 사람은 점심을 잊고 온 유나예요.", "떨어져 앉은 사람은 점심이 없던 유나예요.", "바로 앞의 '보라가 이것을 보았다'에 이어, 자기 샌드위치를 반으로 자른 사람은 보라예요.", "고맙다고 한 유나가 과일을 가져오겠다고 약속했어요.", "점심을 잊었던 사람은 유나예요."],
 "shy 수줍은 / quietly 조용히 / promise 약속하다")
item(6, 2, '벤', '홀 씨',
 [("Ben broke a window when (a)he kicked a ball too hard in the street.", "벤은 길에서 (a)그가 공을 너무 세게 찼을 때 창문을 깨뜨렸다."),
  ("(b)He knocked on the door at once because he wanted to say sorry.", "(b)그는 사과하고 싶어서 곧바로 문을 두드렸다."),
  ("Mr. Hall opened it, and (c)he looked at the glass for a long time.", "홀 씨가 문을 열었고, (c)그는 유리를 오랫동안 바라보았다."),
  ("Then the old man smiled at the boy and gave (d)him a brush.", "그러고 나서 노인은 소년에게 미소를 짓고 (d)그에게 빗자루를 주었다."),
  ("Ben swept the path, and (e)he paid for the window from his pocket money.", "벤은 길을 쓸었고, (e)그는 자기 용돈으로 창문 값을 냈다.")],
 ["공을 찬 사람은 벤이에요.", "사과하려고 문을 두드린 사람은 벤이에요.", "바로 앞의 '홀 씨가 문을 열었다'에 이어, 깨진 유리를 바라본 사람은 홀 씨예요.", "노인이 빗자루를 준 상대는 소년, 곧 벤이에요.", "용돈으로 창문 값을 낸 사람은 벤이에요."],
 "knock 두드리다 / sweep 쓸다 / pocket money 용돈")
item(7, 2, '수미', '진',
 [("Sumi could not understand fractions, and (a)she was afraid of the test on Friday.", "수미는 분수를 이해할 수 없었고, (a)그녀는 금요일 시험이 두려웠다."),
  ("Her older sister Jin offered to help (b)her after dinner.", "언니 진이 저녁을 먹은 뒤 (b)그녀를 도와주겠다고 했다."),
  ("Jin drew a pizza on paper because (c)she remembered learning it that way herself.", "진은 종이에 피자를 그렸는데, (c)그녀 자신이 그렇게 배웠던 것을 기억했기 때문이다."),
  ("Sumi looked at the slices, and suddenly (d)she understood.", "수미는 피자 조각들을 보았고, 갑자기 (d)그녀는 이해했다."),
  ("On Friday (e)she finished the test before anyone else.", "금요일에 (e)그녀는 누구보다 먼저 시험을 끝냈다.")],
 ["시험이 두려운 사람은 분수를 모르는 수미예요.", "진이 도와주겠다고 한 상대는 수미예요.", "피자를 그린 진이 '자신도 그렇게 배웠다'고 기억한 것이니, 진이에요.", "조각을 보고 이해한 사람은 수미예요.", "시험을 먼저 끝낸 사람은 수미예요."],
 "fraction 분수 / offer 해 주겠다고 하다 / slice 조각")
item(8, 3, '에번스 선생님', '톰',
 [("Mr. Evans had taught the school band for twenty years, and (a)he knew every piece by heart.", "에번스 선생님은 20년 동안 학교 밴드를 가르쳤고, (a)그는 모든 곡을 외우고 있었다."),
  ("One day (b)he noticed a new boy, Tom, who kept losing his place.", "어느 날 (b)그는 자꾸 연주할 곳을 놓치는 새 학생 톰을 알아보았다."),
  ("After practice (c)he asked the boy to stay.", "연습이 끝난 뒤 (c)그는 그 학생에게 남으라고 했다."),
  ("Tom was worried because (d)he thought he was in trouble.", "톰은 (d)그가 혼날 것이라고 생각해서 걱정했다."),
  ("But the teacher only smiled, and (e)he played each line slowly until Tom could follow.", "그러나 선생님은 미소만 지었고, (e)그는 톰이 따라올 수 있을 때까지 한 줄씩 천천히 연주했다.")],
 ["모든 곡을 외우는 사람은 20년 동안 가르친 에번스 선생님이에요.", "새 학생 톰을 알아본 사람은 선생님이에요.", "학생에게 남으라고 한 사람은 선생님이에요.", "걱정한 톰이 '자기가 혼날 것'이라고 생각한 것이니, 톰이에요.", "미소를 짓고 천천히 연주해 준 사람은 선생님이에요."],
 "by heart 외워서 / notice 알아보다 / be in trouble 혼나게 되다")
item(10, 3, '박 씨 아주머니', '나리',
 [("Mrs. Park has sold flowers at the market for thirty years, and (a)she knows most of her customers by name.", "박 씨 아주머니는 30년 동안 시장에서 꽃을 팔았고, (a)그녀는 손님 대부분의 이름을 안다."),
  ("Every Friday (b)she keeps the best roses for a girl called Nari.", "금요일마다 (b)그녀는 나리라는 소녀를 위해 가장 좋은 장미를 남겨 둔다."),
  ("(c)She has done so since the spring.", "(c)그녀는 봄부터 그렇게 해 왔다."),
  ("Nari buys them because (d)she visits her grandmother in hospital every Friday evening.", "나리는 (d)그녀가 금요일 저녁마다 병원에 계신 할머니를 찾아가기 때문에 그 장미를 산다."),
  ("Mrs. Park never asks questions, but (e)she always adds one extra flower.", "박 씨 아주머니는 아무것도 묻지 않지만, (e)그녀는 언제나 꽃 한 송이를 더 넣어 준다.")],
 ["손님의 이름을 아는 사람은 꽃을 파는 박 씨 아주머니예요.", "장미를 남겨 두는 사람은 박 씨 아주머니예요.", "봄부터 그렇게 해 온 사람은 박 씨 아주머니예요.", "장미를 사는 나리가 할머니를 찾아가는 것이니, 나리예요.", "꽃 한 송이를 더 넣어 주는 사람은 박 씨 아주머니예요."],
 "customer 손님 / visit 찾아가다 / extra 덤의")
item(11, 3, '지호', '최 씨',
 [("Jiho's bicycle chain broke on the way to school, so (a)he started to push the bike.", "지호의 자전거 체인이 학교 가는 길에 끊어져서, (a)그는 자전거를 밀기 시작했다."),
  ("(b)He was already late when he passed a small repair shop.", "(b)그는 작은 수리점을 지날 때 이미 늦어 있었다."),
  ("The owner, Mr. Choi, came out and looked at the chain for (c)him.", "주인인 최 씨가 나와서 (c)그를 위해 체인을 살펴보았다."),
  ("In two minutes the old man fixed it, and (d)he refused to take any money.", "2분 만에 노인은 그것을 고쳤고, (d)그는 돈을 한 푼도 받지 않으려 했다."),
  ("Jiho thanked him, and the next day (e)he brought a bag of apples to the shop.", "지호는 고맙다고 했고, 다음 날 (e)그는 사과 한 봉지를 가게에 가져왔다.")],
 ["자전거를 민 사람은 체인이 끊어진 지호예요.", "학교에 늦은 사람은 지호예요.", "최 씨가 체인을 살펴봐 준 상대는 지호예요.", "체인을 고친 노인이 돈을 받지 않으려 한 것이니, 최 씨예요.", "사과를 가져온 사람은 고마워한 지호예요."],
 "chain 체인 / repair 수리 / refuse 거절하다")
item(12, 3, '애나', '루시',
 [("Anna moved to a new town in March, and (a)she did not know anyone at school.", "애나는 3월에 새 동네로 이사했고, (a)그녀는 학교에 아는 사람이 없었다."),
  ("At lunch (b)she usually read a book by the window.", "점심시간에 (b)그녀는 보통 창가에서 책을 읽었다."),
  ("One day a girl named Lucy sat down beside (c)her.", "어느 날 루시라는 여자아이가 (c)그녀 옆에 앉았다."),
  ("Lucy pointed at the book because (d)she had read the same story twice.", "루시는 (d)그녀가 같은 이야기를 두 번 읽었기 때문에 그 책을 가리켰다."),
  ("The two girls talked until the bell rang, and Anna felt that (e)she had finally found a friend.", "두 아이는 종이 울릴 때까지 이야기했고, 애나는 (e)그녀가 마침내 친구를 찾았다고 느꼈다.")],
 ["아는 사람이 없던 사람은 이사 온 애나예요.", "창가에서 책을 읽은 사람은 애나예요.", "루시가 옆에 앉은 상대는 애나예요.", "책을 가리킨 루시가 '같은 이야기를 두 번 읽었다'는 것이니, 루시예요.", "친구를 찾았다고 느낀 사람은 애나예요."],
 "move 이사하다 / point at 가리키다 / finally 마침내")
item(14, 4, '민호', '아버지',
 [("Minho wanted to run in the school race, but (a)he was the slowest boy in his class.", "민호는 학교 달리기 대회에 나가고 싶었지만, (a)그는 반에서 가장 느린 아이였다."),
  ("Every morning (b)he ran around the park before breakfast.", "매일 아침 (b)그는 아침을 먹기 전에 공원을 한 바퀴 달렸다."),
  ("His father timed (c)him with an old watch.", "아버지는 낡은 시계로 (c)그의 기록을 쟀다."),
  ("On race day (d)he finished third and could hardly believe it.", "대회 날 (d)그는 3등으로 들어왔고 그것을 거의 믿을 수 없었다."),
  ("His father said nothing, but (e)he kept the old watch on the shelf beside the medal.", "아버지는 아무 말도 하지 않았지만, (e)그는 그 낡은 시계를 메달 옆 선반에 놓아 두었다.")],
 ["반에서 가장 느린 아이는 민호예요.", "아침마다 공원을 달린 사람은 민호예요.", "아버지가 기록을 재 준 상대는 민호예요.", "대회에서 3등을 한 사람은 민호예요.", "바로 앞의 '아버지는 아무 말도 하지 않았다'에 이어, 시계를 선반에 놓아 둔 사람은 아버지예요."],
 "race 달리기 대회 / time 시간을 재다 / hardly 거의 ~않다")
item(16, 4, '하나', '할머니',
 [("Hana's grandmother taught her to make kimchi last winter.", "하나의 할머니는 지난겨울 하나에게 김치 담그는 법을 가르쳐 주셨다."),
  ("At first (a)she cut the cabbage too small, and (b)she used far too much salt.", "처음에 (a)그녀는 배추를 너무 작게 썰었고, (b)그녀는 소금을 지나치게 많이 넣었다."),
  ("(c)She wanted to give up after the second try.", "(c)그녀는 두 번째 시도 뒤에 그만두고 싶었다."),
  ("But the old woman tasted it and told (d)her to try once more.", "그러나 할머니는 맛을 보고 (d)그녀에게 한 번만 더 해 보라고 하셨다."),
  ("This winter Hana made it alone, and her grandmother said (e)she could not tell the difference from her own.", "이번 겨울 하나는 혼자 김치를 담갔고, 할머니는 (e)그녀가 자신의 김치와 차이를 알 수 없다고 말씀하셨다.")],
 ["배추를 너무 작게 썬 사람은 배우는 하나예요.", "소금을 너무 많이 넣은 사람은 하나예요.", "그만두고 싶었던 사람은 하나예요.", "할머니가 한 번 더 해 보라고 한 상대는 하나예요.", "'자신의 김치와 차이를 알 수 없다'고 말한 사람은 맛을 본 할머니예요."],
 "cabbage 배추 / give up 그만두다 / difference 차이")
item(17, 4, '리오', '노인',
 [("Leo found a wallet on the bus when (a)he was going home.", "리오는 (a)그가 집에 가던 길에 버스에서 지갑을 발견했다."),
  ("(b)He saw an address inside and walked there, although it was far.", "(b)그는 안에서 주소를 보고, 멀었지만 그곳까지 걸어갔다."),
  ("An old man opened the door, and the boy told the man where (c)he had found it.", "한 노인이 문을 열었고, 소년은 (c)그가 그것을 어디서 발견했는지 노인에게 말했다."),
  ("The man offered money, but Leo shook his head because (d)he did not want any.", "노인은 돈을 주려 했지만, 리오는 (d)그가 돈을 바라지 않았기 때문에 고개를 저었다."),
  ("A week later a letter came to Leo's school because (e)he had written to thank the boy.", "일주일 뒤 리오의 학교로 편지 한 통이 왔는데, (e)그가 소년에게 고마움을 전하려고 쓴 것이었다.")],
 ["집에 가던 사람은 지갑을 발견한 리오예요.", "주소를 보고 걸어간 사람은 리오예요.", "지갑을 발견한 사람은 리오예요.", "돈을 바라지 않아 고개를 저은 사람은 리오예요.", "'소년에게 고마움을 전하려고' 편지를 쓴 사람은 지갑을 돌려받은 노인이에요."],
 "wallet 지갑 / address 주소 / offer 주려고 하다")
item(18, 0, '소라', '이모',
 [("Sora's aunt gave her an old camera because (a)she no longer used it.", "소라의 이모는 (a)그녀가 더는 쓰지 않아서 소라에게 낡은 카메라를 주었다."),
  ("Sora took it everywhere, and (b)she photographed the same tree every week.", "소라는 그것을 어디에나 들고 다녔고, (b)그녀는 매주 같은 나무를 찍었다."),
  ("At first (c)her pictures were dark and unclear.", "처음에 (c)그녀의 사진은 어둡고 흐릿했다."),
  ("Slowly (d)she learned how to use the light.", "천천히 (d)그녀는 빛을 쓰는 법을 익혔다."),
  ("By autumn (e)she had fifty pictures of one tree in four colours.", "가을이 되자 (e)그녀는 네 가지 색을 띤 한 나무의 사진 쉰 장을 갖게 되었다.")],
 ["카메라를 '더는 쓰지 않은' 사람은 그것을 준 이모예요.", "매주 같은 나무를 찍은 사람은 카메라를 받은 소라예요.", "사진이 어둡고 흐릿했던 사람은 소라예요.", "빛을 쓰는 법을 익힌 사람은 소라예요.", "사진 쉰 장을 갖게 된 사람은 소라예요."],
 "no longer 더는 ~않다 / photograph 사진을 찍다 / unclear 흐릿한")
item(20, 0, '준', '김 씨',
 [("Mr. Kim asked his son Jun to wash the car because (a)he had hurt his back.", "김 씨는 (a)그가 허리를 다쳤기 때문에 아들 준에게 세차를 부탁했다."),
  ("Jun did not want to do it, and (b)he worked slowly at first.", "준은 하고 싶지 않았고, (b)그는 처음에는 느릿느릿 일했다."),
  ("Then (c)he found an old coin under the seat.", "그러다 (c)그는 좌석 밑에서 오래된 동전을 발견했다."),
  ("(d)He cleaned it and showed it to his father that evening.", "(d)그는 그것을 닦아서 그날 저녁 아버지에게 보여 주었다."),
  ("Jun's father let him keep it, and (e)he still has it in his desk.", "준의 아버지는 그것을 가지라고 했고, (e)그는 지금도 그것을 책상 속에 가지고 있다.")],
 ["허리를 다쳐 세차를 부탁한 사람은 아버지 김 씨예요.", "느릿느릿 일한 사람은 하기 싫었던 준이에요.", "동전을 발견한 사람은 세차하던 준이에요.", "동전을 닦아 아버지에게 보여 준 사람은 준이에요.", "아버지가 가지라고 했으니, 동전을 가지고 있는 사람은 준이에요."],
 "hurt 다치다 / coin 동전 / seat 좌석")
item(21, 0, '에마', '이 씨 아주머니',
 [("Mrs. Lee lent her neighbour Emma a ladder because (a)she did not need it that week.", "이 씨 아주머니는 (a)그녀가 그 주에는 필요하지 않아서 이웃 에마에게 사다리를 빌려주었다."),
  ("Emma wanted to paint her kitchen, and (b)she started early on Saturday.", "에마는 부엌을 칠하고 싶었고, (b)그녀는 토요일에 일찍 시작했다."),
  ("By noon (c)she had finished two walls.", "정오까지 (c)그녀는 벽 두 면을 끝냈다."),
  ("Then (d)she noticed that the colour was much darker than the picture on the tin.", "그때 (d)그녀는 색이 통에 그려진 것보다 훨씬 어둡다는 것을 알아차렸다."),
  ("In the end (e)she liked the dark colour better.", "결국 (e)그녀는 그 어두운 색이 더 마음에 들었다.")],
 ["사다리가 '그 주에는 필요하지 않았던' 사람은 그것을 빌려준 이 씨 아주머니예요.", "토요일에 일찍 칠하기 시작한 사람은 에마예요.", "벽 두 면을 끝낸 사람은 에마예요.", "색이 어둡다는 것을 알아차린 사람은 칠하던 에마예요.", "어두운 색이 마음에 든 사람은 에마예요."],
 "lend 빌려주다 / ladder 사다리 / tin 통")
item(22, 0, '샘', '제빵사',
 [("The baker gave Sam a job on Saturdays because (a)he needed help in the early morning.", "제빵사는 (a)그가 이른 아침에 일손이 필요했기 때문에 샘에게 토요일 일자리를 주었다."),
  ("Sam got up at five, and (b)he swept the floor before the shop opened.", "샘은 다섯 시에 일어났고, (b)그는 가게가 문을 열기 전에 바닥을 쓸었다."),
  ("In the first month (c)he burned two trays of bread.", "첫 달에 (c)그는 빵 두 판을 태웠다."),
  ("Sam was sure the baker would be angry with (d)him.", "샘은 제빵사가 (d)그에게 화를 낼 것이라고 확신했다."),
  ("But the old man only laughed, and Sam decided that (e)he would stay.", "그러나 노인은 웃기만 했고, 샘은 (e)그가 계속 일하기로 마음먹었다.")],
 ["이른 아침에 일손이 필요한 사람은 일자리를 준 제빵사예요.", "바닥을 쓴 사람은 다섯 시에 일어난 샘이에요.", "빵을 태운 사람은 일을 배우던 샘이에요.", "제빵사가 화를 낼 상대는 빵을 태운 샘이에요.", "계속 일하기로 마음먹은 사람은 샘이에요."],
 "baker 제빵사 / tray 판 / decide 마음먹다")
item(23, 0, '미나', '선생님',
 [("Mina's teacher gave her a notebook because (a)she had seen the girl writing stories on scraps of paper.", "미나의 선생님은 (a)그녀가 그 아이가 종이 쪼가리에 이야기를 쓰는 것을 보았기 때문에 미나에게 공책을 주었다."),
  ("Mina was surprised, and (b)she filled the first page that night.", "미나는 놀랐고, (b)그녀는 그날 밤 첫 쪽을 채웠다."),
  ("Every week (c)she wrote one more story.", "매주 (c)그녀는 이야기를 한 편씩 더 썼다."),
  ("At the end of the year (d)she had forty of them.", "한 해가 끝날 무렵 (d)그녀는 마흔 편을 갖게 되었다."),
  ("The teacher read every one and returned the notebook to (e)her with a short note.", "선생님은 한 편도 빠짐없이 읽고 짧은 쪽지와 함께 공책을 (e)그녀에게 돌려주었다.")],
 ["'그 아이가 이야기를 쓰는 것을 본' 사람은 공책을 준 선생님이에요.", "그날 밤 첫 쪽을 채운 사람은 공책을 받은 미나예요.", "매주 이야기를 쓴 사람은 미나예요.", "이야기 마흔 편을 갖게 된 사람은 미나예요.", "선생님이 공책을 돌려준 상대는 미나예요."],
 "scrap 쪼가리 / fill 채우다 / return 돌려주다")
item(24, 1, '댄', '마크',
 [("Dan was afraid of the water, so (a)he stood at the edge of the pool.", "댄은 물이 무서워서 (a)그는 수영장 가장자리에 서 있었다."),
  ("His older brother Mark was already swimming, and (b)he called out that it was not deep.", "형 마크는 벌써 헤엄치고 있었고, (b)그는 깊지 않다고 소리쳤다."),
  ("Dan put one foot in because (c)he did not want to look scared.", "댄은 (c)그가 겁먹은 것처럼 보이고 싶지 않아서 한 발을 넣었다."),
  ("Slowly (d)he walked in up to his chest.", "천천히 (d)그는 가슴 높이까지 걸어 들어갔다."),
  ("By the end of summer (e)he could swim across the pool.", "여름이 끝날 무렵 (e)그는 수영장을 헤엄쳐 건널 수 있었다.")],
 ["가장자리에 서 있던 사람은 물이 무서운 댄이에요.", "바로 앞의 '형 마크는 벌써 헤엄치고 있었다'에 이어, 깊지 않다고 소리친 사람은 마크예요.", "겁먹은 것처럼 보이고 싶지 않았던 사람은 발을 넣은 댄이에요.", "가슴 높이까지 걸어 들어간 사람은 댄이에요.", "여름 끝에 헤엄쳐 건너게 된 사람은 댄이에요."],
 "edge 가장자리 / deep 깊은 / scared 겁먹은")
item(26, 1, '지수', '윤 씨 아주머니',
 [("Jisu wanted a dog, but (a)she lived in a small flat.", "지수는 개를 기르고 싶었지만, (a)그녀는 작은 아파트에 살았다."),
  ("Her neighbour Mrs. Yoon had an old dog, and (b)she could not walk it far any more.", "이웃 윤 씨 아주머니에게는 늙은 개가 있었는데, (b)그녀는 이제 개를 멀리 산책시킬 수 없었다."),
  ("So Jisu offered to help, and (c)she took the dog out every evening.", "그래서 지수가 돕겠다고 했고, (c)그녀는 저녁마다 개를 데리고 나갔다."),
  ("(d)She learned to carry water and a small bag.", "(d)그녀는 물과 작은 봉지를 챙기는 법을 익혔다."),
  ("Now the dog waits at the door for (e)her at six o'clock.", "이제 그 개는 여섯 시가 되면 문 앞에서 (e)그녀를 기다린다.")],
 ["작은 아파트에 사는 사람은 개를 기르고 싶던 지수예요.", "바로 앞의 '윤 씨 아주머니에게는 늙은 개가 있었다'에 이어, 개를 멀리 산책시킬 수 없는 사람은 윤 씨 아주머니예요.", "저녁마다 개를 데리고 나간 사람은 돕겠다고 한 지수예요.", "물과 봉지를 챙기는 법을 익힌 사람은 지수예요.", "개가 여섯 시에 기다리는 사람은 산책시켜 주는 지수예요."],
 "flat 아파트 / neighbour 이웃 / offer 해 주겠다고 하다")
item(27, 1, '피터', '버스 기사',
 [("Peter could not find his way in the new city, and (a)he had no map on his phone.", "피터는 낯선 도시에서 길을 찾을 수 없었고, (a)그는 전화기에 지도도 없었다."),
  ("A bus driver saw the boy at the stop, and (b)he asked where the boy wanted to go.", "한 버스 기사가 정류장에 있는 소년을 보았고, (b)그는 소년이 어디로 가고 싶은지 물었다."),
  ("Peter showed the address that (c)he had written on his hand.", "피터는 (c)그가 손에 적어 둔 주소를 보여 주었다."),
  ("The driver pointed to the next street, so (d)he walked there.", "기사가 다음 길을 가리켜서 (d)그는 그곳으로 걸어갔다."),
  ("In five minutes (e)he was standing in front of his uncle's house.", "5분 뒤 (e)그는 삼촌 집 앞에 서 있었다.")],
 ["지도가 없던 사람은 길을 잃은 피터예요.", "'소년이 어디로 가고 싶은지' 물은 사람은 소년을 본 버스 기사예요.", "손에 주소를 적어 둔 사람은 그것을 보여 준 피터예요.", "기사가 가리킨 길로 걸어간 사람은 피터예요.", "삼촌 집 앞에 선 사람은 피터예요."],
 "map 지도 / address 주소 / point to 가리키다")
item(29, 1, '은지', '한 선생님',
 [("Eunji practised the piano every day, but (a)she always made mistakes in the same place.", "은지는 날마다 피아노를 연습했지만, (a)그녀는 늘 같은 곳에서 틀렸다."),
  ("Her teacher Mrs. Han listened carefully, and (b)she marked two notes with a pencil.", "한 선생님이 주의 깊게 들었고, (b)그녀는 연필로 음표 두 개에 표시를 했다."),
  ("Eunji played only those two notes because (c)she was told to repeat them ten times.", "은지는 (c)그녀가 그것을 열 번 되풀이하라는 말을 들었기 때문에 그 두 음만 연주했다."),
  ("Then (d)she played the whole line without a mistake.", "그러고 나서 (d)그녀는 한 줄 전체를 틀리지 않고 연주했다."),
  ("That evening (e)she played it for her parents.", "그날 저녁 (e)그녀는 부모님께 그것을 연주해 드렸다.")],
 ["같은 곳에서 틀린 사람은 연습하던 은지예요.", "바로 앞의 '한 선생님이 주의 깊게 들었다'에 이어, 음표에 표시를 한 사람은 한 선생님이에요.", "열 번 되풀이하라는 말을 들은 사람은 배우는 은지예요.", "한 줄을 틀리지 않고 연주한 사람은 은지예요.", "부모님께 연주해 드린 사람은 은지예요."],
 "practise 연습하다 / note 음표 / repeat 되풀이하다")

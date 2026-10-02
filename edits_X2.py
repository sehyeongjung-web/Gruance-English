# 164번: 선생님 승인("승인합니다") 반영
AUTO_SYNC = True
E = {}

# (1) 29번 레벨8 30번째 — 지문의 번호 ②가 묻는 낱말(inserted) 뒤에 붙어 있던 것을 앞으로 옮김 (지문 수정 · 승인)
E[('29','8',29)] = {'passage_ok': True, 'text': ('A patch inserted ②without disturbing', 'A patch ②inserted without disturbing')}

# (2) 23번 레벨4 — 30문항에 하나씩 들어 있던 '글과 관계없는 엉뚱한 소재' 오답을 지문과 같은 소재의 오답으로 교체 (승인)
E[('23','4',0)] = {'ch': {1: 'what yawning does for the brain and the body'}, 'cn': {1: "'what yawning does for the brain and the body' (하품이 뇌와 몸에 하는 일) — 하품의 기능은 글에 나오지 않습니다. 글은 하품이 옮는 현상을 다룹니다."}}
E[('23','4',1)] = {'ch': {0: 'which remedies cure hiccups most quickly of all'}, 'cn': {0: "'which remedies cure hiccups most quickly of all' (딸꾹질을 가장 빨리 멎게 하는 방법) — 글은 민간요법이 모두 호흡을 끊는 원리라는 점을 말할 뿐, 어느 것이 빠른지는 다루지 않습니다."}}
E[('23','4',2)] = {'ch': {0: 'why a sneeze is louder in some people'}, 'cn': {0: "'why a sneeze is louder in some people' (어떤 사람의 재채기 소리가 더 큰 이유) — 재채기 소리의 크기는 글에 나오지 않습니다."}}
E[('23','4',3)] = {'ch': {0: 'why humans no longer have a thick coat of hair'}, 'cn': {0: "'why humans no longer have a thick coat of hair' (사람에게 두꺼운 털이 더는 없는 이유) — 털이 없어진 이유는 다루지 않습니다. 털을 세우는 근육이 추위와 음악에 똑같이 반응한다는 글입니다."}}
E[('23','4',4)] = {'ch': {0: 'why the eyes water more on a cold windy day'}, 'cn': {0: "'why the eyes water more on a cold windy day' (춥고 바람 부는 날 눈물이 더 나는 이유) — 날씨 이야기는 글에 나오지 않습니다."}}
E[('23','4',5)] = {'ch': {0: 'how textbooks are checked before printing'}, 'cn': {0: "'how textbooks are checked before printing' (교과서가 인쇄 전에 검토되는 방법) — 교과서는 틀린 그림이 실렸던 곳으로 나올 뿐입니다."}}
E[('23','4',6)] = {'ch': {1: 'how thick soles protect the feet outdoors'}, 'cn': {1: "'how thick soles protect the feet outdoors' (두꺼운 밑창이 밖에서 발을 보호하는 방법) — 글은 오히려 두꺼운 밑창이 균형을 해친다고 합니다."}}
E[('23','4',7)] = {'ch': {0: 'how swallowing helps food go down'}, 'cn': {0: "'how swallowing helps food go down' (삼키는 동작이 음식을 내려보내는 방법) — 삼키기는 관을 여는 방법으로 나올 뿐입니다."}}
E[('23','4',8)] = {'ch': {0: 'why wet objects are hard to hold'}, 'cn': {0: "'why wet objects are hard to hold' (젖은 물건을 쥐기 어려운 이유) — 쥐는 힘은 주름의 효과로 덧붙인 내용일 뿐, 글의 중심은 주름이 생기는 까닭입니다."}}
E[('23','4',9)] = {'ch': {0: 'why chilled drinks are bad for the heart'}, 'cn': {0: "'why chilled drinks are bad for the heart' (찬 음료가 심장에 해로운 이유) — 찬 음료와 심장은 서로 다른 예로 나올 뿐, 둘을 잇는 내용은 없습니다."}}
E[('23','4',10)] = {'ch': {0: 'how sight and sound are sorted by the brain'}, 'cn': {0: "'how sight and sound are sorted by the brain' (뇌가 시각과 청각을 분류하는 방법) — 시각과 청각은 후각과 대비하려고 나올 뿐입니다."}}
E[('23','4',11)] = {'ch': {1: 'how volunteers are chosen for sleep studies'}, 'cn': {1: "'how volunteers are chosen for sleep studies' (수면 연구의 지원자를 뽑는 방법) — 지원자는 실험 대상으로 나올 뿐입니다."}}
E[('23','4',12)] = {'ch': {0: 'how bicycles have changed in twenty years'}, 'cn': {0: "'how bicycles have changed in twenty years' (20년 동안 자전거가 변해 온 모습) — 자전거는 몸에 밴 동작의 예로 나올 뿐입니다."}}
E[('23','4',13)] = {'ch': {0: 'why the spinal cord is protected by the backbone'}, 'cn': {0: "'why the spinal cord is protected by the backbone' (척수가 등뼈의 보호를 받는 이유) — 등뼈 이야기는 글에 나오지 않습니다."}}
E[('23','4',14)] = {'ch': {0: 'which thermometer gives the fastest reading'}, 'cn': {0: "'which thermometer gives the fastest reading' (가장 빨리 재는 체온계) — 체온계의 종류는 글에 나오지 않습니다."}}
E[('23','4',15)] = {'ch': {0: 'how the brain stores what the eyes see'}, 'cn': {0: "'how the brain stores what the eyes see' (눈이 본 것을 뇌가 저장하는 방법) — 저장이 아니라 깜박이는 동안의 처리를 말하는 글입니다."}}
E[('23','4',16)] = {'ch': {0: 'why one ear hears better than the other'}, 'cn': {0: "'why one ear hears better than the other' (한쪽 귀가 다른 쪽보다 잘 듣는 이유) — 한쪽 귀가 더 잘 듣는다는 말은 없습니다. 두 귀에 닿는 차이를 뇌가 비교한다는 글입니다."}}
E[('23','4',17)] = {'ch': {0: 'how an empty stomach signals the brain'}, 'cn': {0: "'how an empty stomach signals the brain' (빈 위가 뇌에 신호를 보내는 방법) — 글은 배고픔이 빈 위가 아니라 호르몬에서 온다고 합니다."}}
E[('23','4',18)] = {'ch': {0: 'how artists learn to draw straight lines'}, 'cn': {0: "'how artists learn to draw straight lines' (화가가 직선 그리기를 배우는 방법) — 그리는 방법은 글에 나오지 않습니다."}}
E[('23','4',19)] = {'ch': {0: 'how cave paintings were made long ago'}, 'cn': {0: "'how cave paintings were made long ago' (오래전 동굴 벽화가 만들어진 방법) — 동굴 벽화는 증거로 나올 뿐입니다."}}
E[('23','4',20)] = {'ch': {0: 'how bacteria on the skin cause illness'}, 'cn': {0: "'how bacteria on the skin cause illness' (피부의 세균이 병을 일으키는 방법) — 세균은 냄새의 원인으로 나올 뿐, 병 이야기는 없습니다."}}
E[('23','4',21)] = {'ch': {0: 'how the inner ear helps people to hear'}, 'cn': {0: "'how the inner ear helps people to hear' (속귀가 듣는 데 하는 일) — 듣기가 아니라 회전 감각을 다루는 글입니다."}}
E[('23','4',22)] = {'ch': {0: 'why blood is red inside the body'}, 'cn': {0: "'why blood is red inside the body' (몸속의 피가 붉은 이유) — 피의 색 자체는 다루지 않습니다. 멍의 색이 바뀌는 까닭을 말하는 글입니다."}}
E[('23','4',23)] = {'ch': {0: 'how warm clothes keep in body heat'}, 'cn': {0: "'how warm clothes keep in body heat' (따뜻한 옷이 체온을 지키는 방법) — 옷 이야기는 글에 나오지 않습니다."}}
E[('23','4',24)] = {'ch': {1: 'how recording machines capture the human voice'}, 'cn': {1: "'how recording machines capture the human voice' (녹음기가 사람 목소리를 담는 방법) — 녹음 방식은 글에 나오지 않습니다."}}
E[('23','4',25)] = {'ch': {0: 'why people run more slowly in their dreams'}, 'cn': {0: "'why people run more slowly in their dreams' (꿈속에서 더 느리게 달리는 이유) — 달리기는 꿈의 예로 나올 뿐입니다."}}
E[('23','4',26)] = {'ch': {1: 'how sugar harms the teeth of children'}, 'cn': {1: "'how sugar harms the teeth of children' (설탕이 아이의 이를 해치는 방법) — 이(치아) 이야기는 글에 나오지 않습니다."}}
E[('23','4',27)] = {'ch': {0: 'how windows let more light into a room'}, 'cn': {0: "'how windows let more light into a room' (창문이 방에 빛을 더 들이는 방법) — 창문은 멀리 보는 방법으로 나올 뿐입니다."}}
E[('23','4',28)] = {'ch': {1: 'why closing the eyes helps people rest'}, 'cn': {1: "'why closing the eyes helps people rest' (눈을 감으면 쉬는 데 도움이 되는 이유) — 눈 감기는 균형이 어려워지는 예로 나올 뿐입니다."}}
E[('23','4',29)] = {'ch': {0: 'how long a medical procedure should last'}, 'cn': {0: "'how long a medical procedure should last' (시술이 얼마나 오래 이어져야 하는가) — 글은 길이가 거의 기억되지 않는다고 할 뿐, 알맞은 길이는 다루지 않습니다."}}

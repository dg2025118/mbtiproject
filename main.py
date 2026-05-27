import streamlit as st
import requests
import time
import random

# ─────────────────────────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="⚡ MBTI 포켓몬 퀴즈",
    page_icon="🎮",
    layout="centered"
)

# ─────────────────────────────────────────────────────────────
# CSS 스타일
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

* { font-family: 'Jua', sans-serif !important; }

body {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
}

.main-title {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 25px;
    padding: 35px;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 20px 60px rgba(102,126,234,0.4);
    border: 2px solid rgba(255,255,255,0.2);
}

.question-card {
    background: linear-gradient(135deg, #ffffff 0%, #f0f4ff 100%);
    border-radius: 20px;
    padding: 30px;
    margin: 15px 0;
    box-shadow: 0 10px 40px rgba(0,0,0,0.15);
    border-left: 6px solid #667eea;
}

.progress-bar-container {
    background: rgba(255,255,255,0.2);
    border-radius: 50px;
    padding: 5px;
    margin: 15px 0;
}

.result-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8f0ff 100%);
    border-radius: 25px;
    padding: 35px;
    text-align: center;
    box-shadow: 0 20px 60px rgba(0,0,0,0.2);
    border: 3px solid #e8d5ff;
    margin: 10px 0;
}

.reason-box {
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
    border-radius: 18px;
    padding: 22px;
    margin: 15px 0;
    border-left: 6px solid #ff8c69;
}

.trait-box {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    border-radius: 18px;
    padding: 22px;
    margin: 15px 0;
}

.fun-fact-box {
    background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
    border-radius: 18px;
    padding: 22px;
    margin: 15px 0;
    border-left: 6px solid #52c234;
}

.score-box {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    border-radius: 18px;
    padding: 22px;
    margin: 15px 0;
    color: white;
    text-align: center;
}

.option-selected {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    transform: scale(1.02);
}

.intro-box {
    background: linear-gradient(135deg, #f5f7fa 0%, #e8ecff 100%);
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    margin: 15px 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 15px;
    padding: 12px 25px;
    font-size: 1.05em;
    font-weight: bold;
    width: 100%;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 5px 20px rgba(102,126,234,0.35);
    font-family: 'Jua', sans-serif !important;
    margin: 4px 0;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 28px rgba(102,126,234,0.5);
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
}

.stButton > button:active {
    transform: scale(0.98);
}

.mbti-badge {
    display: inline-block;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 10px 28px;
    border-radius: 50px;
    font-size: 1.5em;
    font-weight: bold;
    margin: 10px;
    box-shadow: 0 4px 18px rgba(102,126,234,0.45);
}

.type-badge {
    display: inline-block;
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 0.95em;
    margin: 4px;
    color: white;
    font-weight: bold;
    box-shadow: 0 3px 10px rgba(0,0,0,0.2);
}

.answer-feedback {
    border-radius: 15px;
    padding: 18px;
    margin: 10px 0;
    font-size: 1.1em;
    text-align: center;
    font-weight: bold;
}

.quiz-number {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border-radius: 50%;
    width: 38px;
    height: 38px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 1em;
    font-weight: bold;
    margin-right: 10px;
}

.footer {
    text-align: center;
    padding: 25px;
    color: #999;
    font-size: 0.85em;
    margin-top: 20px;
}

.shimmer {
    animation: shimmer 2s infinite;
}

@keyframes shimmer {
    0% { opacity: 1; }
    50% { opacity: 0.6; }
    100% { opacity: 1; }
}

.star-rating {
    font-size: 2em;
    text-align: center;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# MBTI별 포켓몬 데이터
# ─────────────────────────────────────────────────────────────
MBTI_POKEMON = {
    "INTJ": {
        "name": "뮤츠",
        "english_name": "mewtwo",
        "emoji": "🧠",
        "reason": "혼자서도 강력하고, 치밀한 전략가! 감정보다 논리를 중시하며 자신만의 세계를 구축하는 당신은 뮤츠입니다.",
        "traits": ["🎯 완벽주의자", "🔬 분석적 사고", "🏆 독립적", "💡 전략가"],
        "fun_fact": "뮤츠는 과학으로 탄생한 포켓몬으로, 압도적인 지능과 실력을 자랑해요! INTJ처럼 계획적이고 강렬하죠.",
        "type_color": {"에스퍼": "#FF6B9D"},
        "mbti_desc": "용의주도한 전략가 ♟️",
        "rarity": "⭐⭐⭐⭐⭐ 전설등급",
        "battle_style": "🧠 두뇌 플레이형"
    },
    "INTP": {
        "name": "포리곤",
        "english_name": "porygon",
        "emoji": "💻",
        "reason": "디지털 세계를 탐험하는 분석가! 끊임없이 지식을 탐구하고 새로운 이론을 발견하는 당신은 포리곤입니다.",
        "traits": ["🔍 탐구적", "🧩 논리적", "💭 창의적 사고", "📚 지식 탐험가"],
        "fun_fact": "포리곤은 완전히 프로그래밍으로 만들어진 최초의 포켓몬이에요! 끊임없이 진화하는 모습이 INTP와 닮았죠.",
        "type_color": {"노말": "#A8A878"},
        "mbti_desc": "논리적인 사색가 🔭",
        "rarity": "⭐⭐⭐⭐ 희귀등급",
        "battle_style": "💡 분석 계산형"
    },
    "ENTJ": {
        "name": "리자몽",
        "english_name": "charizard",
        "emoji": "🔥",
        "reason": "타오르는 카리스마로 모두를 이끄는 리더! 목표를 향해 불꽃처럼 돌진하는 당신은 리자몽입니다.",
        "traits": ["👑 천생 리더", "🔥 강한 의지", "⚡ 결단력", "🎖️ 야망가"],
        "fun_fact": "리자몽은 강한 상대와의 싸움을 즐기는 포켓몬이에요! ENTJ처럼 도전을 두려워하지 않는 불굴의 정신을 가졌죠.",
        "type_color": {"불꽃": "#F08030", "비행": "#6890F0"},
        "mbti_desc": "대담한 통솔자 🦁",
        "rarity": "⭐⭐⭐⭐⭐ 전설등급",
        "battle_style": "🔥 압도적 공격형"
    },
    "ENTP": {
        "name": "개굴닌자",
        "english_name": "greninja",
        "emoji": "🌊",
        "reason": "재치와 아이디어로 상황을 뒤집는 토론가! 항상 새로운 방식으로 문제를 해결하는 당신은 개굴닌자입니다.",
        "traits": ["💬 토론왕", "⚡ 빠른 두뇌", "🎭 유머러스", "🆕 혁신가"],
        "fun_fact": "개굴닌자는 순식간에 물 수리검을 만들어 공격하는 창의적인 전술가에요! ENTP처럼 즉흥적이면서도 천재적이죠.",
        "type_color": {"물": "#6890F0", "악": "#705848"},
        "mbti_desc": "논쟁을 즐기는 변론가 ⚡",
        "rarity": "⭐⭐⭐⭐ 희귀등급",
        "battle_style": "💨 스피드 기습형"
    },
    "INFJ": {
        "name": "루기아",
        "english_name": "lugia",
        "emoji": "🌙",
        "reason": "깊은 내면과 숭고한 이상을 가진 선지자! 세상을 더 나은 곳으로 만들고 싶은 당신은 루기아입니다.",
        "traits": ["🌟 이상주의자", "💞 공감 능력", "🔮 통찰력", "🕊️ 평화주의"],
        "fun_fact": "루기아는 바다의 수호자로 강한 힘을 가지고 있지만 조용히 숨어사는 포켓몬이에요! INFJ의 조용한 영향력과 닮았죠.",
        "type_color": {"에스퍼": "#FF6B9D", "비행": "#6890F0"},
        "mbti_desc": "통찰력 있는 선지자 🔮",
        "rarity": "⭐⭐⭐⭐⭐ 전설등급",
        "battle_style": "🌊 신비로운 수호형"
    },
    "INFP": {
        "name": "이브이",
        "english_name": "eevee",
        "emoji": "🌸",
        "reason": "무한한 가능성과 풍부한 감수성을 가진 중재자! 자신만의 가치관을 소중히 여기는 당신은 이브이입니다.",
        "traits": ["🎨 풍부한 감성", "🌈 무한한 가능성", "💝 따뜻한 마음", "🦋 자유로운 영혼"],
        "fun_fact": "이브이는 8가지 진화형을 가진 특별한 포켓몬이에요! INFP처럼 어떤 방향으로든 성장할 수 있는 무한한 잠재력을 가졌죠.",
        "type_color": {"노말": "#A8A878"},
        "mbti_desc": "열정적인 중재자 🌸",
        "rarity": "⭐⭐⭐⭐ 희귀등급",
        "battle_style": "🌸 감성 전략형"
    },
    "ENFJ": {
        "name": "뮤",
        "english_name": "mew",
        "emoji": "✨",
        "reason": "모두를 사랑하고 이끄는 선도자! 타인의 성장을 진심으로 응원하는 당신은 뮤입니다.",
        "traits": ["🤝 사교적", "💖 이타적", "🌟 영감을 주는", "🎯 목표 지향적"],
        "fun_fact": "뮤는 모든 포켓몬의 DNA를 가진 전설의 포켓몬이에요! ENFJ처럼 누구와도 잘 어울리고 모두를 품을 수 있죠.",
        "type_color": {"에스퍼": "#FF6B9D"},
        "mbti_desc": "정의로운 사회운동가 🌟",
        "rarity": "⭐⭐⭐⭐⭐ 환상등급",
        "battle_style": "✨ 올라운드 만능형"
    },
    "ENFP": {
        "name": "파치리스",
        "english_name": "pachirisu",
        "emoji": "⚡",
        "reason": "넘치는 에너지와 긍정으로 주변을 밝히는 활동가! 호기심 많고 열정적인 당신은 파치리스입니다.",
        "traits": ["🎉 활기차고 명랑", "💫 창의적", "🌈 낙천적", "🤗 사교적"],
        "fun_fact": "파치리스는 항상 활발하게 뛰어다니는 에너지 넘치는 포켓몬이에요! ENFP처럼 어디서든 분위기를 밝게 만들죠.",
        "type_color": {"전기": "#F8D030"},
        "mbti_desc": "재기발랄한 활동가 🎊",
        "rarity": "⭐⭐⭐ 일반등급",
        "battle_style": "⚡ 스파크 에너지형"
    },
    "ISTJ": {
        "name": "두두",
        "english_name": "doduo",
        "emoji": "📋",
        "reason": "책임감 강하고 신뢰할 수 있는 현실주의자! 맡은 일을 끝까지 해내는 당신은 두두입니다.",
        "traits": ["✅ 책임감", "📌 꼼꼼함", "🏛️ 전통 중시", "🔐 신뢰할 수 있는"],
        "fun_fact": "두두는 날지 못하지만 엄청난 속도로 달리는 포켓몬이에요! ISTJ처럼 꾸준하고 성실하게 자신의 방식을 지켜나가죠.",
        "type_color": {"노말": "#A8A878", "비행": "#6890F0"},
        "mbti_desc": "청렴결백한 논리주의자 📐",
        "rarity": "⭐⭐⭐ 일반등급",
        "battle_style": "🛡️ 철벽 수비형"
    },
    "ISFJ": {
        "name": "치코리타",
        "english_name": "chikorita",
        "emoji": "🌿",
        "reason": "따뜻하고 헌신적인 수호자! 소중한 사람들을 위해 조용히 곁을 지키는 당신은 치코리타입니다.",
        "traits": ["🤲 헌신적", "🌱 배려심", "🏠 안정 추구", "💚 따뜻한 마음"],
        "fun_fact": "치코리타는 달콤한 향기로 주변을 치유하는 포켓몬이에요! ISFJ처럼 말없이 주변 사람들을 돌보는 따뜻한 존재죠.",
        "type_color": {"풀": "#78C850"},
        "mbti_desc": "용감한 수호자 🛡️",
        "rarity": "⭐⭐⭐ 일반등급",
        "battle_style": "💚 힐링 서포트형"
    },
    "ESTJ": {
        "name": "갸라도스",
        "english_name": "gyarados",
        "emoji": "💪",
        "reason": "강력한 실행력과 리더십으로 조직을 이끄는 경영자! 목표를 향해 거침없이 나아가는 당신은 갸라도스입니다.",
        "traits": ["👔 강한 리더십", "⚡ 결단력", "📊 체계적", "🎯 목표 지향"],
        "fun_fact": "갸라도스는 연약한 잉어킹에서 엄청난 포켓몬으로 진화해요! ESTJ처럼 끊임없는 노력으로 최고의 자리에 오르죠.",
        "type_color": {"물": "#6890F0", "비행": "#6890F0"},
        "mbti_desc": "엄격한 관리자 📊",
        "rarity": "⭐⭐⭐⭐ 희귀등급",
        "battle_style": "💪 강력 돌파형"
    },
    "ESFJ": {
        "name": "푸린",
        "english_name": "jigglypuff",
        "emoji": "🎤",
        "reason": "모두를 행복하게 만드는 사교적인 외교관! 언제나 주변을 즐겁게 해주는 당신은 푸린입니다.",
        "traits": ["🎵 사교적", "💕 다정함", "🤝 협력적", "🎉 분위기 메이커"],
        "fun_fact": "푸린은 노래로 모두를 즐겁게 해주는 포켓몬이에요! ESFJ처럼 자신의 재능으로 주변을 행복하게 만들죠.",
        "type_color": {"노말": "#A8A878", "페어리": "#EE99AC"},
        "mbti_desc": "사교적인 외교관 🎊",
        "rarity": "⭐⭐⭐ 일반등급",
        "battle_style": "🎵 매력 지원형"
    },
    "ISTP": {
        "name": "팬텀",
        "english_name": "haunter",
        "emoji": "🔧",
        "reason": "조용하지만 놀라운 실력을 가진 만능 재주꾼! 혼자서 모든 것을 해결하는 당신은 팬텀입니다.",
        "traits": ["🔩 실용적", "🎭 관찰력", "⚡ 위기 대응", "🤫 독립적"],
        "fun_fact": "팬텀은 조용히 관찰하다가 갑자기 나타나 상황을 반전시키는 포켓몬이에요! ISTP처럼 언제나 예상치 못한 해결책을 가지고 있죠.",
        "type_color": {"고스트": "#705898", "독": "#A040A0"},
        "mbti_desc": "대담한 탐험가 🔧",
        "rarity": "⭐⭐⭐ 일반등급",
        "battle_style": "👻 암습 기습형"
    },
    "ISFP": {
        "name": "뮨",
        "english_name": "mime-jr",
        "emoji": "🎨",
        "reason": "자유롭고 예술적인 영혼을 가진 모험가! 순간을 소중히 여기는 감성적인 당신은 뮨입니다.",
        "traits": ["🎨 예술적", "🌸 감성적", "🌿 자연 친화", "💃 자유로운"],
        "fun_fact": "뮨은 흉내내기의 달인으로 표현력이 풍부한 포켓몬이에요! ISFP처럼 자신만의 독특한 방식으로 세상을 표현하죠.",
        "type_color": {"에스퍼": "#FF6B9D"},
        "mbti_desc": "호기심 많은 예술가 🎨",
        "rarity": "⭐⭐⭐ 일반등급",
        "battle_style": "🎭 변칙 표현형"
    },
    "ESTP": {
        "name": "잠만보",
        "english_name": "snorlax",
        "emoji": "🌪️",
        "reason": "현실적이고 활동적인 사업가! 눈앞의 상황에 즉각 반응하는 당신은 먹을 것 앞에서만큼은 누구보다 빠른 잠만보입니다! 😄",
        "traits": ["💨 즉흥적", "😎 여유로움", "💪 강인함", "🎯 현실주의"],
        "fun_fact": "잠만보는 평소엔 여유롭지만 먹을 것 앞에서는 누구보다 빠르게 행동하는 포켓몬이에요! ESTP처럼 필요할 때 폭발적인 에너지를 발휘하죠.",
        "type_color": {"노말": "#A8A878"},
        "mbti_desc": "모험을 즐기는 사업가 🌪️",
        "rarity": "⭐⭐⭐ 일반등급",
        "battle_style": "💥 파워 압박형"
    },
    "ESFP": {
        "name": "피카츄",
        "english_name": "pikachu",
        "emoji": "⚡",
        "reason": "세상에서 가장 유명하고 사랑받는 연예인! 항상 밝고 에너지 넘치는 당신은 피카츄입니다!",
        "traits": ["🌟 스타 기질", "💛 사랑스러운", "🎉 활기차고 재미있는", "🤸 자유분방"],
        "fun_fact": "피카츄는 전 세계에서 가장 사랑받는 포켓몬이에요! ESFP처럼 어디서든 빛나고 모두에게 사랑받는 천생 연예인이죠.",
        "type_color": {"전기": "#F8D030"},
        "mbti_desc": "자유로운 연예인 🌟",
        "rarity": "⭐⭐⭐⭐⭐ 인기등급",
        "battle_style": "⚡ 번개 쇼맨형"
    },
}

# ─────────────────────────────────────────────────────────────
# 퀴즈 문항 데이터 (12문항, 각 4개 선택지 → MBTI 4개 축 측정)
# E/I, S/N, T/F, J/P 각 3문항씩
# ─────────────────────────────────────────────────────────────
QUESTIONS = [
    # ── E vs I ──
    {
        "id": 1,
        "category": "EI",
        "emoji": "🎉",
        "question": "포켓몬 배틀 대회 날! 당신의 모습은?",
        "options": [
            {"text": "🙋 먼저 다가가서 라이벌들과 수다 떨기! 친구 100명 만들기 도전!", "score": {"E": 2}},
            {"text": "😊 말 걸면 친절하게 대화하지만, 먼저 나서진 않아요", "score": {"E": 1, "I": 1}},
            {"text": "🎧 이어폰 끼고 배틀 전략 복습 중... 방해하지 마세요", "score": {"I": 1}},
            {"text": "🏠 집에서 혼자 훈련하는 게 훨씬 좋았는데... 왜 나온 거지?", "score": {"I": 2}},
        ]
    },
    {
        "id": 2,
        "category": "EI",
        "emoji": "🌙",
        "question": "긴 포켓몬 여행 후 에너지를 충전하는 방법은?",
        "options": [
            {"text": "🎊 트레이너 친구들 불러서 파티! 신나게 놀아야 충전되지~", "score": {"E": 2}},
            {"text": "☕ 친한 친구 한두 명이랑 조용히 카페에서 수다", "score": {"E": 1, "I": 1}},
            {"text": "📖 혼자 좋아하는 책 읽거나 포켓몬 도감 정리하기", "score": {"I": 1}},
            {"text": "🛋️ 이불 속에 파묻혀 혼자만의 시간... 완전한 고독이 필요해", "score": {"I": 2}},
        ]
    },
    {
        "id": 3,
        "category": "EI",
        "emoji": "💬",
        "question": "포켓몬 센터에서 처음 보는 트레이너가 옆에 앉았어요. 당신은?",
        "options": [
            {"text": "😄 '안녕하세요! 저는 OO 체육관 도전 중이에요! 어디서 오셨어요?'", "score": {"E": 2}},
            {"text": "😊 상대가 말 걸면 반갑게 대화하는 편", "score": {"E": 1}},
            {"text": "😶 인사 정도는 하지만 대화는 최소한으로...", "score": {"I": 1}},
            {"text": "🙈 창밖 보면서 모르는 척... 대화하기 너무 어렵다", "score": {"I": 2}},
        ]
    },
    # ── S vs N ──
    {
        "id": 4,
        "category": "SN",
        "emoji": "🗺️",
        "question": "새로운 마을에 도착했어요! 가장 먼저 하고 싶은 것은?",
        "options": [
            {"text": "🏪 마을 구석구석 탐험하고 상점, 포켓몬센터 위치 파악!", "score": {"S": 2}},
            {"text": "📋 지도 보면서 효율적인 동선 계획 세우기", "score": {"S": 1}},
            {"text": "✨ '이 마을엔 어떤 숨겨진 비밀이 있을까?' 상상하며 탐험", "score": {"N": 1}},
            {"text": "🔮 전설 포켓몬이 숨어있을 것 같은 느낌... 직감 따라가기!", "score": {"N": 2}},
        ]
    },
    {
        "id": 5,
        "category": "SN",
        "emoji": "🎮",
        "question": "포켓몬 배틀에서 당신의 전략 스타일은?",
        "options": [
            {"text": "📊 상대 포켓몬의 실제 스탯과 기술을 분석해서 최적의 수 계산", "score": {"S": 2}},
            {"text": "📖 배워온 기본 전략을 충실히 실행하기", "score": {"S": 1}},
            {"text": "💡 상황 보면서 창의적인 전략 즉흥적으로 짜기", "score": {"N": 1}},
            {"text": "🌟 '이거다!' 싶은 직감으로 승부! 영감이 곧 전략", "score": {"N": 2}},
        ]
    },
    {
        "id": 6,
        "category": "SN",
        "emoji": "📚",
        "question": "포켓몬 도감 설명을 읽을 때 어떤 부분이 더 흥미로운가요?",
        "options": [
            {"text": "📏 키, 몸무게, 서식지 등 정확한 수치와 팩트가 재미있어!", "score": {"S": 2}},
            {"text": "🔬 실제 생태와 먹이 관계 같은 구체적인 정보", "score": {"S": 1}},
            {"text": "🌌 포켓몬의 기원과 신화적 배경이 더 흥미로워", "score": {"N": 1}},
            {"text": "💭 '이 포켓몬은 어떤 감정을 느낄까?' 상상하는 게 제일 재미있어", "score": {"N": 2}},
        ]
    },
    # ── T vs F ──
    {
        "id": 7,
        "category": "TF",
        "emoji": "⚔️",
        "question": "친한 트레이너 친구가 배틀에서 졌어요. 당신의 반응은?",
        "options": [
            {"text": "📊 '3번 기술 대신 2번 기술 썼으면 이겼어. 다음엔 이렇게 해봐'", "score": {"T": 2}},
            {"text": "🤔 패배 원인을 객관적으로 분석해서 조언해주기", "score": {"T": 1}},
            {"text": "🤗 '다음엔 잘 할 수 있을 거야! 나도 도와줄게~'", "score": {"F": 1}},
            {"text": "😢 친구가 속상해 보여서 나도 마음이 아파... 먼저 꼭 안아주기", "score": {"F": 2}},
        ]
    },
    {
        "id": 8,
        "category": "TF",
        "emoji": "🏆",
        "question": "배틀 대회에서 심판의 판정이 불공정해 보여요!",
        "options": [
            {"text": "📢 규정집 꺼내서 조항 근거로 논리적으로 항의한다", "score": {"T": 2}},
            {"text": "🗣️ 잘못됐다고 생각하면 차분하게 의견 말하기", "score": {"T": 1}},
            {"text": "😤 화나지만... 분위기 망칠까봐 참는다", "score": {"F": 1}},
            {"text": "😭 억울해서 눈물 날 것 같아... 감정이 먼저 올라와", "score": {"F": 2}},
        ]
    },
    {
        "id": 9,
        "category": "TF",
        "emoji": "🤝",
        "question": "팀 배틀에서 팀원이 실수했어요. 어떻게 하시겠어요?",
        "options": [
            {"text": "🔍 어디서 왜 실수했는지 정확하게 짚어주기 (감정 없이 팩트만)", "score": {"T": 2}},
            {"text": "💡 '이 부분은 이렇게 하는 게 더 효율적이야'라고 말하기", "score": {"T": 1}},
            {"text": "😊 '괜찮아! 다음엔 같이 연습하자'며 격려하기", "score": {"F": 1}},
            {"text": "🥺 팀원이 자책할까봐 걱정돼서 먼저 '내 잘못도 있어'라고 말하기", "score": {"F": 2}},
        ]
    },
    # ── J vs P ──
    {
        "id": 10,
        "category": "JP",
        "emoji": "🗓️",
        "question": "포켓몬 여행 계획을 세울 때 당신의 스타일은?",
        "options": [
            {"text": "📅 날짜별 일정, 방문할 체육관, 숙박 장소까지 완벽히 계획!", "score": {"J": 2}},
            {"text": "📝 큰 틀만 정해두고 세부 사항은 그때그때 결정", "score": {"J": 1}},
            {"text": "🎲 대충 방향만 정하고 발길 닿는 대로 가기", "score": {"P": 1}},
            {"text": "🌈 계획? 그게 뭔가요? 느낌 따라 자유롭게 떠나는 거지!", "score": {"P": 2}},
        ]
    },
    {
        "id": 11,
        "category": "JP",
        "emoji": "⏰",
        "question": "포켓몬 센터 약속 시간에 대한 당신의 생각은?",
        "options": [
            {"text": "⏱️ 10분 일찍 도착하는 건 기본! 늦는 건 상상도 못 해", "score": {"J": 2}},
            {"text": "✅ 약속 시간은 최대한 지키려고 노력해", "score": {"J": 1}},
            {"text": "😅 가끔 늦을 수도 있지... 5~10분은 괜찮지 않나?", "score": {"P": 1}},
            {"text": "🤷 '시간은 상대적인 거야~' (항상 20분 이상 늦음)", "score": {"P": 2}},
        ]
    },
    {
        "id": 12,
        "category": "JP",
        "emoji": "🎒",
        "question": "포켓몬 여행 가방을 쌀 때 당신의 모습은?",
        "options": [
            {"text": "📋 체크리스트 만들어서 하나하나 확인하며 완벽하게 준비", "score": {"J": 2}},
            {"text": "🧳 주요 아이템 위주로 꼼꼼히 챙기기", "score": {"J": 1}},
            {"text": "😄 '뭐 빠뜨려도 현지에서 사면 되지~' 가볍게 챙기기", "score": {"P": 1}},
            {"text": "🙈 출발 직전에 닥치는 대로 던져넣기 (뭐가 들었는지 모름)", "score": {"P": 2}},
        ]
    },
]

# ─────────────────────────────────────────────────────────────
# 포켓몬 이미지 가져오기 함수
# ─────────────────────────────────────────────────────────────
def get_pokemon_image(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data["sprites"]["other"]["official-artwork"]["front_default"]
    except:
        pass
    return None

# ─────────────────────────────────────────────────────────────
# MBTI 계산 함수
# ─────────────────────────────────────────────────────────────
def calculate_mbti(scores):
    mbti = ""
    mbti += "E" if scores.get("E", 0) >= scores.get("I", 0) else "I"
    mbti += "N" if scores.get("N", 0) >= scores.get("S", 0) else "S"
    mbti += "F" if scores.get("F", 0) >= scores.get("T", 0) else "T"
    mbti += "P" if scores.get("P", 0) >= scores.get("J", 0) else "J"
    return mbti

# ─────────────────────────────────────────────────────────────
# 성향 강도 계산 함수
# ─────────────────────────────────────────────────────────────
def get_tendency_percent(scores, key1, key2):
    total = scores.get(key1, 0) + scores.get(key2, 0)
    if total == 0:
        return 50
    return int((scores.get(key1, 0) / total) * 100)

# ─────────────────────────────────────────────────────────────
# 세션 상태 초기화
# ─────────────────────────────────────────────────────────────
if "stage" not in st.session_state:
    st.session_state.stage = "intro"       # intro / quiz / result
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "scores" not in st.session_state:
    st.session_state.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
if "answers" not in st.session_state:
    st.session_state.answers = []
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None
if "show_next" not in st.session_state:
    st.session_state.show_next = False

# ─────────────────────────────────────────────────────────────
# 타이틀 (항상 표시)
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-title">
    <h1 style="color:white; font-size:2.2em; margin:0;">⚡ MBTI 포켓몬 퀴즈 ⚡</h1>
    <p style="color:rgba(255,255,255,0.85); font-size:1.15em; margin:10px 0 0 0;">
        🎮 12가지 질문으로 나와 닮은 포켓몬 찾기! 🎮
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 인트로 화면
# ─────────────────────────────────────────────────────────────
if st.session_state.stage == "intro":

    st.markdown("""
    <div class="intro-box">
        <p style="font-size:3.5em; margin:0;">🎮</p>
        <h2 style="color:#333; margin:10px 0;">나의 포켓몬 파트너는 누구?</h2>
        <p style="color:#555; font-size:1.05em; line-height:1.8;">
            12개의 재미있는 질문에 답하면<br>
            당신의 MBTI 성격 유형과 딱 맞는<br>
            <b>🌟 나만의 포켓몬 파트너</b>를 알려드려요!
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 통계 카드
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#667eea,#764ba2);color:white;
                    border-radius:15px;padding:20px;text-align:center;">
            <p style="font-size:2em;margin:0;">❓</p>
            <p style="font-size:1.5em;font-weight:bold;margin:5px 0;">12문항</p>
            <p style="font-size:0.85em;margin:0;opacity:0.85;">정성껏 만든 퀴즈</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#f093fb,#f5576c);color:white;
                    border-radius:15px;padding:20px;text-align:center;">
            <p style="font-size:2em;margin:0;">🎮</p>
            <p style="font-size:1.5em;font-weight:bold;margin:5px 0;">16종류</p>
            <p style="font-size:0.85em;margin:0;opacity:0.85;">포켓몬 파트너</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#4facfe,#00f2fe);color:white;
                    border-radius:15px;padding:20px;text-align:center;">
            <p style="font-size:2em;margin:0;">⏱️</p>
            <p style="font-size:1.5em;font-weight:bold;margin:5px 0;">3분</p>
            <p style="font-size:0.85em;margin:0;opacity:0.85;">예상 소요 시간</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 미리보기 포켓몬
    st.markdown("### 👀 어떤 포켓몬이 기다릴까요?")
    preview = [
        ("⚡","피카츄","ESFP"), ("🔥","리자몽","ENTJ"),
        ("🧠","뮤츠","INTJ"),  ("✨","뮤","ENFJ"),
        ("🌙","루기아","INFJ"), ("🌸","이브이","INFP"),
        ("🌊","개굴닌자","ENTP"),("🎤","푸린","ESFJ"),
    ]
    cols = st.columns(4)
    for i, (emoji, name, mbti_type) in enumerate(preview):
        with cols[i % 4]:
            st.markdown(f"""
            <div style="text-align:center;padding:14px;background:white;
                        border-radius:14px;box-shadow:0 4px 15px rgba(0,0,0,0.1);
                        margin:5px 0; transition: all 0.3s;">
                <p style="font-size:2em;margin:0;">{emoji}</p>
                <p style="font-size:0.9em;color:#333;margin:4px 0;font-weight:bold;">{name}</p>
                <p style="font-size:0.78em;color:#888;margin:0;">{mbti_type}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 퀴즈 시작하기! 내 포켓몬 파트너 찾으러 GO!"):
        st.session_state.stage = "quiz"
        st.session_state.current_q = 0
        st.session_state.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
        st.session_state.answers = []
        st.session_state.selected_option = None
        st.session_state.show_next = False
        st.rerun()

# ─────────────────────────────────────────────────────────────
# 퀴즈 화면
# ─────────────────────────────────────────────────────────────
elif st.session_state.stage == "quiz":

    q_idx = st.session_state.current_q
    q = QUESTIONS[q_idx]
    total_q = len(QUESTIONS)

    # 진행률 표시
    progress = (q_idx) / total_q
    st.markdown(f"""
    <div style="margin:10px 0 20px 0;">
        <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
            <span style="font-size:0.9em; color:#667eea; font-weight:bold;">
                🎮 질문 {q_idx + 1} / {total_q}
            </span>
            <span style="font-size:0.9em; color:#764ba2; font-weight:bold;">
                {int(progress * 100)}% 완료
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.progress(progress)

    # 카테고리 라벨
    cat_labels = {
        "EI": "💬 사교성 탐구",
        "SN": "🔭 인식 방식 탐구",
        "TF": "❤️ 판단 방식 탐구",
        "JP": "📅 생활 방식 탐구"
    }
    cat_color = {
        "EI": "#667eea", "SN": "#f093fb",
        "TF": "#f5576c", "JP": "#4facfe"
    }
    cat = q["category"]
    st.markdown(f"""
    <div style="display:inline-block; background:{cat_color[cat]}; color:white;
                padding:5px 16px; border-radius:20px; font-size:0.85em;
                margin-bottom:10px; font-weight:bold;">
        {cat_labels[cat]}
    </div>
    """, unsafe_allow_html=True)

    # 질문 카드
    st.markdown(f"""
    <div class="question-card">
        <h2 style="color:#333; font-size:1.5em; margin:0; line-height:1.5;">
            {q['emoji']} Q{q_idx + 1}. {q['question']}
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # 선택지 버튼
    st.markdown("##### 🖱️ 아래에서 하나를 선택해주세요!")

    for opt_idx, option in enumerate(q["options"]):
        # 이미 선택된 항목이면 표시 다르게
        if st.session_state.selected_option == opt_idx:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#667eea,#764ba2);
                        color:white; border-radius:14px; padding:16px 20px;
                        margin:8px 0; font-size:1.05em; line-height:1.5;
                        box-shadow:0 5px 20px rgba(102,126,234,0.5);
                        border:2px solid #fff;">
                ✅ {option['text']}
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.button(
                option["text"],
                key=f"q{q_idx}_opt{opt_idx}",
                disabled=st.session_state.show_next
            ):
                st.session_state.selected_option = opt_idx
                st.session_state.show_next = True
                # 점수 누적
                for k, v in option["score"].items():
                    st.session_state.scores[k] = st.session_state.scores.get(k, 0) + v
                st.session_state.answers.append({
                    "question": q["question"],
                    "answer": option["text"]
                })
                st.rerun()

    # 선택 후 피드백 + 다음 버튼
    if st.session_state.show_next:
        selected_opt = q["options"][st.session_state.selected_option]
        score_keys = list(selected_opt["score"].keys())

        # 성향 힌트
        hint_map = {
            "E": "🗣️ 외향적 성향이 나타났어요!",
            "I": "🤫 내향적 성향이 나타났어요!",
            "S": "🔍 현실감각이 뛰어나요!",
            "N": "🌟 직관력이 번뜩여요!",
            "T": "🧠 논리적 사고가 강해요!",
            "F": "💖 감성이 풍부해요!",
            "J": "📋 계획적인 성격이에요!",
            "P": "🎲 자유로운 영혼이에요!"
        }
        hint_emojis = [hint_map.get(k, "") for k in score_keys if k in hint_map]
        hint_text = " / ".join(hint_emojis) if hint_emojis else "🎯 선택 완료!"

        reactions = ["잘 골랐어요! 🎉", "좋은 선택이에요! ✨", "멋진 대답이에요! 🌟",
                     "흥미롭네요! 🔮", "포켓몬이 고개를 끄덕여요! 👍"]
        reaction = random.choice(reactions)

        st.markdown(f"""
        <div class="answer-feedback" style="background:linear-gradient(135deg,#d4fc79,#96e6a1);color:#333;">
            <p style="margin:0; font-size:1.05em;">{reaction}</p>
            <p style="margin:5px 0 0 0; font-size:0.9em; color:#555;">{hint_text}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 다음 / 결과 보기 버튼
        if q_idx < total_q - 1:
            if st.button(f"다음 질문으로 → ({q_idx + 2}/{total_q}) 🎮"):
                st.session_state.current_q += 1
                st.session_state.selected_option = None
                st.session_state.show_next = False
                st.rerun()
        else:
            if st.button("🎊 결과 보기! 내 포켓몬 파트너가 누구야?! 🎊"):
                st.session_state.stage = "result"
                st.session_state.selected_option = None
                st.session_state.show_next = False
                st.rerun()

    # 하단 포켓몬 이모지 장식
    st.markdown("<br>", unsafe_allow_html=True)
    random_emojis = ["⚡","🔥","💧","🌿","✨","🌙","💎","🌊"]
    emoji_row = " ".join(
        f"<span style='opacity:{'1.0' if i == q_idx % len(random_emojis) else '0.3'};font-size:1.5em;'>{e}</span>"
        for i, e in enumerate(random_emojis)
    )
    st.markdown(
        f"<div style='text-align:center; margin-top:10px;'>{emoji_row}</div>",
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────────────────────
# 결과 화면
# ─────────────────────────────────────────────────────────────
elif st.session_state.stage == "result":

    mbti = calculate_mbti(st.session_state.scores)
    data = MBTI_POKEMON.get(mbti, MBTI_POKEMON["ESFP"])

    # 🎉 축하 애니메이션 텍스트
    st.markdown("""
    <div style="text-align:center; font-size:2.5em; margin:10px 0;" class="shimmer">
        🎊 결과가 나왔어요! 🎊
    </div>
    """, unsafe_allow_html=True)

    # MBTI 뱃지
    st.markdown(f"""
    <div style="text-align:center; margin:10px 0;">
        <span class="mbti-badge">✨ {mbti} ✨</span>
        <br>
        <span style="font-size:1.1em; color:#555;">{data['mbti_desc']}</span>
    </div>
    """, unsafe_allow_html=True)

    # 포켓몬 카드
    st.markdown('<div class="result-card">', unsafe_allow_html=True)

    # 포켓몬 이미지
    img_url = get_pokemon_image(data["english_name"])
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        if img_url:
            st.image(img_url, width=260)
        else:
            st.markdown(
                f"<p style='text-align:center;font-size:6em;margin:0;'>{data['emoji']}</p>",
                unsafe_allow_html=True
            )

    # 포켓몬 이름 & 등급
    st.markdown(f"""
    <h2 style="text-align:center; font-size:2.2em; color:#333; margin:8px 0;">
        {data['emoji']} {data['name']} {data['emoji']}
    </h2>
    <p style="text-align:center; font-size:1em; color:#888; margin:4px 0;">
        {data['rarity']} &nbsp;|&nbsp; {data['battle_style']}
    </p>
    """, unsafe_allow_html=True)

    # 타입 뱃지
    type_colors = {
        "불꽃": "#F08030", "물": "#6890F0", "풀": "#78C850",
        "전기": "#F8D030", "에스퍼": "#FF6B9D", "노말": "#A8A878",
        "비행": "#98B8F0", "독": "#A040A0", "고스트": "#705898",
        "페어리": "#EE99AC", "악": "#705848"
    }
    badges = ""
    for type_name, color in data["type_color"].items():
        badges += f'<span class="type-badge" style="background:{color};">{type_name}</span>'
    st.markdown(
        f'<div style="text-align:center;margin:10px 0;">{badges}</div>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 📊 MBTI 성향 분석 바
    st.markdown("### 📊 나의 성향 분석 결과")
    scores = st.session_state.scores

    axes = [
        ("E", "I", "🗣️ 외향", "🤫 내향"),
        ("N", "S", "🌟 직관", "🔍 감각"),
        ("F", "T", "💖 감성", "🧠 논리"),
        ("P", "J", "🎲 자유", "📋 계획"),
    ]
    for k1, k2, label1, label2 in axes:
        pct = get_tendency_percent(scores, k1, k2)
        pct2 = 100 - pct
        chosen = k1 if else pct >= 50
   

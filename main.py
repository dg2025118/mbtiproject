import streamlit as st
import requests

# ─────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────
st.set_page_config(
    page_title="🔮 MBTI 포켓몬 매칭",
    page_icon="⚡",
    layout="centered"
)

# ─────────────────────────────────────────
# CSS 스타일
# ─────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

    html, body, [class*="css"] {
        font-family: 'Jua', sans-serif;
    }

    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    .title-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }

    .pokemon-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        border: 3px solid #e8eeff;
        margin: 10px 0;
    }

    .mbti-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 8px 20px;
        border-radius: 50px;
        font-size: 1.3em;
        font-weight: bold;
        margin: 10px;
        box-shadow: 0 4px 15px rgba(102,126,234,0.4);
    }

    .type-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.9em;
        margin: 3px;
        color: white;
        font-weight: bold;
    }

    .reason-box {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border-left: 5px solid #ff8c69;
    }

    .trait-box {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
    }

    .fun-fact-box {
        background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border-left: 5px solid #52c234;
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 15px 40px;
        font-size: 1.2em;
        font-weight: bold;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(102,126,234,0.4);
        font-family: 'Jua', sans-serif;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102,126,234,0.5);
    }

    .footer {
        text-align: center;
        padding: 20px;
        color: #888;
        font-size: 0.85em;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# MBTI별 포켓몬 데이터
# ─────────────────────────────────────────
MBTI_POKEMON = {
    "INTJ": {
        "name": "뮤츠",
        "english_name": "mewtwo",
        "emoji": "🧠",
        "reason": "혼자서도 강력하고, 치밀한 전략가! 감정보다 논리를 중시하며 자신만의 세계를 구축하는 당신은 뮤츠입니다.",
        "traits": ["🎯 완벽주의자", "🔬 분석적 사고", "🏆 독립적", "💡 전략가"],
        "fun_fact": "뮤츠는 과학으로 탄생한 포켓몬으로, 압도적인 지능과 실력을 자랑해요! INTJ처럼 계획적이고 강렬하죠.",
        "type_color": {"에스퍼": "#FF6B9D"},
        "mbti_desc": "용의주도한 전략가 ♟️"
    },
    "INTP": {
        "name": "포리곤",
        "english_name": "porygon",
        "emoji": "💻",
        "reason": "디지털 세계를 탐험하는 분석가! 끊임없이 지식을 탐구하고 새로운 이론을 발견하는 당신은 포리곤입니다.",
        "traits": ["🔍 탐구적", "🧩 논리적", "💭 창의적 사고", "📚 지식 탐험가"],
        "fun_fact": "포리곤은 완전히 프로그래밍으로 만들어진 최초의 포켓몬이에요! 끊임없이 진화하는 모습이 INTP와 닮았죠.",
        "type_color": {"노말": "#A8A878"},
        "mbti_desc": "논리적인 사색가 🔭"
    },
    "ENTJ": {
        "name": "리자몽",
        "english_name": "charizard",
        "emoji": "🔥",
        "reason": "타오르는 카리스마로 모두를 이끄는 리더! 목표를 향해 불꽃처럼 돌진하는 당신은 리자몽입니다.",
        "traits": ["👑 천생 리더", "🔥 강한 의지", "⚡ 결단력", "🎖️ 야망가"],
        "fun_fact": "리자몽은 강한 상대와의 싸움을 즐기는 포켓몬이에요! ENTJ처럼 도전을 두려워하지 않는 불굴의 정신을 가졌죠.",
        "type_color": {"불꽃": "#F08030", "비행": "#6890F0"},
        "mbti_desc": "대담한 통솔자 🦁"
    },
    "ENTP": {
        "name": "개굴닌자",
        "english_name": "greninja",
        "emoji": "🌊",
        "reason": "재치와 아이디어로 상황을 뒤집는 토론가! 항상 새로운 방식으로 문제를 해결하는 당신은 개굴닌자입니다.",
        "traits": ["💬 토론왕", "⚡ 빠른 두뇌", "🎭 유머러스", "🆕 혁신가"],
        "fun_fact": "개굴닌자는 순식간에 물 수리검을 만들어 공격하는 창의적인 전술가에요! ENTP처럼 즉흥적이면서도 천재적이죠.",
        "type_color": {"물": "#6890F0", "악": "#705848"},
        "mbti_desc": "논쟁을 즐기는 변론가 ⚡"
    },
    "INFJ": {
        "name": "루기아",
        "english_name": "lugia",
        "emoji": "🌙",
        "reason": "깊은 내면과 숭고한 이상을 가진 선지자! 세상을 더 나은 곳으로 만들고 싶은 당신은 루기아입니다.",
        "traits": ["🌟 이상주의자", "💞 공감 능력", "🔮 통찰력", "🕊️ 평화주의"],
        "fun_fact": "루기아는 바다의 수호자로 강한 힘을 가지고 있지만 조용히 숨어사는 포켓몬이에요! INFJ의 조용한 영향력과 닮았죠.",
        "type_color": {"에스퍼": "#FF6B9D", "비행": "#6890F0"},
        "mbti_desc": "통찰력 있는 선지자 🔮"
    },
    "INFP": {
        "name": "이브이",
        "english_name": "eevee",
        "emoji": "🌸",
        "reason": "무한한 가능성과 풍부한 감수성을 가진 중재자! 자신만의 가치관을 소중히 여기는 당신은 이브이입니다.",
        "traits": ["🎨 풍부한 감성", "🌈 무한한 가능성", "💝 따뜻한 마음", "🦋 자유로운 영혼"],
        "fun_fact": "이브이는 8가지 진화형을 가진 특별한 포켓몬이에요! INFP처럼 어떤 방향으로든 성장할 수 있는 무한한 잠재력을 가졌죠.",
        "type_color": {"노말": "#A8A878"},
        "mbti_desc": "열정적인 중재자 🌸"
    },
    "ENFJ": {
        "name": "뮤",
        "english_name": "mew",
        "emoji": "✨",
        "reason": "모두를 사랑하고 이끄는 선도자! 타인의 성장을 진심으로 응원하는 당신은 뮤입니다.",
        "traits": ["🤝 사교적", "💖 이타적", "🌟 영감을 주는", "🎯 목표 지향적"],
        "fun_fact": "뮤는 모든 포켓몬의 DNA를 가진 전설의 포켓몬이에요! ENFJ처럼 누구와도 잘 어울리고 모두를 품을 수 있죠.",
        "type_color": {"에스퍼": "#FF6B9D"},
        "mbti_desc": "정의로운 사회운동가 🌟"
    },
    "ENFP": {
        "name": "파치리스",
        "english_name": "pachirisu",
        "emoji": "⚡",
        "reason": "넘치는 에너지와 긍정으로 주변을 밝히는 활동가! 호기심 많고 열정적인 당신은 파치리스입니다.",
        "traits": ["🎉 활기차고 명랑", "💫 창의적", "🌈 낙천적", "🤗 사교적"],
        "fun_fact": "파치리스는 항상 활발하게 뛰어다니는 에너지 넘치는 포켓몬이에요! ENFP처럼 어디서든 분위기를 밝게 만들죠.",
        "type_color": {"전기": "#F8D030"},
        "mbti_desc": "재기발랄한 활동가 🎊"
    },
    "ISTJ": {
        "name": "두두",
        "english_name": "doduo",
        "emoji": "📋",
        "reason": "책임감 강하고 신뢰할 수 있는 현실주의자! 맡은 일을 끝까지 해내는 당신은 두두입니다. (사실 가장 믿음직한 포켓몬 중 하나!)",
        "traits": ["✅ 책임감", "📌 꼼꼼함", "🏛️ 전통 중시", "🔐 신뢰할 수 있는"],
        "fun_fact": "두두는 날지 못하지만 엄청난 속도로 달리는 포켓몬이에요! ISTJ처럼 꾸준하고 성실하게 자신의 방식을 지켜나가죠.",
        "type_color": {"노말": "#A8A878", "비행": "#6890F0"},
        "mbti_desc": "청렴결백한 논리주의자 📐"
    },
    "ISFJ": {
        "name": "치코리타",
        "english_name": "chikorita",
        "emoji": "🌿",
        "reason": "따뜻하고 헌신적인 수호자! 소중한 사람들을 위해 조용히 곁을 지키는 당신은 치코리타입니다.",
        "traits": ["🤲 헌신적", "🌱 배려심", "🏠 안정 추구", "💚 따뜻한 마음"],
        "fun_fact": "치코리타는 달콤한 향기로 주변을 치유하는 포켓몬이에요! ISFJ처럼 말없이 주변 사람들을 돌보는 따뜻한 존재죠.",
        "type_color": {"풀": "#78C850"},
        "mbti_desc": "용감한 수호자 🛡️"
    },
    "ESTJ": {
        "name": "갸라도스",
        "english_name": "gyarados",
        "emoji": "💪",
        "reason": "강력한 실행력과 리더십으로 조직을 이끄는 경영자! 목표를 향해 거침없이 나아가는 당신은 갸라도스입니다.",
        "traits": ["👔 강한 리더십", "⚡ 결단력", "📊 체계적", "🎯 목표 지향"],
        "fun_fact": "갸라도스는 연약한 잉어킹에서 엄청난 포켓몬으로 진화해요! ESTJ처럼 끊임없는 노력으로 최고의 자리에 오르죠.",
        "type_color": {"물": "#6890F0", "비행": "#6890F0"},
        "mbti_desc": "엄격한 관리자 📊"
    },
    "ESFJ": {
        "name": "푸린",
        "english_name": "jigglypuff",
        "emoji": "🎤",
        "reason": "모두를 행복하게 만드는 사교적인 외교관! 언제나 주변을 즐겁게 해주는 당신은 푸린입니다.",
        "traits": ["🎵 사교적", "💕 다정함", "🤝 협력적", "🎉 분위기 메이커"],
        "fun_fact": "푸린은 노래로 모두를 즐겁게 해주는 포켓몬이에요! ESFJ처럼 자신의 재능으로 주변을 행복하게 만들죠.",
        "type_color": {"노말": "#A8A878", "페어리": "#EE99AC"},
        "mbti_desc": "사교적인 외교관 🎊"
    },
    "ISTP": {
        "name": "팬텀",
        "english_name": "haunter",
        "emoji": "🔧",
        "reason": "조용하지만 놀라운 실력을 가진 만능 재주꾼! 혼자서 모든 것을 해결하는 당신은 팬텀입니다.",
        "traits": ["🔩 실용적", "🎭 관찰력", "⚡ 위기 대응", "🤫 독립적"],
        "fun_fact": "팬텀은 조용히 관찰하다가 갑자기 나타나 상황을 반전시키는 포켓몬이에요! ISTP처럼 언제나 예상치 못한 해결책을 가지고 있죠.",
        "type_color": {"고스트": "#705898", "독": "#A040A0"},
        "mbti_desc": "대담한 탐험가 🔧"
    },
    "ISFP": {
        "name": "뮨",
        "english_name": "mime-jr",
        "emoji": "🎨",
        "reason": "자유롭고 예술적인 영혼을 가진 모험가! 순간을 소중히 여기는 감성적인 당신은 뮨입니다.",
        "traits": ["🎨 예술적", "🌸 감성적", "🌿 자연 친화", "💃 자유로운"],
        "fun_fact": "뮨은 흉내내기의 달인으로 표현력이 풍부한 포켓몬이에요! ISFP처럼 자신만의 독특한 방식으로 세상을 표현하죠.",
        "type_color": {"에스퍼": "#FF6B9D"},
        "mbti_desc": "호기심 많은 예술가 🎨"
    },
    "ESTP": {
        "name": "잠만보",
        "english_name": "snorlax",
        "emoji": "🌪️",
        "reason": "현실적이고 활동적인 사업가! 눈앞의 상황에 즉각 반응하는 당신은 사실... 먹을 것 앞에서만큼은 누구보다 빠른 잠만보입니다! 😄",
        "traits": ["💨 즉흥적", "😎 여유로움", "💪 강인함", "🎯 현실주의"],
        "fun_fact": "잠만보는 평소엔 여유롭지만 먹을 것 앞에서는 누구보다 빠르게 행동하는 포켓몬이에요! ESTP처럼 필요할 때 폭발적인 에너지를 발휘하죠.",
        "type_color": {"노말": "#A8A878"},
        "mbti_desc": "모험을 즐기는 사업가 🌪️"
    },
    "ESFP": {
        "name": "피카츄",
        "english_name": "pikachu",
        "emoji": "⚡",
        "reason": "세상에서 가장 유명하고 사랑받는 연예인! 항상 밝고 에너지 넘치는 당신은 피카츄입니다!",
        "traits": ["🌟 스타 기질", "💛 사랑스러운", "🎉 활기차고 재미있는", "🤸 자유분방"],
        "fun_fact": "피카츄는 전 세계에서 가장 사랑받는 포켓몬이에요! ESFP처럼 어디서든 빛나고 모두에게 사랑받는 천생 연예인이죠.",
        "type_color": {"전기": "#F8D030"},
        "mbti_desc": "자유로운 연예인 🌟"
    },
}

# 타입별 배경색
TYPE_COLORS = {
    "불꽃": "#F08030", "물": "#6890F0", "풀": "#78C850",
    "전기": "#F8D030", "에스퍼": "#FF6B9D", "노말": "#A8A878",
    "비행": "#98B8F0", "독": "#A040A0", "고스트": "#705898",
    "페어리": "#EE99AC", "악": "#705848", "강철": "#B8B8D0",
    "드래곤": "#7038F8", "얼음": "#98D8D8", "격투": "#C03028",
    "바위": "#B8A038", "땅": "#E0C068", "벌레": "#A8B820",
}

def get_pokemon_image(pokemon_name):
    """포켓몬 이미지 URL 가져오기"""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data["sprites"]["other"]["official-artwork"]["front_default"]
    except:
        pass
    return None

# ─────────────────────────────────────────
# 앱 메인
# ─────────────────────────────────────────

# 타이틀
st.markdown("""
<div class="title-box">
    <h1>⚡ MBTI 포켓몬 매칭 ⚡</h1>
    <p style="font-size:1.2em; color:#555;">
        🎮 나의 MBTI와 닮은 포켓몬은 누구일까요? 🎮
    </p>
    <p style="font-size:0.95em; color:#888;">
        16가지 MBTI 유형별로 딱 맞는 포켓몬을 찾아드려요! 🌟
    </p>
</div>
""", unsafe_allow_html=True)

# MBTI 선택
st.markdown("### 🔍 당신의 MBTI를 선택해주세요!")

mbti_list = list(MBTI_POKEMON.keys())

# 4x4 그리드로 MBTI 보여주기
cols = st.columns(4)
selected_mbti = None

if "selected_mbti" not in st.session_state:
    st.session_state.selected_mbti = None

for i, mbti in enumerate(mbti_list):
    with cols[i % 4]:
        if st.button(mbti, key=f"btn_{mbti}"):
            st.session_state.selected_mbti = mbti

st.markdown("---")

# 결과 표시
if st.session_state.selected_mbti:
    mbti = st.session_state.selected_mbti
    data = MBTI_POKEMON[mbti]

    # 선택된 MBTI 표시
    st.markdown(f"""
    <div style="text-align:center; margin: 10px 0;">
        <span class="mbti-badge">✨ {mbti} ✨</span>
        <p style="font-size:1.1em; color:#555; margin-top:5px;">{data['mbti_desc']}</p>
    </div>
    """, unsafe_allow_html=True)

    # 포켓몬 카드
    with st.container():
        st.markdown('<div class="pokemon-card">', unsafe_allow_html=True)

        # 포켓몬 이미지
        img_url = get_pokemon_image(data["english_name"])

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if img_url:
                st.image(img_url, width=250)
            else:
                st.markdown(f"<h1 style='text-align:center; font-size:5em;'>{data['emoji']}</h1>",
                           unsafe_allow_html=True)

        # 포켓몬 이름
        st.markdown(f"""
        <h2 style="text-align:center; font-size:2em; color:#333; margin:10px 0;">
            {data['emoji']} {data['name']} {data['emoji']}
        </h2>
        """, unsafe_allow_html=True)

        # 타입 배지
        type_badges = ""
        for type_name, color in data["type_color"].items():
            type_badges += f'<span class="type-badge" style="background-color:{color};">{type_name}</span>'

        st.markdown(f'<div style="text-align:center; margin:10px 0;">{type_badges}</div>',
                   unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # 이유 박스
    st.markdown(f"""
    <div class="reason-box">
        <h3>💌 당신이 {data['name']}인 이유!</h3>
        <p style="font-size:1.05em; line-height:1.8;">{data['reason']}</p>
    </div>
    """, unsafe_allow_html=True)

    # 성격 특성
    st.markdown(f"""
    <div class="trait-box">
        <h3>🌈 {mbti} 유형의 특징</h3>
        <div style="display:flex; flex-wrap:wrap; gap:10px; justify-content:center; margin-top:10px;">
            {''.join([f'<span style="background:white; padding:8px 15px; border-radius:20px; font-size:0.95em; box-shadow:0 2px 8px rgba(0,0,0,0.1);">{trait}</span>' for trait in data['traits']])}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 재미있는 사실
    st.markdown(f"""
    <div class="fun-fact-box">
        <h3>🎲 포켓몬 재미있는 사실!</h3>
        <p style="font-size:1.05em; line-height:1.8;">{data['fun_fact']}</p>
    </div>
    """, unsafe_allow_html=True)

    # 공유 메시지
    st.markdown(f"""
    <div style="text-align:center; padding:20px; background:linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                border-radius:15px; color:white; margin:15px 0;">
        <h3>📱 친구들에게 공유해보세요!</h3>
        <p style="font-size:1em;">나의 MBTI는 {mbti}! 나와 닮은 포켓몬은 {data['emoji']} {data['name']}이래요~</p>
    </div>
    """, unsafe_allow_html=True)

    # 다시하기
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 다른 MBTI도 확인해보기!", key="reset"):
        st.session_state.selected_mbti = None
        st.rerun()

else:
    # 선택 전 안내 화면
    st.markdown("""
    <div style="text-align:center; padding:40px; background:linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
                border-radius:20px; margin:20px 0;">
        <p style="font-size:3em; margin:0;">👆</p>
        <h3 style="color:#555;">위에서 MBTI를 선택해보세요!</h3>
        <p style="color:#777; font-size:1em;">당신과 닮은 포켓몬이 기다리고 있어요 🌟</p>
        <p style="font-size:2em; margin:10px 0;">
            🌱 🔥 💧 ⚡ 🌊 🧠 ✨ 💛
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 미리보기 힌트
    st.markdown("### 👀 어떤 포켓몬이 있을까요?")
    hints = [
        ("⚡", "ESFP", "피카츄"),
        ("🔥", "ENTJ", "리자몽"),
        ("✨", "ENFJ", "뮤"),
        ("🧠", "INTJ", "뮤츠"),
        ("🌸", "INFP", "이브이"),
        ("🌙", "INFJ", "루기아"),
        ("🌊", "ENTP", "개굴닌자"),
        ("💛", "ESFJ", "푸린"),
    ]

    hint_cols = st.columns(4)
    for i, (emoji, mbti_type, name) in enumerate(hints):
        with hint_cols[i % 4]:
            st.markdown(f"""
            <div style="text-align:center; padding:15px; background:white;
                        border-radius:15px; box-shadow:0 3px 10px rgba(0,0,0,0.1); margin:5px 0;">
                <p style="font-size:2em; margin:0;">{emoji}</p>
                <p style="font-size:0.85em; color:#666; margin:3px 0; font-weight:bold;">{mbti_type}</p>
                <p style="font-size:0.8em; color:#999; margin:0;">{name}</p>
            </div>
            """, unsafe_allow_html=True)

# 푸터
st.markdown("""
<div class="footer">
    <p>⚡ MBTI 포켓몬 매칭 | 당곡고등학교 AI 도우미 ⚡</p>
    <p>🎮 포켓몬 이미지 출처: PokéAPI | 재미로 즐기는 MBTI 테스트 🎮</p>
</div>
""", unsafe_allow_html=True)

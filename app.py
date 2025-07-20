import streamlit as st
from PIL import Image
import os
import random
import pandas as pd
import json
from datetime import datetime

# ✅ 허용된 아이디 목록
ALLOWED_USERS = ["cotty23", "teleecho", "cotty00"]

# ✅ 관리자 ID
ADMIN_ID = "cotty23"

# ✅ 카드 해석 딕셔너리
card_meanings = {}

# ✅ JSON 불러오기
if os.path.exists("card_meanings.json"):
    with open("card_meanings.json", "r", encoding="utf-8") as f:
        card_meanings = json.load(f)

# ✅ 로그인 처리
if "user" not in st.session_state:
    st.set_page_config(page_title="동양타로", page_icon="🌗", layout="centered")
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp { overflow-x: hidden; }
        button[title="View source"] {visibility: hidden;}
        .stDeployButton {display: none;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    st.markdown("## 🔐 로그인")
    email = st.text_input("아이디를 입력하세요")
    if st.button("로그인"):
        if email in ALLOWED_USERS:
            st.session_state.user = email
            st.success(f"{email} 님 환영합니다.")
            st.rerun()
        else:
            st.error("접근 권한이 없습니다.")
    st.stop()

# ➤ 세션 초기화
for key in ["mode", "cards", "reversed", "extra_cards", "advice_card", "question_yes", "question_no", "history"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key in ["cards", "reversed", "extra_cards", "history"] else ""

img_folder = "카드이미지"

def load_cards():
    if not os.path.exists(img_folder):
        st.error(f"이미지 폴더가 없습니다: {img_folder}")
        return []
    return [f for f in os.listdir(img_folder) if f.lower().endswith(('png', 'jpg', 'jpeg'))]

def draw_cards(n):
    card_pool = load_cards()
    if len(card_pool) < n:
        return []
    cards = random.sample(card_pool, n)
    directions = [random.choice(['정방향', '역방향']) for _ in range(n)]
    return list(zip(cards, directions))

def show_card(card, direction, width=200):
    img = Image.open(os.path.join(img_folder, card))
    if direction == "역방향":
        img = img.rotate(180)
    st.image(img, caption=f"{card} ({direction})", width=width)

def interpret_result(card_name, direction):
    result = card_meanings.get(card_name, {})
    parts = []
    if "이미지설명" in result:
        parts.append(f"🖼️ {result['이미지설명']}")
    if "의미요약" in result:
        parts.append(f"🧭 {result['의미요약']}")
    parts.append(result.get(direction, "💬 이 카드에 대한 해석이 준비 중입니다."))
    if "조언" in result:
        parts.append(f"📝 {result['조언']}")
    return "\n\n".join(parts)

def save_result(title, card_data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"시간": timestamp, "타입": title, "카드 정보": card_data}
    st.session_state.history.append(entry)

def download_history():
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 결과 다운로드 (CSV)", data=csv, file_name="타로_기록.csv", mime="text/csv")

# ✅ 사용자 모드 (관리자 포함)
if st.session_state.user in ALLOWED_USERS:
    st.markdown("---")
    st.markdown("<h2 style='text-align:center;'>🌗 동양타로</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>\"한 장의 카드가 내 마음을 말하다\"</p>", unsafe_allow_html=True)
    st.markdown("---")

    rerun_needed = False

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔮 3카드 보기"):
            st.session_state.cards = draw_cards(3)
            st.session_state.extra_cards = [None, None, None]
            st.session_state.advice_card = None
            st.session_state.mode = "3카드"
            rerun_needed = True
    with col2:
        if st.button("✨ 원카드"):
            st.session_state.cards = draw_cards(1)
            st.session_state.extra_cards = [None]
            st.session_state.mode = "원카드"
            rerun_needed = True

    col3, col4 = st.columns(2)
    with col3:
        if st.button("🔀 양자택일"):
            st.session_state.cards = draw_cards(2)
            st.session_state.extra_cards = [None, None]
            st.session_state.mode = "양자택일"
            rerun_needed = True
    with col4:
        if st.button("🗣 오늘의 조언"):
            st.session_state.cards = draw_cards(1)
            st.session_state.extra_cards = [None]
            st.session_state.mode = "조언카드"
            rerun_needed = True

    download_history()

    if rerun_needed:
        st.rerun()

    # ✅ 양자택일 결과 + 최종 결론 카드
    if st.session_state.mode == "양자택일" and len(st.session_state.cards) == 2:
        st.subheader("🔀 양자택일 결과")
        col1, col2 = st.columns(2)
        for i, col in enumerate([col1, col2]):
            with col:
                card, direction = st.session_state.cards[i]
                label = "선택 1" if i == 0 else "선택 2"
                st.markdown(f"**{label}**")
                show_card(card, direction)
                st.markdown(interpret_result(card, direction))
        if st.button("✅ 최종 결론 카드 보기"):
            st.session_state.advice_card = draw_cards(1)[0]
        if st.session_state.advice_card:
            st.subheader("📌 최종 결론 카드")
            final_card, final_dir = st.session_state.advice_card
            show_card(final_card, final_dir)
            st.markdown(interpret_result(final_card, final_dir))

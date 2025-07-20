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

    # ✅ 관리자 메시지 및 기능 노출
    if st.session_state.user == ADMIN_ID:
        st.success("🛠️ 관리자님 반갑습니다.")
        with st.expander("📂 카드 설명 등록/삭제"):
            selected_card = st.selectbox("카드 이미지 파일 선택", load_cards())
            img = Image.open(os.path.join(img_folder, selected_card))
            st.image(img, caption=selected_card, width=200)

            with st.form("add_meaning_form"):
                desc = st.text_area("🖼️ 이미지 설명")
                summary = st.text_area("🧭 카드 의미 요약")
                meaning_upright = st.text_area("🟢 정방향 해석")
                meaning_reversed = st.text_area("🔴 역방향 해석")
                advice = st.text_area("📝 조언 메시지")
                submitted = st.form_submit_button("✅ 등록/수정")
                if submitted:
                    card_meanings[selected_card] = {
                        "이미지설명": desc,
                        "의미요약": summary,
                        "정방향": meaning_upright,
                        "역방향": meaning_reversed,
                        "조언": advice
                    }
                    with open("card_meanings.json", "w", encoding="utf-8") as f:
                        json.dump(card_meanings, f, ensure_ascii=False, indent=2)
                    st.success("카드 설명이 저장되었습니다.")

            if selected_card in card_meanings:
                if st.button("❌ 이 카드의 설명 삭제"):
                    del card_meanings[selected_card]
                    with open("card_meanings.json", "w", encoding="utf-8") as f:
                        json.dump(card_meanings, f, ensure_ascii=False, indent=2)
                    st.success("해당 카드의 해석이 삭제되었습니다.")

    # ✅ 메뉴 버튼들 - 폼 기반
    with st.form("menu_form"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            start_3card = st.form_submit_button("🔮 3카드 보기")
        with col2:
            start_onecard = st.form_submit_button("✨ 원카드")
        with col3:
            start_choice = st.form_submit_button("🔀 양자택일")
        with col4:
            start_advice = st.form_submit_button("🗣 오늘의 조언")

        if start_3card:
            st.session_state.cards = draw_cards(3)
            st.session_state.extra_cards = [None, None, None]
            st.session_state.mode = "3카드"
        elif start_onecard:
            st.session_state.cards = draw_cards(1)
            st.session_state.extra_cards = [None]
            st.session_state.mode = "원카드"
        elif start_choice:
            st.session_state.cards = []
            st.session_state.extra_cards = [None, None]
            st.session_state.mode = "양자택일"
            st.session_state.question_yes = ""
            st.session_state.question_no = ""
        elif start_advice:
            st.session_state.cards = draw_cards(1)
            st.session_state.extra_cards = [None]
            st.session_state.mode = "조언카드"

    download_history()

    # ✅ 모드별 결과 처리
    if st.session_state.mode == "3카드":
        st.subheader("🔮 3카드 결과")
        for i, (card, direction) in enumerate(st.session_state.cards):
            show_card(card, direction)
            st.markdown(interpret_result(card, direction))

    elif st.session_state.mode == "원카드":
        st.subheader("✨ 원카드 결과")
        card, direction = st.session_state.cards[0]
        show_card(card, direction)
        st.markdown(interpret_result(card, direction))

    elif st.session_state.mode == "조언카드":
        st.subheader("🗣 오늘의 조언 결과")
        card, direction = st.session_state.cards[0]
        show_card(card, direction)
        st.markdown(interpret_result(card, direction))

    elif st.session_state.mode == "양자택일":
        st.subheader("🔀 양자택일")
        with st.form("choice_form"):
            st.session_state.question_yes = st.text_input("선택 1 질문 입력 (예: 계속 다닐까?)", st.session_state.question_yes)
            st.session_state.question_no = st.text_input("선택 2 질문 입력 (예: 이직할까?)", st.session_state.question_no)
            submit_questions = st.form_submit_button("🃏 카드 뽑기")

            if submit_questions and st.session_state.question_yes and st.session_state.question_no:
                st.session_state.cards = draw_cards(2)
                st.session_state.extra_cards = [None, None]

        if st.session_state.cards:
            st.markdown(f"### 선택 1: {st.session_state.question_yes}")
            card1, dir1 = st.session_state.cards[0]
            show_card(card1, dir1)
            st.markdown(interpret_result(card1, dir1))

            st.markdown(f"### 선택 2: {st.session_state.question_no}")
            card2, dir2 = st.session_state.cards[1]
            show_card(card2, dir2)
            st.markdown(interpret_result(card2, dir2))

            if st.button("✅ 최종 결론 카드 보기"):
                final_card = draw_cards(1)[0]
                st.markdown("### 🧭 최종 결론")
                show_card(final_card[0], final_card[1])
                st.markdown(interpret_result(final_card[0], final_card[1]))

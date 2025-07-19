import streamlit as st
from PIL import Image
import os
import random

# ✅ 허용된 이메일 목록
ALLOWED_USERS = ["cotty79@naver.com", "teleecho@naver.com"]

# ✅ 로그인 처리
if "user" not in st.session_state:
    st.markdown("## 🔐 로그인")
    email = st.text_input("이메일을 입력하세요")
    if st.button("로그인"):
        if email in ALLOWED_USERS:
            st.session_state.user = email
            st.success(f"{email} 님 환영합니다.")
            st.rerun()
        else:
            st.error("접근 권한이 없습니다.")
    st.stop()

# 세션 초기화
if 'mode' not in st.session_state:
    st.session_state.mode = None
if 'cards' not in st.session_state:
    st.session_state.cards = []
if 'reversed' not in st.session_state:
    st.session_state.reversed = []
if 'extra_cards' not in st.session_state:
    st.session_state.extra_cards = []
if 'advice_card' not in st.session_state:
    st.session_state.advice_card = None
if 'question_yes' not in st.session_state:
    st.session_state.question_yes = ""
if 'question_no' not in st.session_state:
    st.session_state.question_no = ""

img_folder = "카드이미지"

# 카드 리스트 불러오기
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

# 카드 표시 함수
def show_card(card, direction, width=200):
    img = Image.open(os.path.join(img_folder, card))
    if direction == "역방향":
        img = img.rotate(180)
    st.image(img, caption=f"{card} ({direction})", width=width)

# 메인화면
if st.session_state.mode is None:
    st.markdown("---")
    st.markdown("<h2 style='text-align:center;'>🌗 동양타로</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>\"한 장의 카드가 내 마음을 말하다\"</p>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔮 3카드 보기"):
            st.session_state.cards = draw_cards(3)
            st.session_state.extra_cards = [None, None, None]
            st.session_state.advice_card = None
            st.session_state.mode = "3카드"
    with col2:
        if st.button("✨ 원카드"):
            st.session_state.cards = draw_cards(1)
            st.session_state.extra_cards = [None]
            st.session_state.mode = "원카드"

    col3, col4 = st.columns(2)
    with col3:
        if st.button("🔀 양자택일"):
            st.session_state.cards = draw_cards(2)
            st.session_state.mode = "양자택일"
    with col4:
        if st.button("🗣 오늘의 조언"):
            st.session_state.cards = draw_cards(1)
            st.session_state.extra_cards = [None]
            st.session_state.mode = "조언카드"

elif st.session_state.mode == "3카드":
    st.markdown("## 🃏 3장의 카드")
    cols = st.columns(3)
    for i, (card, direction) in enumerate(st.session_state.cards):
        with cols[i]:
            show_card(card, direction)

    col_buttons = st.columns(3)
    for i, (card, direction) in enumerate(st.session_state.cards):
        if direction == "역방향" and st.session_state.extra_cards[i] is None:
            with col_buttons[i]:
                if st.button(f"🔁 보조카드 ({i+1})"):
                    st.session_state.extra_cards[i] = draw_cards(1)[0]

    col_extras = st.columns(3)
    for i in range(3):
        if st.session_state.extra_cards[i] is not None:
            extra_card, extra_dir = st.session_state.extra_cards[i]
            with col_extras[i]:
                st.markdown("**→ 보조카드**")
                show_card(extra_card, extra_dir)

    st.markdown("---")
    if st.session_state.advice_card is None:
        if st.button("🗣 조언 카드 보기"):
            st.session_state.advice_card = draw_cards(1)[0]

    if st.session_state.advice_card:
        advice_card, advice_dir = st.session_state.advice_card
        st.markdown("### 💡 조언 카드")
        show_card(advice_card, advice_dir)

    st.button("처음으로 ⭯", on_click=lambda: st.session_state.update(mode=None))

elif st.session_state.mode == "원카드":
    st.markdown("## 🃏 한 장의 카드")
    card, direction = st.session_state.cards[0]
    show_card(card, direction)

    if direction == "역방향" and st.session_state.extra_cards[0] is None:
        if st.button("🔁 보조카드"):
            st.session_state.extra_cards[0] = draw_cards(1)[0]

    if st.session_state.extra_cards[0] is not None:
        extra_card, extra_dir = st.session_state.extra_cards[0]
        st.markdown("**→ 보조카드**")
        show_card(extra_card, extra_dir)

    st.button("처음으로 ⭯", on_click=lambda: st.session_state.update(mode=None))

elif st.session_state.mode == "조언카드":
    st.markdown("## 🗣 오늘의 조언 카드")
    card, direction = st.session_state.cards[0]
    show_card(card, direction)

    if direction == "역방향" and st.session_state.extra_cards[0] is None:
        if st.button("🔁 보조카드"):
            st.session_state.extra_cards[0] = draw_cards(1)[0]

    if st.session_state.extra_cards[0] is not None:
        extra_card, extra_dir = st.session_state.extra_cards[0]
        st.markdown("**→ 보조카드**")
        show_card(extra_card, extra_dir)

    st.button("처음으로 ⭯", on_click=lambda: st.session_state.update(mode=None))

elif st.session_state.mode == "양자택일":
    st.markdown("## 🔀 양자택일 카드")

    st.session_state.question_yes = st.text_input("Yes에 해당하는 질문을 입력하세요:", value=st.session_state.question_yes)
    st.session_state.question_no = st.text_input("No에 해당하는 질문을 입력하세요:", value=st.session_state.question_no)

    if len(st.session_state.cards) < 2:
        st.session_state.cards = draw_cards(2)

    cols = st.columns(2)
    for i, (card, direction) in enumerate(st.session_state.cards):
        with cols[i]:
            label = "Yes" if i == 0 else "No"
            st.markdown(f"#### {label} - {st.session_state.question_yes if i == 0 else st.session_state.question_no}")
            show_card(card, direction)

    st.button("처음으로 ⭯", on_click=lambda: st.session_state.update(mode=None))

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
    st.markdown("<h2 style='text-align:center;'>\ud83c\udf17 \ub3d9\uc591\ud0c0\ub85c</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>\"\ud55c \uc7a5\uc758 \uce74\ub4dc\uac00 \ub0b4 \ub9d0\uc744 \ub9d0\ud558\ub2e4\"</p>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("\ud83d\udd2e 3\uce74\ub4dc \ubcf4\uae30"):
            st.session_state.cards = draw_cards(3)
            st.session_state.extra_cards = [None, None, None]
            st.session_state.advice_card = None
            st.session_state.mode = "3\uce74\ub4dc"
    with col2:
        if st.button("\u2728 \uc6d0\uce74\ub4dc"):
            st.session_state.cards = draw_cards(1)
            st.session_state.extra_cards = [None]
            st.session_state.mode = "\uc6d0\uce74\ub4dc"

    col3, col4 = st.columns(2)
    with col3:
        if st.button("\ud83d\udd00 \uc591\uc790\ud0dd\uc77c"):
            st.session_state.mode = "\uc591\uc790\ud0dd\uc77c"
    with col4:
        if st.button("\ud83d\udd23 \uc624\ub298\uc758 \uc870\uc5b8"):
            st.session_state.cards = draw_cards(1)
            st.session_state.extra_cards = [None]
            st.session_state.mode = "\uc870\uc5b8\uce74\ub4dc"

elif st.session_state.mode == "3\uce74\ub4dc":
    st.markdown("## \ud83c\udccf 3\uc7a5\uc758 \uce74\ub4dc")
    cols = st.columns(3)
    for i, (card, direction) in enumerate(st.session_state.cards):
        with cols[i]:
            show_card(card, direction)

    col_buttons = st.columns(3)
    for i, (card, direction) in enumerate(st.session_state.cards):
        if direction == "\uc5ed\ubc29\ud5a5" and st.session_state.extra_cards[i] is None:
            with col_buttons[i]:
                if st.button(f"\ud83d\udd01 \ubcf4\uc870\uce74\ub4dc ({i+1})"):
                    st.session_state.extra_cards[i] = draw_cards(1)[0]

    col_extras = st.columns(3)
    for i in range(3):
        if st.session_state.extra_cards[i] is not None:
            extra_card, extra_dir = st.session_state.extra_cards[i]
            with col_extras[i]:
                st.markdown("**\u2192 \ubcf4\uc870\uce74\ub4dc**")
                show_card(extra_card, extra_dir)

    st.markdown("---")
    if st.session_state.advice_card is None:
        if st.button("\ud83d\udd23 \uc870\uc5b8 \uce74\ub4dc \ubcf4\uae30"):
            st.session_state.advice_card = draw_cards(1)[0]

    if st.session_state.advice_card:
        advice_card, advice_dir = st.session_state.advice_card
        st.markdown("### \ud83d\udca1 \uc870\uc5b8 \uce74\ub4dc")
        show_card(advice_card, advice_dir)

    st.button("\ucc98\uc74c\uc73c\ub85c \u2baf", on_click=lambda: st.session_state.update(mode=None))

elif st.session_state.mode == "\uc6d0\uce74\ub4dc":
    st.markdown("## \ud83c\udccf \ud55c \uc7a5\uc758 \uce74\ub4dc")
    card, direction = st.session_state.cards[0]
    show_card(card, direction)

    if direction == "\uc5ed\ubc29\ud5a5" and st.session_state.extra_cards[0] is None:
        if st.button("\ud83d\udd01 \ubcf4\uc870\uce74\ub4dc"):
            st.session_state.extra_cards[0] = draw_cards(1)[0]

    if st.session_state.extra_cards[0] is not None:
        extra_card, extra_dir = st.session_state.extra_cards[0]
        st.markdown("**\u2192 \ubcf4\uc870\uce74\ub4dc**")
        show_card(extra_card, extra_dir)

    st.button("\ucc98\uc74c\uc73c\ub85c \u2baf", on_click=lambda: st.session_state.update(mode=None))

elif st.session_state.mode == "\uc870\uc5b8\uce74\ub4dc":
    st.markdown("## \ud83d\udd23 \uc624\ub298\uc758 \uc870\uc5b8 \uce74\ub4dc")
    card, direction = st.session_state.cards[0]
    show_card(card, direction)

    if direction == "\uc5ed\ubc29\ud5a5" and st.session_state.extra_cards[0] is None:
        if st.button("\ud83d\udd01 \ubcf4\uc870\uce74\ub4dc"):
            st.session_state.extra_cards[0] = draw_cards(1)[0]

    if st.session_state.extra_cards[0] is not None:
        extra_card, extra_dir = st.session_state.extra_cards[0]
        st.markdown("**\u2192 \ubcf4\uc870\uce74\ub4dc**")
        show_card(extra_card, extra_dir)

    st.button("\ucc98\uc74c\uc73c\ub85c \u2baf", on_click=lambda: st.session_state.update(mode=None))

elif st.session_state.mode == "\uc591\uc790\ud0dd\uc77c":
    st.markdown("## \ud83d\udd00 \uc591\uc790\ud0dd\uc77c \uce74\ub4dc")

    st.session_state.question_yes = st.text_input("Yes\uc5d0 \ud574\ub2f9\ud558\ub294 \uc9c8\ubb38\uc744 \uc785\ub825\ud558\uc138\uc694:", value=st.session_state.question_yes)
    st.session_state.question_no = st.text_input("No\uc5d0 \ud574\ub2f9\ud558\ub294 \uc9c8\ubb38\uc744 \uc785\ub825\ud558\uc138\uc694:", value=st.session_state.question_no)

    if len(st.session_state.cards) < 2:
        if st.button("\ud83d\udd2e \uce74\ub4dc \ubcf4\uae30"):
            st.session_state.cards = draw_cards(2)
            st.rerun()

    def interpret_result(direction):
        if direction == "정방향":
            return "\ud83c\udf3f \uac00\ub2a5\uc131\uc774 \ub192\uc2b5\ub2c8\ub2e4. \uc9c4\ud589\uc744 \uace0\ub824\ud574\ubcf4\uc138\uc694."
        else:
            return "\u26a0\ufe0f \uc544\uc9c1\uc740 \uc2dc\uae30\uc0c1\uc870\uc77c \uc218 \uc788\uc2b5\ub2c8\ub2e4. \uc2e0\uc911\ud788 \ud310\ub2e8\ud558\uc138\uc694."

    if len(st.session_state.cards) == 2:
        cols = st.columns(2)
        for i, (card, direction) in enumerate(st.session_state.cards):
            with cols[i]:
                label = "Yes" if i == 0 else "No"
                question = st.session_state.question_yes if i == 0 else st.session_state.question_no
                st.markdown(f"#### {label} - {question}")
                show_card(card, direction)
                interpretation = interpret_result(direction)
                st.markdown(f"**{interpretation}**")

    st.button("\ucc98\uc74c\uc73c\ub85c \u2baf", on_click=lambda: st.session_state.update(mode=None))

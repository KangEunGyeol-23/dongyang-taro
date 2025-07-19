import streamlit as st
from PIL import Image
import os
import random

# ✅ 로그인 허용 이메일 목록
ALLOWED_USERS = ["cotty79@naver.com"]

# ✅ 로그인 처리
if "user" not in st.session_state:
    st.markdown("## 🔐 로그인")
    email = st.text_input("이메일을 입력하세요")
    if st.button("로그인"):
        if email in ALLOWED_USERS:
            st.session_state.user = email
            st.success(f"{email} 님 환영합니다.")
            st.rerun()  # 최신 버전용으로 수정
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

img_folder = "카드이미지"

# 카드 리스트 불러오기
def load_cards():
    if not os.path.exists(img_folder):
        st.error(f"이미지 폴더가 없습니다: {img_folder}")
        return []
    return [f for f in os.listdir(img_folder) if f.lower().endswith(('png', 'jpg', 'jpeg'))]

def draw_cards(n):
    cards = random.sample(load_cards(), n)
    directions = [random.choice(['정방향', '역방향']) for _ in range(n)]
    return list(zip(cards, directions))

# 처음 화면
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
            st.session_state.mode = "3카드"
    with col2:
        if st.button("✨ 원카드"):
            st.session_state.cards = draw_cards(1)
            st.session_state.extra_cards = [None]
            st.session_state.mode = "원카드"

    col3, col4 = st.columns(2)
    with col3:
        if st.button("🔀 양자택일"):
            st.session_state.mode = "양자택일"  # 추후 구현
    with col4:
        if st.button("🗣 오늘의 조언"):
            st.session_state.cards = draw_cards(1)
            st.session_state.extra_cards = [None]
            st.session_state.mode = "조언카드"

# 3카드 보기
elif st.session_state.mode == "3카드":
    st.markdown("## 🃏 3장의 카드")
    cols = st.columns(3)
    for i, (card, direction) in enumerate(st.session_state.cards):
        with cols[i]:
            img = Image.open(os.path.join(img_folder, card))
            if direction == "역방향":
                img = img.rotate(180)
            st.image(img, caption=f"{card} ({direction})", use_column_width=True)

            if direction == "역방향" and st.session_state.extra_cards[i] is None:
                if st.button(f"🔁 보조카드 ({i+1})"):
                    st.session_state.extra_cards[i] = draw_cards(1)[0]

            if st.session_state.extra_cards[i] is not None:
                extra_card, extra_dir = st.session_state.extra_cards[i]
                st.markdown("**→ 보조카드**")
                extra_img = Image.open(os.path.join(img_folder, extra_card))
                if extra_dir == "역방향":
                    extra_img = extra_img.rotate(180)
                st.image(extra_img, caption=f"{extra_card} ({extra_dir})", use_column_width=True)

    st.button("처음으로 ⭯", on_click=lambda: st.session_state.update(mode=None))

# 원카드
elif st.session_state.mode == "원카드":
    st.markdown("## 🃏 한 장의 카드")
    card, direction = st.session_state.cards[0]
    img = Image.open(os.path.join(img_folder, card))
    if direction == "역방향":
        img = img.rotate(180)
    st.image(img, caption=f"{card} ({direction})", use_column_width=True)

    if direction == "역방향" and st.session_state.extra_cards[0] is None:
        if st.button("🔁 보조카드"):
            st.session_state.extra_cards[0] = draw_cards(1)[0]

    if st.session_state.extra_cards[0] is not None:
        extra_card, extra_dir = st.session_state.extra_cards[0]
        extra_img = Image.open(os.path.join(img_folder, extra_card))
        if extra_dir == "역방향":
            extra_img = extra_img.rotate(180)
        st.image(extra_img, caption=f"{extra_card} ({extra_dir})", use_column_width=True)

    st.button("처음으로 ⭯", on_click=lambda: st.session_state.update(mode=None))

# 조언카드
elif st.session_state.mode == "조언카드":
    st.markdown("## 🗣 오늘의 조언 카드")
    card, direction = st.session_state.cards[0]
    img = Image.open(os.path.join(img_folder, card))
    if direction == "역방향":
        img = img.rotate(180)
    st.image(img, caption=f"{card} ({direction})", use_column_width=True)

    if direction == "역방향" and st.session_state.extra_cards[0] is None:
        if st.button("🔁 보조카드"):
            st.session_state.extra_cards[0] = draw_cards(1)[0]

    if st.session_state.extra_cards[0] is not None:
        extra_card, extra_dir = st.session_state.extra_cards[0]
        extra_img = Image.open(os.path.join(img_folder, extra_card))
        if extra_dir == "역방향":
            extra_img = extra_img.rotate(180)
        st.image(extra_img, caption=f"{extra_card} ({extra_dir})", use_column_width=True)

    st.button("처음으로 ⭯", on_click=lambda: st.session_state.update(mode=None))

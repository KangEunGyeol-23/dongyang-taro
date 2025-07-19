import streamlit as st
from PIL import Image
import os
import random

# 📍 카드 이미지 폴더 경로
img_folder = "카드이미지"

# 📍 카드 해설 사전 (임시)
card_meanings = {
    "The Fool.jpg": "새로운 시작과 자유를 상징합니다.",
    "The Magician.jpg": "의지와 창조력을 나타냅니다.",
    "The Tower.jpg": "충격과 예기치 않은 변화를 의미합니다.",
    "Justice.jpg": "공정함과 균형을 상징합니다.",
    # 필요한 카드들 추가 가능
}

# 📍 카드 이미지 불러오기 함수
def load_images():
    files = [f for f in os.listdir(img_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return sorted(files)

# 📍 중복 없이 카드 1장 뽑기 함수 (이미 뽑힌 카드 제외)
def draw_unique_card(used_cards):
    choices = [card for card in load_images() if card not in used_cards]
    if not choices:
        return None, False
    card = random.choice(choices)
    is_reversed = random.choice([True, False])
    used_cards.append(card)
    return card, is_reversed

# 📍 카드 이미지 표시 함수
def show_card(card, is_reversed, caption):
    img_path = os.path.join(img_folder, card)
    img = Image.open(img_path)
    if is_reversed:
        img = img.rotate(180)
        caption += " (역방향)"
    st.image(img, use_container_width=False, width=220)
    meaning = card_meanings.get(card, "이 카드의 해설은 준비 중입니다.")
    st.markdown(f"""
        <div style='text-align: center; margin-top: 6px; font-size: 13px; color: #eee; font-style: italic;'>🔍 {meaning}</div>
    """, unsafe_allow_html=True)

# 📍 배경 이미지 스타일 삽입
st.set_page_config(page_title="양자택일 타로", layout="centered")

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("file=./background.png");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stImage > img {{
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
    }}
    .button-container {{
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 20px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align:center; color:white;'>🔮 양자택일 타로</h1>", unsafe_allow_html=True)

# 📍 사용자 질문 입력 전 카드 뽑기 차단
if "show_cards" not in st.session_state:
    st.session_state.show_cards = False

option1 = st.text_input("선택지 1 입력", placeholder="예: 이직하기")
option2 = st.text_input("선택지 2 입력", placeholder="예: 지금 회사에 남기")

if not st.session_state.show_cards:
    if st.button("✨ 질문 완료 후 카드 뽑기"):
        st.session_state.option1 = option1
        st.session_state.option2 = option2
        st.session_state.used_cards = []
        st.session_state.left_card, st.session_state.left_reversed = draw_unique_card(st.session_state.used_cards)
        st.session_state.left_sub_card = None
        st.session_state.right_card, st.session_state.right_reversed = draw_unique_card(st.session_state.used_cards)
        st.session_state.right_sub_card = None
        st.session_state.advice_card = None
        st.session_state.advice_reversed = False
        st.session_state.advice_drawn = False
        st.session_state.show_cards = True

if st.session_state.show_cards:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"선택 1: {st.session_state.option1 or '입력 안 됨'}")
        show_card(st.session_state.left_card, st.session_state.left_reversed, st.session_state.left_card)
        if st.session_state.left_reversed:
            if st.button("보조카드 보기 (선택 1)") and not st.session_state.left_sub_card:
                st.session_state.left_sub_card = draw_unique_card(st.session_state.used_cards)
            if st.session_state.left_sub_card:
                show_card(st.session_state.left_sub_card[0], st.session_state.left_sub_card[1], "보조카드")

    with col2:
        st.subheader(f"선택 2: {st.session_state.option2 or '입력 안 됨'}")
        show_card(st.session_state.right_card, st.session_state.right_reversed, st.session_state.right_card)
        if st.session_state.right_reversed:
            if st.button("보조카드 보기 (선택 2)") and not st.session_state.right_sub_card:
                st.session_state.right_sub_card = draw_unique_card(st.session_state.used_cards)
            if st.session_state.right_sub_card:
                show_card(st.session_state.right_sub_card[0], st.session_state.right_sub_card[1], "보조카드")

    st.markdown("---")
    if st.button("🧭 조언 카드 뽑기") and not st.session_state.advice_drawn:
        st.session_state.advice_card, st.session_state.advice_reversed = draw_unique_card(st.session_state.used_cards)
        st.session_state.advice_drawn = True

    if st.session_state.advice_drawn:
        st.subheader("✨ 오늘의 조언 카드")
        show_card(st.session_state.advice_card, st.session_state.advice_reversed, "조언카드")

    if st.button("처음으로 ⭯"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]

import streamlit as st
import random
import time
import matplotlib.pyplot as plt
import numpy as np

# 1. 데이터 정의
menu_data = {
    "한식 🇰🇷": ["김치찌개", "비빔밥", "불고기", "제육볶음", "된장찌개"],
    "중식 🇨🇳": ["짜장면", "짬뽕", "탕수육", "마파두부", "볶음밥"],
    "일식 🇯🇵": ["초밥", "라멘", "돈카츠", "규동", "소바"],
    "양식 🍕": ["파스타", "피자", "스테이크", "리조또", "햄버거"],
    "분식 🍢": ["떡볶이", "튀김", "순대", "라면", "김밥"]
}

st.set_page_config(page_title="진짜 메뉴 룰렛", layout="centered")
st.title("🎯 메뉴 결정 룰렛 (이름 표시)")

# --- 사이드바 설정 ---
st.sidebar.title("🍔 메뉴 설정")

selected_categories = st.sidebar.multiselect(
    "카테고리를 고르세요",
    options=list(menu_data.keys()),
    default=list(menu_data.keys())[0],
    key="cat_select"
)

all_menus = []
for c in selected_categories:
    all_menus.extend(menu_data[c])

final_candidates = st.sidebar.multiselect(
    "후보 메뉴 확인",
    options=all_menus,
    default=all_menus,
    key=f"menu_select_{selected_categories}"
)

# --- 룰렛 시각화 함수 ---
def draw_roulette(items, offset=0):
    num_items = len(items)
    if num_items == 0: return None
    
    # 폰트 설정 (에러 방지를 위해 기본 폰트 사용하되 크기 조정)
    plt.rcParams['font.family'] = 'Malgun Gothic' # 윈도우 한글 폰트
    
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_alpha(0) # 배경 투명
    
    sizes = [1] * num_items
    colors = plt.cm.get_cmap('Set3', num_items).colors
    
    # 룰렛 판 그리기
    # labels=items 를 사용하면 판 밖에 글자가 써지므로, 직접 안에 넣기 위해 autopct 등을 활용하거나 수동 배치합니다.
    wedges, _ = ax.pie(
        sizes, 
        startangle=90 + offset, 
        colors=colors,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2}
    )
    
    # [추가] 메뉴명 텍스트를 각 조각 안에 배치
    for i, wedge in enumerate(wedges):
        # 조각의 각도 계산
        ang = (wedge.theta2 + wedge.theta1) / 2.
        
        # 텍스트 위치 (원 중심에서 0.7 지점)
        x = 0.7 * np.cos(np.deg2rad(ang))
        y = 0.7 * np.sin(np.deg2rad(ang))
        
        # 텍스트가 판과 함께 회전하도록 설정
        ax.text(x, y, items[i], 
                ha='center', va='center', 
                fontsize=11, weight='bold',
                rotation=ang - 180 if 90 < ang < 270 else ang) # 읽기 편하게 회전 각도 조정

    # 맨 위 화살표 (고정)
    ax.annotate('', xy=(0, 1.05), xytext=(0, 1.25),
                arrowprops=dict(facecolor='red', shrink=0.05, width=12, headwidth=25))
    
    # 중앙 원 (장식)
    center_circle = plt.Circle((0,0), 0.1, color='white', zorder=10)
    ax.add_artist(center_circle)
    
    return fig

# --- 메인 실행 ---
if not final_candidates:
    st.info("왼쪽 사이드바에서 카테고리를 선택해 주세요!")
else:
    placeholder = st.empty()
    # 첫 로드 시 0도 상태로 표시
    placeholder.pyplot(draw_roulette(final_candidates, offset=0))

    if st.button("🚀 룰렛 돌리기!"):
        # 애니메이션: 총 40프레임 동안 회전
        total_frames = 40
        current_rotation = 0
        speed = 50 
        
        for i in range(total_frames):
            current_rotation += speed
            speed *= 0.93 # 감속 효과
            
            with placeholder:
                fig = draw_roulette(final_candidates, offset=current_rotation)
                st.pyplot(fig)
                plt.close(fig) # 메모리 관리
            time.sleep(0.05)
        
        # 최종 당첨자 계산
        final_angle = current_rotation % 360
        # 화살표가 12시 방향(90도)에 고정되어 있으므로 그에 따른 인덱스 계산
        # 파이차트는 반시계 방향으로 그려지므로 (360 - offset) 기준
        winner_idx = int(((360 - final_angle) % 360) / (360 / len(final_candidates)))
        winner = final_candidates[winner_idx]
        
        st.balloons()
        st.markdown(f"""
            <div style="text-align: center; margin-top: 20px;">
                <h3 style="color: gray;">오늘의 당첨 메뉴는?</h3>
                <h1 style="color: #ff4b4b; font-size: 60px; border: 5px solid #ff4b4b; border-radius: 15px; display: inline-block; padding: 10px 30px;">
                    {winner}
                </h1>
            </div>
        """, unsafe_allow_html=True)
import streamlit as st
import random
import time
import streamlit.components.v1 as components


st.set_page_config(layout="wide")

WIDTH = 800
HEIGHT = 500

# ---------- INIT STATE ----------
if "player_x" not in st.session_state:
    st.session_state.player_x = WIDTH // 2
    st.session_state.bullets = []
    st.session_state.enemies = []
    st.session_state.score = 0
    st.session_state.health = 100
    st.session_state.last_spawn = time.time()

# ---------- UI ----------
st.title("Streamlit Shooter Game")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("Left"):
        st.session_state.player_x -= 30

with c2:
    if st.button("Shoot"):
        st.session_state.bullets.append(
            [st.session_state.player_x, HEIGHT - 40]
        )

with c3:
    if st.button("Right"):
        st.session_state.player_x += 30

st.session_state.player_x = max(0, min(WIDTH - 30, st.session_state.player_x))

# ---------- SPAWN ENEMIES ----------
if time.time() - st.session_state.last_spawn > 1:
    st.session_state.enemies.append(
        [random.randint(20, WIDTH - 40), 0]
    )
    st.session_state.last_spawn = time.time()

# ---------- UPDATE BULLETS ----------
for bullet in st.session_state.bullets:
    bullet[1] -= 15
st.session_state.bullets = [
    b for b in st.session_state.bullets if b[1] > 0
]

# ---------- UPDATE ENEMIES ----------
for enemy in st.session_state.enemies:
    enemy[1] += 5
    if enemy[1] > HEIGHT:
        st.session_state.health -= 10

# ---------- COLLISIONS ----------
for bullet in st.session_state.bullets[:]:
    for enemy in st.session_state.enemies[:]:
        if abs(bullet[0] - enemy[0]) < 20 and abs(bullet[1] - enemy[1]) < 20:
            st.session_state.bullets.remove(bullet)
            st.session_state.enemies.remove(enemy)
            st.session_state.score += 10
            break

# ---------- DRAW ----------
html = f"""
<div style="position:relative;width:{WIDTH}px;height:{HEIGHT}px;background:black;">

    <div style="
        position:absolute;
        left:{st.session_state.player_x}px;
        bottom:20px;
        width:30px;
        height:20px;
        background:blue;">
    </div>

    {''.join(
        f'''
        <div style="
            position:absolute;
            left:{b[0]}px;
            top:{b[1]}px;
            width:5px;
            height:10px;
            background:green;">
        </div>
        '''
        for b in st.session_state.bullets
    )}

    {''.join(
        f'''
        <div style="
            position:absolute;
            left:{e[0]}px;
            top:{e[1]}px;
            width:25px;
            height:20px;
            background:red;">
        </div>
        '''
        for e in st.session_state.enemies
    )}

</div>
"""

components.html(html, height=HEIGHT + 20)


st.write(f"Health: {st.session_state.health} | Score: {st.session_state.score}")

if st.session_state.health <= 0:
    st.error("GAME OVER")
    st.stop()

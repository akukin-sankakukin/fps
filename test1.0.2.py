import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection # ★高速描画用

# --- 1. 設定と数学関数 ---

STEP_ANGLE = 2 
angles_deg = np.arange(0, 360, STEP_ANGLE)

# 初期位置
current_origin = [0, -5] 
MAX_SCAN_LENGTH = 20.0
PROJECTION_CONSTANT = 10.0

def f(x):
    return 0.1 * x**2

def df(x):
    return 0.2 * x

def get_distance_to_curve(theta_rad, x0, y0):
    r = 1.0
    for _ in range(8): # 精度を少し犠牲にしてループを減らす(8回で十分)
        x_curr = x0 + r * np.cos(theta_rad)
        g_val = f(x_curr) - (y0 + r * np.sin(theta_rad))
        dg_val = df(x_curr) * np.cos(theta_rad) - np.sin(theta_rad)
        
        if abs(dg_val) < 1e-6: return None
        r_new = r - g_val / dg_val
        if abs(r_new - r) < 1e-4: # 許容誤差も少し緩める
            return r_new if r_new > 0 else None
        r = r_new
    return None

# --- 2. 描画更新用関数 ---

def update_plot():
    ax1.cla()
    ax2.cla()
    
    px, py = current_origin
    
    # 計算用配列
    rads = np.deg2rad(angles_deg)
    
    # 結果格納用リスト
    segments_hit = []   # 交点ありの線
    segments_miss = []  # 交点なしの線
    cross_points_x = [] # 交点のX座標
    cross_points_y = [] # 交点のY座標
    heights = []        # 壁の高さ
    
    # 計算ループ
    for rad in rads:
        r = get_distance_to_curve(rad, px, py)
        
        # 描画用の座標計算
        cos_t = np.cos(rad)
        sin_t = np.sin(rad)
        
        if r is not None and 0 < r <= MAX_SCAN_LENGTH:
            # 交点あり
            cx = px + r * cos_t
            cy = py + r * sin_t
            
            segments_hit.append([(px, py), (cx, cy)])
            cross_points_x.append(cx)
            cross_points_y.append(cy)
            
            safe_r = max(r, 0.5)
            heights.append(PROJECTION_CONSTANT / safe_r)
        else:
            # 交点なし（最大長まで）
            sx = px + MAX_SCAN_LENGTH * cos_t
            sy = py + MAX_SCAN_LENGTH * sin_t
            segments_miss.append([(px, py), (sx, sy)])
            heights.append(0) # 壁なし

    # --- Graph 1: Top View (LineCollectionで高速化) ---
    x_line = np.linspace(-20, 20, 100) # 点数削減
    ax1.plot(x_line, f(x_line), color='black', linewidth=2)
    ax1.scatter(px, py, color='red', s=100, zorder=10)

    # 交点ありの線を一括描画
    if segments_hit:
        lc_hit = LineCollection(segments_hit, colors='green', alpha=0.3, linewidth=0.5)
        ax1.add_collection(lc_hit)
        # 交点も一括描画
        ax1.scatter(cross_points_x, cross_points_y, color='blue', s=10, zorder=5, alpha=0.6)

    # 交点なしの線を一括描画
    if segments_miss:
        lc_miss = LineCollection(segments_miss, colors='green', alpha=0.05, linewidth=0.5, linestyles='--')
        ax1.add_collection(lc_miss)

    ax1.set_title(f"Top View (Pos: {px:.1f}, {py:.1f})")
    ax1.set_aspect('equal')
    ax1.set_xlim(-20, 20)
    ax1.set_ylim(-10, 20)
    ax1.grid(True, alpha=0.3)

    # --- Graph 2: FPS View (fill_betweenで高速化) ---
    x_pos = np.arange(len(angles_deg))
    h_array = np.array(heights)
    
    # barの代わりにfill_betweenを使う（爆速）
    # step='mid'でカクカクしたレトロ感を維持
    ax2.fill_between(x_pos, -h_array, h_array*2, step='mid', color="#FFFFFF", alpha=1.0)
    
    ax2.set_facecolor('#222222')
    ax2.axhline(0, color='black', linewidth=1)
    
    ax2.set_title("Player View (High Speed)")
    ax2.set_ylim(-15, 15)
    ax2.set_xticks([])
    ax2.invert_xaxis() # 反転維持

    plt.draw()

# --- 3. イベントハンドラ ---

def on_key(event):
    step = 0.5
    if event.key == 'up':    current_origin[1] += step
    elif event.key == 'down':  current_origin[1] -= step
    elif event.key == 'right': current_origin[0] += step
    elif event.key == 'left':  current_origin[0] -= step
    update_plot()

# --- 4. メイン ---

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.canvas.mpl_connect('key_press_event', on_key)
update_plot()
plt.show()
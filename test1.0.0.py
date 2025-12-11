import numpy as np
import matplotlib.pyplot as plt

# 1. 設定
origin = (0, -2)  # 任意の点P (x0, y0)
angles_deg = np.arange(0, 360, 30)  # 0度から330度まで30度刻み
MAX_SCAN_LENGTH = 15.0 # 可視化線の一定長さ
PROJECTION_CONSTANT = 10.0 # 反比例計算用の定数（壁の高さ係数）

# 対象の曲線関数 f(x) と その導関数 f'(x)
# 例: y = 0.1 * x^2
def f(x):
    return 0.1 * x**2

def df(x):
    return 0.2 * x

# 2. ニュートン法による距離計算
def get_distance_to_curve(theta_rad, x0, y0):
    r = 1.0  # 初期値
    for _ in range(20): # 収束回数を少し多めに
        # 現在のrでの先端のx座標
        x_curr = x0 + r * np.cos(theta_rad)
        
        # 関数 g(r) = f(x) - y の値（0にしたい値）
        g_val = f(x_curr) - (y0 + r * np.sin(theta_rad))
        
        # g(r)の微分 g'(r)
        dg_val = df(x_curr) * np.cos(theta_rad) - np.sin(theta_rad)
        
        # 接線の傾きが0に近い（計算不能）場合は中断
        if abs(dg_val) < 1e-6:
            return None
            
        # 更新
        r_new = r - g_val / dg_val
        
        if abs(r_new - r) < 1e-6: # 収束判定
            return r_new if r_new > 0 else None
        r = r_new
    return None

# 3. 計算実行
results = []
scan_lines = []

for deg in angles_deg:
    rad = np.deg2rad(deg)
    
    # 可視化用の一定長の線の座標を計算
    scan_x = origin[0] + MAX_SCAN_LENGTH * np.cos(rad)
    scan_y = origin[1] + MAX_SCAN_LENGTH * np.sin(rad)
    scan_lines.append((scan_x, scan_y))
    
    # 距離計算
    r = get_distance_to_curve(rad, origin[0], origin[1])
    
    height = 0
    cross_pt = None
    
    # 有効な距離かどうか判定（正の値、かつ最大探索範囲内）
    if r is not None and 0 < r <= MAX_SCAN_LENGTH:
        cross_x = origin[0] + r * np.cos(rad)
        cross_y = origin[1] + r * np.sin(rad)
        cross_pt = (cross_x, cross_y)
        
        # 反比例の計算 (距離が近いほど値が大きい)
        # 0除算防止のため小さな値を加えるか、最小値を制限する
        safe_r = max(r, 0.1)
        height = PROJECTION_CONSTANT / safe_r
    
    results.append({
        'deg': deg,
        'cross_point': cross_pt,
        'height': height
    })

# 4. グラフ描画
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Graph 1: 2D Top View ---
# 曲線の描画
x_line = np.linspace(-15, 15, 200)
ax1.plot(x_line, f(x_line), label='Curve y=0.1x^2', color='black', linewidth=1.5)

# 点Pの描画
ax1.scatter(*origin, color='red', label='Point P', zorder=10, s=80)

# 一定長の可視化線と交点の描画
for i, deg in enumerate(angles_deg):
    # 緑色の点線（一定の長さ）
    sx, sy = scan_lines[i]
    ax1.plot([origin[0], sx], [origin[1], sy], 'g--', alpha=0.3)
    
    # 交点がある場合は青い点を打つ
    res = results[i]
    if res['cross_point']:
        cx, cy = res['cross_point']
        ax1.scatter(cx, cy, color='blue', zorder=5)

ax1.set_title("Graph 1: 2D Raycast (Top View)")
ax1.set_aspect('equal')
ax1.grid(True)
ax1.set_xlim(-15, 15)
ax1.set_ylim(-5, 20)
ax1.legend(loc='upper right')

# --- Graph 2: Pseudo 3D View (Bar Chart) ---
angles = [r['deg'] for r in results]
heights = [r['height'] for r in results]
x_pos = np.arange(len(angles))

# Y軸の中心を0にして、正負に同じ長さの棒を描画
# これにより、視野中央から上下に壁が伸びているように見える（FPSスタイル）
ax2.bar(x_pos, heights, width=0.8, color='cornflowerblue', alpha=0.8, label='Wall Height')
ax2.bar(x_pos, [-h for h in heights], width=0.8, color='cornflowerblue', alpha=0.8)

# 中央線の描画
ax2.axhline(0, color='black', linewidth=1)

# ラベル設定
ax2.set_xticks(x_pos)
ax2.set_xticklabels(angles)
ax2.set_title("Graph 2: Projected Wall Height (1/Distance)")
ax2.set_xlabel("Angle (degrees)")
ax2.set_ylabel("Height Value")

# Y軸のスケール調整（見栄え良く）
max_h = max(heights) if heights and max(heights) > 0 else 1.0
ax2.set_ylim(-max_h * 1.1, max_h * 1.1)
ax2.grid(True, axis='y', linestyle=':', alpha=0.6)

plt.tight_layout()
plt.show()
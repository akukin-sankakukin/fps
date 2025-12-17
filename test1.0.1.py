import numpy as np
import matplotlib.pyplot as plt

# --- 1. 設定と数学関数 ---

# 初期位置
current_origin = [0, -5]  # リストにして変更可能にする
STEP_ANGLE = 2  # ここで密度を調整
angles_deg = np.arange(0, 360, STEP_ANGLE)
# angles_deg = np.arange(0, 360, 15)  # 少し刻みを細かくしました（30->15）
MAX_SCAN_LENGTH = 20.0
PROJECTION_CONSTANT = 10.0

# 対象の曲線関数 f(x) と その導関数 f'(x)
def f(x):
    return 0.1 * x**2

def df(x):
    return 0.2 * x

# ニュートン法による距離計算
def get_distance_to_curve(theta_rad, x0, y0):
    r = 1.0
    for _ in range(10):
        x_curr = x0 + r * np.cos(theta_rad)
        g_val = f(x_curr) - (y0 + r * np.sin(theta_rad))
        dg_val = df(x_curr) * np.cos(theta_rad) - np.sin(theta_rad)
        
        if abs(dg_val) < 1e-6:
            return None
        
        r_new = r - g_val / dg_val
        if abs(r_new - r) < 1e-6:
            return r_new if r_new > 0 else None
        r = r_new
    return None

# --- 2. 描画更新用関数 ---

def update_plot():
    # 画面をクリア
    ax1.cla()
    ax2.cla()
    
    px, py = current_origin
    
    # 計算実行
    results = []
    scan_lines = []
    
    for deg in angles_deg:
        rad = np.deg2rad(deg)
        
        # 可視化用の線の終点（描画用）
        scan_x = px + MAX_SCAN_LENGTH * np.cos(rad)
        scan_y = py + MAX_SCAN_LENGTH * np.sin(rad)
        scan_lines.append((scan_x, scan_y))
        
        # 距離計算
        r = get_distance_to_curve(rad, px, py)
        
        height = 0
        cross_pt = None
        
        if r is not None and 0 < r <= MAX_SCAN_LENGTH:
            cross_x = px + r * np.cos(rad)
            cross_y = py + r * np.sin(rad)
            cross_pt = (cross_x, cross_y)
            
            safe_r = max(r, 0.5) # 壁に近づきすぎた時の補正
            height = PROJECTION_CONSTANT / safe_r
        
        results.append({
            'deg': deg,
            'cross_point': cross_pt,
            'height': height
        })

    # --- Graph 1: 2D Top View の再描画 ---
    x_line = np.linspace(-20, 20, 200)
    ax1.plot(x_line, f(x_line), color='black', linewidth=1.5, label='Wall')
    ax1.scatter(px, py, color='red', s=100, label='Player', zorder=10) # プレイヤー
    
    # 線と交点の描画
    for i, res in enumerate(results):
        sx, sy = scan_lines[i]
        # 交点がある場合とない場合で線の色を変えるなど工夫可能
        if res['cross_point']:
            cx, cy = res['cross_point']
            ax1.plot([px, cx], [py, cy], 'g-', alpha=0.4, linewidth=1)
            ax1.scatter(cx, cy, color='blue', s=20, zorder=5)
        else:
            ax1.plot([px, sx], [py, sy], 'g--', alpha=0.1, linewidth=1)

    ax1.set_title(f"Top View (Pos: {px:.1f}, {py:.1f})")
    ax1.set_aspect('equal')
    ax1.set_xlim(-20, 20)
    ax1.set_ylim(-10, 20) # 範囲固定
    ax1.grid(True)

    # --- Graph 2: Pseudo 3D View の再描画 ---
    heights = [r['height'] for r in results]
    x_pos = np.arange(len(angles_deg))
    
    # 上下のバーを描画
    ax2.bar(x_pos, heights, width=1.0, color='cornflowerblue', alpha=0.9)
    ax2.bar(x_pos, [-h for h in heights], width=1.0, color='cornflowerblue', alpha=0.9)
    
    # 背景を黒っぽくするとFPS感が出ます
    ax2.set_facecolor('#222222')
    ax2.axhline(0, color='black', linewidth=1)
    
    ax2.set_title("Player View")
    ax2.set_ylim(-15, 15) # Y軸固定（これがないとグラフがガクガクします）
    ax2.set_xticks([]) # X軸のメモリは消して雰囲気重視に

    ax2.invert_xaxis()

    plt.draw() # 描画を反映

# --- 3. キーイベントハンドラ ---

def on_key(event):
    step = 0.5 # 1回の移動量
    
    if event.key == 'up':
        current_origin[1] += step
    elif event.key == 'down':
        current_origin[1] -= step
    elif event.key == 'right':
        current_origin[0] += step
    elif event.key == 'left':
        current_origin[0] -= step
    
    # 再描画関数を呼び出す
    update_plot()

# --- 4. メイン処理 ---

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# キーイベントを接続
fig.canvas.mpl_connect('key_press_event', on_key)

# 初回の描画
update_plot()

plt.show()
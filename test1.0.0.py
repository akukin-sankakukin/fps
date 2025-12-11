import numpy as np
import matplotlib.pyplot as plt

# 1. 設定
origin = (0, 2)  # 任意の点P (x0, y0)
angles_deg = np.arange(0, 360, 30)  # 0度から330度まで30度刻み

# 対象の曲線関数 f(x) と その導関数 f'(x)
# 例: y = 0.1 * x^2
def f(x):
    return 0.1 * x**2

def df(x):
    return 0.2 * x

# 2. ニュートン法による距離計算
def get_distance_to_curve(theta_rad, x0, y0):
    r = 1.0  # 初期値
    for _ in range(10): # 10回繰り返せば十分収束します
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
            return r_new
        r = r_new
    return r

# 3. 計算実行
results = []
for deg in angles_deg:
    rad = np.deg2rad(deg)
    r = get_distance_to_curve(rad, origin[0], origin[1])
    
    if r is not None and r > 0: # 正の距離のみ採用
        cross_x = origin[0] + r * np.cos(rad)
        cross_y = origin[1] + r * np.sin(rad)
        results.append((cross_x, cross_y))
        print(f"角度 {deg:3d}°: 距離 {r:.4f}")

# 4. グラフ描画（確認用）
# 曲線の描画
x_line = np.linspace(-10, 10, 100)
plt.plot(x_line, f(x_line), label='Curve y=0.1x^2')

# 点Pの描画
plt.scatter(*origin, color='red', label='Point P', zorder=5)

# 交点と直線の描画
for rx, ry in results:
    plt.plot([origin[0], rx], [origin[1], ry], 'g--', alpha=0.5) # 直線
    plt.scatter(rx, ry, color='blue') # 交点

plt.grid(True)
plt.legend()
plt.axis('equal') # アスペクト比を1:1に
plt.show()
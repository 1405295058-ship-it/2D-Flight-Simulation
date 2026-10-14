import matplotlib.pyplot as plot
import numpy as np
from pathlib import Path
CHORD = 1.016
X_FIX = - 12.1434
Y_FIX = -24.188

# Case selection
CASE_TYPE = "DomainTest"
CASE_NAME = "3020"

# Path configuration
ROOT = Path(__file__).resolve().parent
CASE_PATH = ROOT / "Case" / CASE_TYPE / CASE_NAME
if not CASE_PATH.is_dir():
    raise FileNotFoundError(
        f"Case directory not found: {CASE_PATH}"
    )

#reference path 
XFOIL_PATH = ROOT / "Reference" / "XFoil" 

# Subdirectories
MESH_PATH = CASE_PATH / "Mesh"
SOLUTION_PATH = CASE_PATH / "Solution"
EXPORT_PATH = CASE_PATH / "Export"




##三元素的打开函数 for coe
def open_fluent_file(x_file_name, y_file_name, skip = 1)->np.array:

    def read_data(filename):
        data = []

        with open(filename, "r") as file:
            for line in file.readlines()[skip:]:
                values = line.split()

                if len(values) == 2:
                    data.append([
                        float(values[0]),
                        float(values[1])
                    ])

        return data

    x_data = read_data(x_file_name)
    y_data = read_data(y_file_name)

    if len(x_data) != len(y_data):
        raise ValueError("X and Y files have different lengths!")

    data = []

    for x, y in zip(x_data, y_data):
        data.append([(x[0]+X_FIX)/CHORD, (y[0]+ Y_FIX)/CHORD, x[1]])

    return np.array(data)


##三元素的打开函数 for coe
def edictable_read(file_name, *columns , skip = 1)->np.array:
    data = []
    with open(file_name, "r") as file:
        for line in file.readlines()[skip:]:
            values = line.split()
            row = []
            try:
                for i in columns:
                    row.append(float(values[i]))
            except (ValueError, IndexError):
                continue       
            
            data.append(row)
        
    return np.array(data)

def plot_fluent(cp_data):
    x = cp_data[:,0]
    y = cp_data[:,1]
    cp = cp_data[:,2]
    plot.figure()
    
    plot.plot(cp,x)
    plot.figure()
    plot.xlabel("y/m")
    plot.ylabel("cp")
    plot.plot(cp,y)
            
def  analysis_data(data:np.array, n:int, data_name, tol = 0.1, should_print = False):
    TOL = tol
    if len(data) < 2*n:
        print("there are no enough data")
        return
    current = data[-n:]
    previous = data[-2*n:(-n)]
    
    current_max = np.max(current)
    current_min = np.min(current)
    current_mean = np.mean(current)
    previous_mean = np.mean(previous)    
    
    #变化
    variation = current_max - current_min
    #convergence in %
    conv = variation/abs(current_mean) * 100
    #drift
    drift = abs(previous_mean - current_mean)
    
    is_conv = False
    if conv < TOL:
        is_conv = True
    if should_print:   
        print("===============================================")
        print(data_name)
        print("===============================================")
    
        print(f"Final mean : {current_mean:.5f}")
    
        print("收敛程度判断：：")
    
        print(f"Variation : {variation:.5f}")
        print(f"Convergence : {conv:.5f}%")
        print(f"Is convergence : {is_conv}")
        print(f"Drift : {drift:.5f}")
    
      
    
    return current_mean
    
def difference_percentage(xfoil:float , fluent:float)-> float:
    if xfoil == 0:
        print("xfoil data cant be zero")
        return 0
    
    diff = abs(abs(xfoil) - abs(fluent))
    
    diff_percen = diff/xfoil * 100
    
    return diff_percen


def plot_coe_compare(fluent_cp, xfoil_cp, x_label_1, x_label_2, y_label):
    def get_sep_data(data):
        x = data[:,0]
        y = data[:,1]
        z = data[:,2]
        return x, y, z
    
    f_x , f_y , f_cp = get_sep_data(fluent_cp)
    x_x , x_y , x_cp = get_sep_data(xfoil_cp)
    
    plot.figure()
    plot.xlim(0, 1)
    plot.grid()
    plot.xlabel(x_label_1)
    plot.ylabel(y_label)
    plot.plot(f_x, f_cp, label="Fluent", linewidth=0.7)
    plot.plot(x_x, x_cp, label = "xfoil", linewidth=0.7)
    plot.legend()
    plot.figure()
    plot.grid()
    plot.xlabel(x_label_2)
    plot.ylabel(y_label)
    plot.plot(f_y, f_cp, label="Fluent", linewidth=0.7)
    plot.plot(x_y, x_cp, label = "xfoil", linewidth=0.7)
    plot.legend()
    
def edictable_plot(data,x ,y , xlabel, ylabel):
    x_data = data[:, x]
    y_data = data[:, y]
    
    plot.figure()
    plot.scatter(x_data, y_data, s=3)
    plot.xlabel(xlabel)
    plot.ylabel(ylabel)
    plot.grid()
    
def get_shape(shape_x, shape_y):
    x = (shape_x + X_FIX) / CHORD
    y = (shape_y + Y_FIX) / CHORD

    return np.column_stack((x, y))
    
def split_surface(shape, coefficient):
    x = shape[:, 0]
    y = shape[:, 1]
    m, p = 0.02, 0.4

    # Mean camber line of NACA 2412
    yc = np.where(
        x <= p,
        m / p**2 * (2*p*x - x**2),
        m / (1-p)**2 * ((1-2*p) + 2*p*x - x**2)
    )

    data = np.column_stack((x, y, coefficient))

    upper = data[y >= yc]
    lower = data[y < yc]

    upper = upper[np.argsort(upper[:, 0])]
    lower = lower[np.argsort(lower[:, 0])]

    return upper, lower

def plot_split(upper, lower,xlabel, ylabel, invert_y=False):
    plot.figure(figsize=(9, 5))

    plot.plot(
        upper[:, 0], upper[:, 2],
        label="Upper", linewidth=1.2
    )

    plot.plot(
        lower[:, 0], lower[:, 2],
        label="Lower", linewidth=1.2
    )

    plot.xlabel(xlabel)
    plot.ylabel(ylabel)
    plot.xlim(0, 1)

    if invert_y:
        plot.gca().invert_yaxis()

    plot.axhline(0, color="gray", linewidth=0.7)
    plot.grid(alpha=0.3)
    plot.legend()
    plot.tight_layout()
    

def find_sepe_location(surface, tol=1e-4):
    # surface: [x/c, y/c, shear]
    surface = surface[np.argsort(surface[:, 0])]

    x = surface[:, 0]
    tau = surface[:, 2]

    for i in range(len(x) - 1):

        if abs(tau[i]) < tol or abs(tau[i+1]) < tol:
            continue

        if tau[i] * tau[i+1] < 0:

            x_zero = x[i] - tau[i] * (
                x[i+1] - x[i]
            ) / (tau[i+1] - tau[i])

            event = (
                "Positive to negative"
                if tau[i] > 0
                else "Negative to positive"
            )

            print(f"x/c = {x_zero:.5f}: {event}")

def find_moment_center(shape_x, shape_y, ratio=0.25):
    # 组合为二维坐标数组（Fluent 原始坐标）
    shape = np.column_stack((shape_x, shape_y))

    # 寻找前缘和尾缘
    le_index = np.argmin(shape[:, 0])
    te_index = np.argmax(shape[:, 0])

    LE = shape[le_index]
    TE = shape[te_index]

    # 计算四分之一弦长位置
    moment_center = LE + ratio * (TE - LE)
    
    print("===============================================")
    print(f"Leading Edge: {LE}")
    print(f"Trailing Edge: {TE}")
    print(f"Moment Center ({ratio:.0%} chord): {moment_center}")
    
    
    return moment_center

def main():
    ##===========================================================找形状和momentcenter
    shape_x = edictable_read(
    EXPORT_PATH / "pressure_coe_x", 
    0, 
    skip = 4
    ).flatten()
    
    shape_y = edictable_read(
    EXPORT_PATH / "pressure_coe_y", 
    0, 
    skip = 4
    ).flatten()
    
    moment_center = find_moment_center(shape_x, shape_y)
    X_FIX = moment_center[0]
    Y_FIX = moment_center[1]
    ##==============================================================
    
    shear = edictable_read(
    EXPORT_PATH / "shear_x",
    0, 1,
    skip=4
    )


    #打开文件
    # coefficient analysis
    fluent_cp = open_fluent_file(
    EXPORT_PATH / "pressure_coe_x",
    EXPORT_PATH / "pressure_coe_y", 
    skip = 4
    )
    
    xfoil_cp = edictable_read(
    XFOIL_PATH / "cp_4deg.txt",
    0,1,2,
    skip = 4
    )
    
    fluent_cf = open_fluent_file(
    EXPORT_PATH / "friction_coe_x",
    EXPORT_PATH / "friction_coe_y", 
    skip = 4
    )
    
    xfoil_cf = edictable_read(
    XFOIL_PATH / "cf_4deg.txt", 
    1, 2, 6, 
    skip = 2
    )
    
    #=====================================================================
    
    shape = get_shape(shape_x, shape_y)
    
    fluent_pressure_coe_split = edictable_read(
    EXPORT_PATH / "pressure_coe_x",
    1 , 
    skip = 4
    ).flatten()
    
    upper, lower = split_surface(shape, fluent_pressure_coe_split)
    
    #=====================================================================
    
    shear_shape_x = edictable_read(
    EXPORT_PATH / "shear_x", 
    0, 
    skip = 4
    ).flatten()
    
    shear_shape_y = edictable_read(
    EXPORT_PATH / "pressure_coe_y", 
    0, 
    skip = 4
    ).flatten()
    
    shear_shape = get_shape(shear_shape_x, shear_shape_y)
    
    fluent_shear_split = edictable_read(
    EXPORT_PATH / "shear_x",
    1 , 
    skip = 4
    ).flatten()
    
    upper_shear, lower_shear = split_surface(shear_shape,fluent_shear_split)
    
    
    #aerodynamic properties analysis
    fluent_cl = edictable_read(EXPORT_PATH / "c-l-rfile.out", 1, skip = 4)
    fluent_cd = edictable_read(EXPORT_PATH / "c-d-rfile.out", 1, skip = 4)
    fluent_cm = edictable_read(EXPORT_PATH / "c-m-rfile.out", 1, skip = 4)
    
    fluent_shear = edictable_read(EXPORT_PATH / "shear_x", 0, 1, skip = 5)
    
   # mesh data analysis
    fluent_y_plus = open_fluent_file(
    EXPORT_PATH / "y++_dia_x",
    EXPORT_PATH / "y++_dia_y", 
    skip = 5
    )
    

    
    #分析数据
    
    
    # coefficient analysis
    plot_split(upper, lower, "x/c", "cp")
    plot_split(upper_shear, lower_shear,"x/c","shear")
    
   
    plot_coe_compare(fluent_cp, xfoil_cp, "x/c", "y/c", "cp")
    plot_coe_compare(fluent_cf, xfoil_cf, "x/c", "y/c", "cf")
    
    #aerodynamic properties analysis
    fluent_mean_cl = analysis_data(fluent_cl, 30, "fluent_cl", should_print=True)
    fluent_mean_cd = analysis_data(fluent_cd, 30, "fluent_cd", should_print=True)
    fluent_mean_cm = analysis_data(fluent_cm, 30, "fluent_cm", should_print=True)
    
    edictable_plot(fluent_shear, 0, 1, "x/c", "shear")
    
    find_sepe_location(upper_shear)
    find_sepe_location(lower_shear)
    
    #找差距 我直接读的表
    diff_cl = difference_percentage(0.7156, fluent_mean_cl)
    diff_cd = difference_percentage(0.00695, fluent_mean_cd)
    diff_cm = difference_percentage(0.0574, fluent_mean_cm)
    print("===============================================")
    print(f"cl different percentage：{diff_cl:.5f}%")
    print(f"cd different percentage：{diff_cd:.5f}%")
    print(f"cm different percentage：{diff_cm:.5f}%")
    
    #mesh data
    edictable_plot(fluent_y_plus, 0, 2, "x/c", "y+")
    edictable_plot(fluent_y_plus, 1, 2, "y/c", "y+")
    
    
    
if __name__ == "__main__":
    main()
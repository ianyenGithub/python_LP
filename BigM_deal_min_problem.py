# 112MP_HW_e EX.4
from fractions import Fraction

def print_tableau(iteration, tableau, basis):
    """
    列印 Simplex 表格的函數。

    Parameters:
    - iteration (int): 迭代次數。
    - tableau (list): Simplex 表格。
    - basis (list): 基本變數列表。

    Returns:
    None
    """
    off_set = 8
    print(f"\n第 {iteration} 迭代:")

    # 列印表格標頭
    header = ["V.B.   "] + ["Z"] + [" "*int(f'{off_set-1}')] + [f"x{i:<{off_set-1}}" for i in range(1, len(tableau[0]) - 1)] + ["RHS"]
    print("".join(header))

    # 列印表格內容
    for i, row in enumerate(tableau):
        if i == 0:
            print(f"Z", end="")
            print("\t".expandtabs(6), end="")
        else:
            print(f"{basis[i-1]:<{off_set-1}}", end="")
        for val in row:
            p_format = ""
            if isinstance(val, list):
                # 處理表示 5*M - 2 這樣的表達式
                if val[0] != 0 or val[1] != 0:
                    if val[0] != 0:
                        p_format += str(Fraction(val[0]).limit_denominator()) + "M"
                        if val[1] > 0:
                            p_format += "+"
                    if val[1] != 0:
                        p_format += str(Fraction(val[1]).limit_denominator())
                else:
                    p_format += "0"
            else:
                p_format += str(Fraction(val).limit_denominator())
            print(f"{p_format:<{off_set}}", end="")
        print()


def simulate_simplex(tableau):
    """
    使用 Simplex 方法進行線性規劃的模擬。

    Parameters:
    - tableau (list): 初始 Simplex 表格。
    - M (int): M 的值，用於處理人工變數。 [M, coef.]

    Returns:
    None
    """
    # 初始化 BASIS，這裡假設一開始基本變數
    basis = ["x8","x9","x6","x10","x5"]
    print(f"basis: {basis}")
    # 開始迭代
    iteration = 1
    print_tableau(iteration, tableau, basis)
    while True:
        # 找到 pivot_column
        pivot_column = tableau[0].index(max(tableau[0][1:-1]))
        # 找到 pivot_row
        min_ratio = float('inf') # 無限大
        pivot_row = -1 # 設置未搜尋初始條件 
        for i in range(1, len(tableau)):
            if tableau[i][pivot_column] > 0 and tableau[i][-1] >= 0: # coef. in pivot_column, and RHS 
                ratio = tableau[i][-1] / tableau[i][pivot_column] # RHS / coef.
                if ratio < min_ratio:
                    min_ratio = ratio
                    pivot_row = i
        # 結束條件
        if pivot_row == -1: 
            print(f"結束，因為pivot_row=-1，min_ratio未通過，找不到進入變數")
            break
        if tableau[0][pivot_column][0] <= 0 and tableau[0][pivot_column][1] <= 0:
            print(f"結束，O.F.係數最大值，小於等於0")
            break

        # 更新(pivot row)
        pivot_value = tableau[pivot_row][pivot_column] # pivot
        for i in range(len(tableau[pivot_row])):
            tableau[pivot_row][i] /= pivot_value

        # 更新(other row)
        factor_0 = tableau[0][pivot_column][0] # M
        factor_1 = tableau[0][pivot_column][1] # coef
        for j in range(1, len(tableau[0])):
            tableau[0][j][0] -= factor_0 * tableau[pivot_row][j]
            tableau[0][j][1] -= factor_1 * tableau[pivot_row][j]
        for i in range(1, len(tableau)):
            if i != pivot_row:
                factor = tableau[i][pivot_column]
                for j in range(len(tableau[i])):
                    tableau[i][j] -= factor * tableau[pivot_row][j]

        # 更新 BASIS
        entering_variable = f"x{pivot_column}"
        leaving_variable = basis[pivot_row - 1]
        basis[pivot_row - 1] = entering_variable
        print(f"選擇{entering_variable}進入，{leaving_variable}離開basis")
        # 列印 Simplex Tableau
        iteration += 1
        print_tableau(iteration, tableau, basis)

# 初始 Simplex Tableau
initial_tableau = [
    [1, [0, 3], [0, 2], [0, 4], [0, 5], [0, 2], [0, -1], [0, 2], [0, 0], [0, 0], [0, 0], [0, 0]],
    [0, 2, 1, -1, 1, 3, 1, 2, 1, 0, 0,  10],
    [0, 3, -2, 2, 1, 1, -1, 3, 0, -1, 0,  5],
    [0, 1, 2, 1, -1, 1, 1, -1, 0, 0, 0,  8],
    [0, 4, -1, 3, 1, 2, -2, 1, 0, 0, 1,  15],
    [0, 2, 3, -1, 2, 1, 1, 4, 0, 0, 0,  12],
]


# 使用 BIG M 方法模擬 Simplex 過程 只處理min問題
simulate_simplex(initial_tableau)

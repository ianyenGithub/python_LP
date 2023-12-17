# algebra Bland’s Rule
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
    header = ["V.B."]+[" "*int(f'{off_set-5}')] + ["Z"] + [" "*int(f'{off_set-1}')] + [f"x{i:<{off_set-1}}" for i in range(1, len(tableau[0]) - 1)] + ["RHS"]
#     print("".join(header))

    # 列印表格內容
#     for i, row in enumerate(tableau):
#         if i == 0:
#             print(f"Z", end="")
#             print("\t".expandtabs(6), end="")
#         else:
#             print(f"{basis[i-1]:<{off_set-1}}", end="")
#         for idx, val in enumerate(row):
#             p_format = ""
#             p_format += str(Fraction(val).limit_denominator()) 
#             if idx != 0 and idx!=11:
#                 p_format += " * " + f"x{idx}"
#             print(f"{p_format:<{off_set}}", end="")
#         print()
    # 列印表格內容
    # 印出HTML table 格式
    print("$$")
    print("\\begin{array}{rcl}")
    for i, row in enumerate(tableau): # i=0, row=[1, 3, 2, 4, 5, 2, -1, 2, 0, 0, 0, 0]
#         print("\t<tr>")
        for idx, val in enumerate(row): # idx=2, val=2
            if val == 0 and idx != len(tableau[0])-1 and idx != 0: # len(tableau[0]-1)==11
                continue
            p_format = "" # ""
            if val >= 0 and idx != 1:
                p_format += "+" # "+"
            p_format += str(Fraction(val).limit_denominator()) # "+2"
            if idx == 0:
                if i == 0:
                    print(f"Z&=&")
                else:
                    print(f"{basis[i-1]}&=&")
            elif idx == len(tableau[0])-1: #RHS
                print(f"{p_format}")
            else:
                print(f"{p_format}x_{{{idx}}}\\;") # "+2" + "x2\\;" "\\"=\ "\b" = backspace
        print("\\\\")
    print("\end{array}$$")
    print()
    print(f'basis: {basis}')

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
        if  tableau[0][pivot_column] <= 0:
            print(f"結束，O.F.係數最大值，小於等於0")
            break

        # 更新(pivot row)
        pivot_value = tableau[pivot_row][pivot_column] # pivot
        for i in range(len(tableau[pivot_row])):
            tableau[pivot_row][i] /= pivot_value

        # 更新(other row)
        factor_1 = tableau[0][pivot_column] # coef
        for j in range(1, len(tableau[0])):
#             tableau[0][j][0] -= factor_0 * tableau[pivot_row][j]
            tableau[0][j] -= factor_1 * tableau[pivot_row][j]
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
    [1, 3, 2, 4, 5, 2, -1, 2, 0, 0, 0, 0],
    [0, 2, 1, -1, 1, 3, 1, 2, 1, 0, 0,  10],
    [0, 3, -2, 2, 1, 1, -1, 3, 0, -1, 0,  5],
    [0, 1, 2, 1, -1, 1, 1, -1, 0, 0, 0,  8],
    [0, 4, -1, 3, 1, 2, -2, 1, 0, 0, 1,  15],
    [0, 2, 3, -1, 2, 1, 1, 4, 0, 0, 0,  12],
]


# Simplex 過程 只處理min問題
simulate_simplex(initial_tableau)

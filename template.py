# -*- coding: utf-8 -*-
"""
Pandas 進階操作課堂練習：學生期末成績分析
"""

import pandas as pd

def merge_and_load_data(file_path_A, file_path_B):
    """任務一：讀取並合併兩個班級的 CSV 資料"""
    df_A = pd.read_csv(file_path_A, encoding='utf-8-sig')
    df_B = pd.read_csv(file_path_B, encoding='utf-8-sig')

    # TODO 1.1: 使用 pd.concat 將 df_A 和 df_B 垂直合併成一個 DataFrame
    # 提示：合併後請重設 index (使用 ignore_index=True)
    full_df = None # 請在此行修改
    
    # 顯示合併後的資料結構
    print("資料合併完成，結構如下：")
    full_df.info()
    return full_df

def feature_engineering(df):
    """任務二：計算總分與平均分數"""
    
    # 總分與平均分數要計算的科目
    score_columns = ['國文', '英文', '數學', '自然', '社會']

    # TODO 2.1: 新增欄位並計算總分，欄位名稱固定為 '總分'
    df['總分'] = None # 請在此行修改

    # TODO 2.2: 新增欄位並計算平均分數，欄位名稱固定為 '平均'
    df['平均'] = None # 請在此行修改
    
    print("\n特徵工程完成，已新增總分與平均欄位。")
    return df 

def advanced_analysis(df):
    """任務三：進階分析 - 分組、排序與條件修改"""
    
    # TODO 3.1: 使用 groupby 計算各班級的「國文」、「英文」、「數學」平均分數
    class_subject_means = None # 請在此行修改
    print("\n各班級主要科目平均分數：")
    print(class_subject_means)

    # TODO 3.2: 使用 groupby 和 agg 計算各班級的「總分」最高分與最低分
    # 提示：.agg(['max','min'])
    class_total_score_range = None # 請在此行修改
    print("\n各班級總分最高與最低分：")
    print(class_total_score_range)
    
    # TODO 3.3: 找出「總分」排名前三名的學生
    # 提示：可以先進行排序後再找前三列
    top_three_students = None # 請在此行修改
    print("\n總分排名前三名學生：")
    print(top_three_students[['姓名', '班級', '總分']])

    # TODO 3.4: 將 A 班英文成績低於 60 分的學生，其英文成績調整為 60 分
    # 提示：df.loc[條件, '英文'] = 60
    # 請在此行修改
    print("\n已將 A 班英文不及格者成績調整為 60。")
    
    return df

def save_results(df, output_file_path):
    df.to_csv(output_file_path, index=False, encoding='utf-8-sig')
    print(f"\n分析結果已儲存至 {output_file_path}")

if __name__ == "__main__":
    CLASS_A_CSV = "grades_classA.csv"
    CLASS_B_CSV = "grades_classB.csv"
    OUTPUT_CSV = "grades_analysis_advanced.csv"

    df = merge_and_load_data(CLASS_A_CSV, CLASS_B_CSV)
    df = feature_engineering(df)
    df = advanced_analysis(df)
    save_results(df, OUTPUT_CSV)

    print("\n所有進階分析任務完成！")

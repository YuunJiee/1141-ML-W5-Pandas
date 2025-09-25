# -*- coding: utf-8 -*-
import pytest
import pandas as pd
import importlib.util
from pathlib import Path
import os

# -------------------------
# 取得學生提交程式
# -------------------------
SUBMIT_DIR = Path(__file__).parent.parent / "submit"
student_files = list(SUBMIT_DIR.glob("*.py"))
if not student_files:
    raise FileNotFoundError(f"{SUBMIT_DIR} 沒有學生提交檔案")

student_file = student_files[0]
spec = importlib.util.spec_from_file_location("student_submission", student_file)
student_submission = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student_submission)

# -------------------------
# 測資 DataFrame
# -------------------------
@pytest.fixture
def sample_df():
    data = {
        "學號": ["S01","S02","S03","S04","S05"],
        "姓名": ["Alice","Bob","Charlie","David","Eva"],
        "班級": ["A","B","A","B","A"],
        "性別": ["F","M","M","M","F"],
        "國文": [78,82,85,50,90],
        "英文": [88,70,92,59,95],
        "數學": [95,55,60,40,88],
        "自然": [90,65,80,45,85],
        "社會": [85,60,70,55,92],
    }
    return pd.DataFrame(data)

# -------------------------
# 工具函式：記錄測試結果
# -------------------------
results = []

def check(name, condition, msg=""):
    if condition:
        results.append(f"✅ {name}")
    else:
        results.append(f"❌ {name} - {msg}")

def save_results_md(filename="test_results/results.md"):
    os.makedirs(Path(filename).parent, exist_ok=True)
    content = "### 學生作業自動測試結果\n\n" + "\n".join(results)
    print("===== results.md 內容 =====")
    print(content)
    print("===========================")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

# -------------------------
# 測試項目
# -------------------------
def test_feature_engineering(sample_df):
    df = student_submission.feature_engineering(sample_df.copy())

    assert "總分" in df.columns, "必須新增欄位：總分"
    assert "平均" in df.columns, "必須新增欄位：平均"

    alice = df[df["姓名"]=="Alice"].iloc[0]
    expected_total = 78 + 88 + 95 + 90 + 85

    check("總分正確", alice["總分"] == expected_total,
          msg=f"Alice 總分應為 {expected_total}, 得到 {alice['總分']}")

    check("平均正確", alice["平均"] == pytest.approx(expected_total/5, rel=1e-3),
          msg=f"Alice 平均應為 {expected_total/5}, 得到 {alice['平均']}")

def test_advanced_analysis(sample_df):
    df = student_submission.feature_engineering(sample_df.copy())
    processed_df = student_submission.advanced_analysis(df.copy())

    # groupby 測試
    class_subject_means = processed_df.groupby("班級")[["國文","英文","數學"]].mean().round(2)
    expected_mean_A_math = df[df["班級"]=="A"]["數學"].mean()
    check("groupby 平均正確",
          abs(class_subject_means.loc["A","數學"] - expected_mean_A_math) < 1e-6)

    # 總分前三名
    top3 = processed_df.sort_values("總分", ascending=False).head(3)
    check("總分最高學生正確", top3.iloc[0]["姓名"]=="Alice")

    # 英文補考調整 (A班 <60 → 60)
    a_class = processed_df[processed_df["班級"]=="A"]
    min_eng_A = a_class["英文"].min()
    check("英文補考調整", min_eng_A >= 60,
          msg=f"A班最低英文分數應 >=60, 得到 {min_eng_A}")

def test_save_results(tmp_path, sample_df):
    df = student_submission.feature_engineering(sample_df.copy())
    df = student_submission.advanced_analysis(df.copy())
    output_file = tmp_path / "grades_output.csv"
    student_submission.save_results(df, output_file)

    check("輸出檔案存在", output_file.exists())
    if output_file.exists():
        df_out = pd.read_csv(output_file, encoding="utf-8-sig")
        check("輸出檔案欄位", all(c in df_out.columns for c in ["總分","平均"]))

def test_generate_md():
    save_results_md("test_results/results.md")

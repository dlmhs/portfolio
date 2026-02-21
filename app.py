import streamlit as st
import pandas as pd

st.title("📊 我的投资组合分配器")

# 1. 设定总金额
total_amount = st.number_input("请输入计划投资总额 (¥):", min_value=0.0, value=10000.0, step=1000.0)

# 2. 设定（或读取）你的策略比例
st.subheader("当前投资策略比例")
col1, col2, col3 = st.columns(3)
with col1:
    stock_pct = st.number_input("股票基金 (%)", value=60.0)
with col2:
    bond_pct = st.number_input("债券基金 (%)", value=30.0)
with col3:
    crypto_pct = st.number_input("加密货币 (%)", value=10.0)

# 校验比例是否为 100%
if stock_pct + bond_pct + crypto_pct != 100.0:
    st.error("⚠️ 警告：各项比例总和必须等于 100%！")
else:
    # 3. 计算并展示结果
    st.subheader("💰 资金分配建议")
    data = {
        "资产类别": ["股票基金", "债券基金", "加密货币"],
        "分配比例": [f"{stock_pct}%", f"{bond_pct}%", f"{crypto_pct}%"],
        "建议金额": [total_amount * stock_pct / 100, 
                 total_amount * bond_pct / 100, 
                 total_amount * crypto_pct / 100]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

import streamlit as st
import pandas as pd

# 设置网页标题
st.set_page_config(page_title="投资分配提示", page_icon="📊")
st.title("📊 投资分配提示")

# 1. 设定总金额 (默认 $7000)
total_amount = st.number_input("请输入计算投资金额 ($):", min_value=0.0, value=7000.0, step=100.0)

# 2. 定义默认策略基数和分配金额
DEFAULT_TOTAL = 7000.0

# 默认投资组合及金额 (基于 $7000，Crypto 交易资产为 14 天总额)
default_portfolio = {
    "Crypto": {
        "BTC": 700.0,
        "ETH": 700.0,
        "LINK": 420.0,
        "SOL": 280.0,
        "USDC": 1400.0
    },
    "Stock": {
        "SGOV": 1400.0,
        "COPX": 1050.0,
        "TOPT": 1050.0
    }
}

# 3. 计算分配比例和实际分配金额
st.subheader("📝 资金分配建议")

data = []
calculated_amounts = {} # 用于存储计算后的具体金额

for category, assets in default_portfolio.items():
    for asset, default_amt in assets.items():
        # 计算该资产占 7000 的比例
        strategy_ratio = default_amt / DEFAULT_TOTAL
        # 根据用户输入的总金额计算实际分配总金额
        actual_amt = total_amount * strategy_ratio
        
        # 存入字典供后续汇总使用
        calculated_amounts[asset] = actual_amt
        
        # 计算 14 天每日定投金额 (仅限特定的 Crypto)
        if asset in ["BTC", "ETH", "LINK", "SOL"]:
            daily_amt = actual_amt / 14
            daily_str = f"${daily_amt:,.2f} / 天"
        else:
            daily_str = "-"
        
        data.append({
            "大类": category,
            "资产标的": asset,
            "策略比例": f"{strategy_ratio * 100:.2f}%",
            "总分配金额": f"${actual_amt:,.2f}",
            "每日定投 (14天)": daily_str
        })

df = pd.DataFrame(data)

# 显示表格
st.dataframe(df, use_container_width=True)

# 4. 计算三大转账汇总
st.subheader("🏦 转账操作指引")

# To Coinbase: 整个 crypto 的总数
to_coinbase = (calculated_amounts["BTC"] + calculated_amounts["ETH"] + 
               calculated_amounts["LINK"] + calculated_amounts["SOL"] + 
               calculated_amounts["USDC"])

# To Wallet: BTC + ETH + USDC
to_wallet = calculated_amounts["BTC"] + calculated_amounts["ETH"] + calculated_amounts["USDC"]

# To Stock: 整个 Stock 的部分
to_stock = calculated_amounts["SGOV"] + calculated_amounts["COPX"] + calculated_amounts["TOPT"]

# 使用 metric 组件展示，美观且醒目
col1, col2, col3 = st.columns(3)
col1.metric("To Coinbase", f"${to_coinbase:,.2f}")
col2.metric("To Wallet", f"${to_wallet:,.2f}")
col3.metric("To Stock", f"${to_stock:,.2f}")

# 5. Crypto 每日执行看板
st.subheader("⏳ Crypto 每日定投执行")
d_col1, d_col2, d_col3, d_col4 = st.columns(4)
d_col1.metric("BTC 每日", f"${calculated_amounts['BTC'] / 14:,.2f}")
d_col2.metric("ETH 每日", f"${calculated_amounts['ETH'] / 14:,.2f}")
d_col3.metric("LINK 每日", f"${calculated_amounts['LINK'] / 14:,.2f}")
d_col4.metric("SOL 每日", f"${calculated_amounts['SOL'] / 14:,.2f}")

# 6. 温馨提示（关于未分配资金）
st.divider() # 添加一条分割线
total_allocated = to_coinbase + to_stock
unallocated = total_amount - total_allocated

# 处理计算机浮点数精度可能导致的微小误差 (比如 -0.00000001)
if abs(unallocated) < 0.01:
    unallocated = 0.0

if unallocated > 0:
    unallocated_ratio = (unallocated / total_amount) * 100 if total_amount > 0 else 0
    st.caption(f"💡 提示：当前策略各项资产比例总计为 {100 - unallocated_ratio:.2f}%。在 ${total_amount:,.2f} 的总投资中，将有 ${unallocated:,.2f} 资金未分配。")
else:
    st.caption("✅ 提示：当前策略各项资产比例总计为 100%。资金已完美全部分配！

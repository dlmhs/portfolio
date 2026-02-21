import streamlit as st
import pandas as pd
import streamlit.components.v1 as components  # 新增：用于注入前端交互代码

# 设置网页标题
st.set_page_config(page_title="投资分配提示", page_icon="📊")
st.title("📊 投资分配提示")

# 1. 设定总金额和定投天数
col_input1, col_input2 = st.columns(2)
with col_input1:
    total_amount = st.number_input("投资金额($):", min_value=0, value=7000, step=100)
with col_input2:
    expected_days = st.number_input("预计定投天数:", min_value=1, value=14, step=1)

# 2. 定义默认策略基数和分配金额
DEFAULT_TOTAL = 7000.0

# 默认投资组合及金额 (基于 $7000)
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
calculated_amounts = {} 

for category, assets in default_portfolio.items():
    for asset, default_amt in assets.items():
        # 计算该资产占 7000 的比例
        strategy_ratio = default_amt / DEFAULT_TOTAL
        # 根据用户输入的总金额计算实际分配总金额
        actual_amt = total_amount * strategy_ratio
        
        # 存入字典供后续汇总使用
        calculated_amounts[asset] = actual_amt
        
        # 计算每日定投金额
        if asset in ["BTC", "ETH", "LINK", "SOL"]:
            daily_amt = actual_amt / expected_days
            daily_str = f"${daily_amt:,.0f} / 天"
        else:
            daily_str = "-"
        
        data.append({
            "大类": category,
            "标的": asset,
            "分配金额": f"${actual_amt:,.0f}",
            f"每日定投 ({expected_days}天)": daily_str,
            "策略比例": f"{strategy_ratio * 100:.2f}%"
        })

df = pd.DataFrame(data)

# 隐藏最左侧无用的数字序号列
st.dataframe(df, use_container_width=True, hide_index=True)

# 4. 计算三大转账汇总
st.subheader("🏦 转账操作指引")

to_coinbase = (calculated_amounts["BTC"] + calculated_amounts["ETH"] + 
               calculated_amounts["LINK"] + calculated_amounts["SOL"] + 
               calculated_amounts["USDC"])
to_wallet = calculated_amounts["BTC"] + calculated_amounts["ETH"] + calculated_amounts["USDC"]
to_stock = calculated_amounts["SGOV"] + calculated_amounts["COPX"] + calculated_amounts["TOPT"]

col1, col2, col3 = st.columns(3)
col1.metric("To Coinbase", f"${to_coinbase:,.0f}")
col2.metric("To Wallet", f"${to_wallet:,.0f}")
col3.metric("To Stock", f"${to_stock:,.0f}")

# 5. Crypto 每日执行看板
st.subheader(f"⏳ Crypto 每日定投执行 ({expected_days} 天)")
d_col1, d_col2, d_col3, d_col4 = st.columns(4)
d_col1.metric("BTC 每日", f"${calculated_amounts['BTC'] / expected_days:,.0f}")
d_col2.metric("ETH 每日", f"${calculated_amounts['ETH'] / expected_days:,.0f}")
d_col3.metric("LINK 每日", f"${calculated_amounts['LINK'] / expected_days:,.0f}")
d_col4.metric("SOL 每日", f"${calculated_amounts['SOL'] / expected_days:,.0f}")

# 6. 温馨提示（关于未分配资金）
st.divider() 
total_allocated = to_coinbase + to_stock
unallocated = total_amount - total_allocated

if abs(unallocated) < 0.01:
    unallocated = 0.0

if unallocated > 0:
    unallocated_ratio = (unallocated / total_amount) * 100 if total_amount > 0 else 0
    st.caption(f"💡 提示：当前策略各项资产比例总计为 {100 - unallocated_ratio:.2f}%。在 ${total_amount:,.0f} 的总投资中，将有 ${unallocated:,.0f} 资金未分配。")
else:
    st.caption("✅ 提示：当前策略各项资产比例总计为 100%。资金已完美全部分配！")

# ---------------------------------------------------------
# 【修改点】7. 注入前端 JS 代码：实现输入框点击全选功能
# ---------------------------------------------------------
js_code = """
<script>
// 监听整个网页的焦点事件
window.parent.document.addEventListener('focusin', function(e) {
    // 如果获得焦点的元素是数字输入框，则自动全选里面的内容
    if (e.target && e.target.type === 'number') {
        e.target.select();
    }
});
</script>
"""
# 渲染这段代码，高度设为0使其隐形
components.html(js_code, height=0)

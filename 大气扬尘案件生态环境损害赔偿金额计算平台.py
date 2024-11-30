import streamlit as st
import math

# 页面设置
st.set_page_config(
    page_title="大气扬尘案件生态环境损害赔偿金额计算器",
    page_icon="🌱",
    layout="wide"
)

# 标题
st.markdown("<h2 style='text-align: center; color: black;'>大气扬尘案件生态环境损害赔偿金额计算器</h2>", unsafe_allow_html=True)


#%%
# 展示扬尘量计算公式
st.success("堆场的扬尘源排放量是装卸、运输引起的扬尘与堆积存放期间风蚀扬尘的加和，计算公式如下：")
st.latex(r"""
  W_Y = \sum_{i=1}^m E_h \times G_{Yi} \times 10^{-3} + E_w \times A_Y \times 10^{-3}
""")
st.markdown("""
其中：
- $W_y$：为堆场扬尘源中颗粒物总排放量，t/a。
- $E_h$：为堆场装卸运输过程的扬尘颗粒物排放系数，kg/t
- $m$： 为每年料堆物料装卸总次数。
- $G_{Yi}$：第 i次装卸过程的物料装卸量
- $A_Y$：料堆表面积，$m^2$。
""")
st.divider()
# 创建两列
col1, col2 = st.columns(2)
with col1:

    
    #%%
    st.markdown("### 一、装卸、运输物料过程扬尘排放量$W_h$计算")
    st.markdown("### 装卸、运输物料过程扬尘排放系数 $E_h$ 的计算公式")
    st.latex(r"""
    \begin{align*}
    E_h = k_i \times 0.00 16 \times \frac{\left( \frac{u}{2.2} \right)^{1.3}}{\left( \frac{M}{2} \right)^{1.4}} \times (1 - \eta)
    \end{align*}
      """)
    st.markdown("""
    其中：
    - $E_h$：为堆场装卸运输过程的扬尘颗粒物排放系数，kg/t
    - $k_i$：物料的粒度乘数
    - $u$：地面平均风速，m/s
    - $M$：物料含水率，%，推荐实测方法同道路积尘含水率测定方法；条件不具备的，可参考表 11。
    
    """)
    inner_col1, inner_col2 = st.columns(2)
    with inner_col1:
        wind_speed_gd = st.number_input("请输入地面平均风速u (m/s)", value=5.0, min_value=0.0, step=0.1)
    with inner_col2:
        water = st.number_input("请输入物料含水率(%)", value=2.0, min_value=0.0, step=0.1)
    options_1 = ['TSP：0.74', 'PM10：0.35','PM2.5：0.053']
    zhuangxie_lidu = st.selectbox('请选择物料的粒度乘数：', options_1)
    # 判断用户选择的选项
    if zhuangxie_lidu.startswith('TSP'):
        zhuangxie_lidu_multiplier = 0.74
    elif zhuangxie_lidu.startswith('PM10'):
        zhuangxie_lidu_multiplier = 0.35
    elif zhuangxie_lidu.startswith('PM2.5'):
        zhuangxie_lidu_multiplier = 0.053
        
    # 计算装卸、运输物料过程扬尘排放系数 Eh
    emission_factor_eh = zhuangxie_lidu_multiplier * 0.0016 * (wind_speed_gd/2.2)**1.3/(water/100/2)**1.4 * (1-0) 
    # st.markdown(f"E_h = {{zhuangxie_lidu_multiplier:.2f} \cdot 0.0016 \cdot \frac{{\left( \frac{{{wind_speed_gd:.2f}}}{{2.2}} \right)^{{1.3}}}}{{\left( \frac{{{water:.2f}} / 100}}{{2}} \right)^{{1.4}}}} \cdot (1 - 0)""")
    st.markdown(f"- 装卸、运输物料过程扬尘排放系数 $E_h = {emission_factor_eh:.6f} \ \t{{kg/t}}$")
    st.image(r"C:\Users\wooji\Documents\WPSDrive\329775283\WPS云盘\1-损害鉴定项目\【2024.11.27】满洲里简易评估\表10 装卸过程中产生的颗粒物粒度乘数.png")
    st.image(r"C:\Users\wooji\Documents\WPSDrive\329775283\WPS云盘\1-损害鉴定项目\【2024.11.27】满洲里简易评估\表11 各种行业堆场物料的含水率参考值.png")
    
    #%%
    st.markdown("### 装卸、运输物料过程排放量")
    
    # 每年料堆物料装卸总次数
    num_zhuangxie = st.number_input("请输入每年料堆物料装卸总次数", value=1, min_value=1, step=1)
    
    
    # 第 i 次装卸过程的物料装卸量
    volume = st.number_input("请输入第 i 次装卸过程的物料装卸量(t),请输入每次的平均量", value=2, min_value=1, step=1)
    
    
    # 计算装卸、运输物料过程排放量 W
    total_emissions_zxys = emission_factor_eh * volume * num_zhuangxie # kg
    total_emissions_zxys_tons = total_emissions_zxys / 1000  # 转换为吨
    st.markdown(f" 装卸、运输物料过程排放量 $W_h = {emission_factor_eh:.6f} \cdot {volume} \cdot {num_zhuangxie} = {total_emissions_zxys:.3f} \ \t{{kg}} = {total_emissions_zxys_tons:.6f} \ \t{{吨}}$")
    

    

with col2:
    
    #%%
    st.markdown("### 二、堆场风蚀扬尘排放量$W_w$计算")
    
    
    st.markdown("### 扬尘排放系数 $E_w$ 的计算公式")
    st.latex(r"""
    E_w = k_i \times \sum_{i=1}^n P_i \times (1 - \eta) \times 10^{-3}
    """)
    st.markdown("""
    其中：
    - $E_w$：扬尘排放系数（单位：kg/m²）
    - $n$： 为料堆每年受扰动的次数
    - $η$：污染控制措施效率（无控尘时 $η = 0$）
    - $k_i$：粒度乘数
    - $P_i$：风蚀潜势（单位：g/m²）
    """)
    
    #%%
    # 展示风蚀潜势公式
    st.markdown("### 风蚀潜势 $P_i$ 的计算公式")
    st.latex(r"""
    P_i =
    \begin{cases}
    58 \cdot (u^* - u_t^*)^2 + 25 \cdot (u^* - u_t^*), & u^* > u_t^* \\
    0, & u^* \leq u_t^*
    \end{cases}
    """)
    st.latex(r"""
    u^* =
    \begin{align*}
     = 0.4u(z)/\ln \left(\frac{z}{z_0}\right) \quad (z > z_0)
    \end{align*}
    """)
    st.markdown("""
    其中：
    - $u^*$：摩擦风速，m/s
    - $u_t^*$：阈值摩擦风速，即起尘的临界摩擦风速，m/s，参考值见表 15。
    - $z$：地面风速检测高度，m。
    - $z_0$：地面粗糙度，m，城市取值 0.6，郊区取值 0.2。
    """)
    inner_col3, inner_col4 = st.columns(2)
    with inner_col3:
        wind_speed = st.number_input("请输入风速 (m/s)", value=5.0, min_value=0.0, step=0.1)
    with inner_col4:
        threshold_friction_velocity = st.number_input("请输入阈值摩擦风速 (m/s)", value=0.45, min_value=0.0, step=0.1)
    st.image(r"C:\Users\wooji\Documents\WPSDrive\329775283\WPS云盘\1-损害鉴定项目\【2024.11.27】满洲里简易评估\表15 阈值摩擦风速参考值.png")
    
    
    options_loc = ['城市', '郊区']
    loc = st.selectbox('请选择区域类型（影响地面粗糙度）：', options_loc)
    # 判断用户选择的选项
    if loc.startswith('城市'):
        z_0 = 0.6
    elif loc.startswith('郊区'):
        z_0 = 0.2

    
    # 计算摩擦风速 u*
    friction_velocity = (wind_speed * 0.4) / math.log(10 / z_0) 
    st.markdown(f" 计算摩擦风速 $u^*$：$u^* = \\frac{{{wind_speed} \\times 0.4}}{{\\ln(10 / {z_0})}} = {friction_velocity:.3f}$")
    
    # 计算风蚀潜势 Pi
    wind_erosion_potential = 0
    if friction_velocity > threshold_friction_velocity:
        wind_erosion_potential = 58 * (friction_velocity - threshold_friction_velocity)**2 + 25 * (friction_velocity - threshold_friction_velocity)
        st.markdown(f"风蚀潜势 $P_i = {wind_erosion_potential:.3f} \ \t{{g/m^2}}$")
    
    # 加和风蚀潜势（假设多次扰动）
    num_disturbances = st.number_input("请输入每年扰动次数", value=1, min_value=1, step=1)
    total_wind_erosion_potential = wind_erosion_potential * num_disturbances
    st.markdown(f"总风蚀潜势 $P_{{\t{{total}}}} = {total_wind_erosion_potential:.3f} \ \t{{g/m^2}}$")
    
    
    options = ['TSP：1.0', 'PM10：0.5','PM2.5：0.25']
    granularity = st.selectbox('请选择风蚀过程中产生的颗粒物：', options)
    # 判断用户选择的选项
    if granularity.startswith('TSP'):
        granularity_multiplier = 1
    elif granularity.startswith('PM10'):
        granularity_multiplier = 0.5
    elif granularity.startswith('PM2.5'):
        granularity_multiplier = 0.25
    
    
    
    # 计算扬尘排放系数 Ew
    emission_factor = (1 - 0) * granularity_multiplier * total_wind_erosion_potential * 1e-3  # 转换为 kg/m²  #ki扰动系数可以修改在
    st.markdown(f" 扬尘排放系数 $E_w = (1 - 0) \cdot {granularity_multiplier:.1f} \cdot {total_wind_erosion_potential:.3f} \cdot 10^{{-3}} = {emission_factor:.6f} \ \t{{kg/m²}}$")
    
    
    
    
    # 输入参数
    area = st.number_input("请输入堆场面积 (m²)", value=453, min_value=1, step=1)
    
    
    
    # 计算总排放量 W
    total_emissions_dc = emission_factor * area  # kg
    total_emissions_dc_tons = total_emissions_dc / 1000  # 转换为吨
    st.markdown(f" 堆场风蚀扬尘排放量 $W_w = {emission_factor:.6f} \cdot {area} = {total_emissions_dc:.3f} \ \t{{kg}} = {total_emissions_dc_tons:.6f} \ \t{{吨}}$")


#%%
st.divider()
st.markdown("### 三、损害赔偿金额计算")

total_emissions_tons = total_emissions_dc_tons + total_emissions_zxys_tons
st.markdown(f" 扬尘排放总量 $W = W_h + W_w = {total_emissions_zxys_tons:.6f} +  {total_emissions_dc_tons:.6f}  = {total_emissions_tons:.6f} \ \t{{吨}}$")

unit_abatement_cost = st.number_input("请输入单位治理成本 (元/吨)", value=2000, min_value=0, step=100)


st.markdown("### 调整系数$\gamma $的计算公式")
st.latex(r"""
\gamma = \ (\alpha \times \beta + \omega) \times \tau
 """)
st.markdown(r"""
其中：
- $\alpha$：危害系数
- $\beta$：受体敏感系数
- $\omega$：环境功能系数
- $\tau$：超标系数
""")

col5, col6,col7, col8 = st.columns(4)
with col5:
    hazard_coefficient = st.number_input("请输入危害系数", value=1.0, min_value=0.0, step=0.01)
with col6:
    env_coefficient = st.number_input("请输入环境功能系数", value=1.0, min_value=0.0, step=0.01)
with col7:
    shouti_coefficient = st.number_input("请输入受体敏感系数", value=1.0, min_value=0.0, step=0.01)
with col8:  
    over_coefficient = st.number_input("请输入超标系数", value=1.0, min_value=0.0, step=0.01)
    

adjustment_coefficient = (hazard_coefficient * env_coefficient +  shouti_coefficient) *  over_coefficient# 转换为吨
st.markdown(rf""" 调整系数 $\gamma = {adjustment_coefficient}$""")






# adjustment_coefficient = st.number_input("请输入调整系数", value=2.25, min_value=0.0, step=0.01)

# 计算损害赔偿金额
damage_amount = total_emissions_tons * unit_abatement_cost * adjustment_coefficient
st.markdown(f"损害赔偿金额：$D = {total_emissions_tons:.6f} \cdot {unit_abatement_cost} \cdot {adjustment_coefficient} = {damage_amount:.2f} \ \t{{元}}$")

# 结果展示
st.markdown("#### 结果")
st.success(f"最终生态环境损害赔偿金额为：{damage_amount:.2f} 元")

import streamlit as st
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# === Streamlit App Title ===
st.title("📊 Regression Analysis Dashboard")

# === Sidebar Data Input ===
st.sidebar.header("📋 Data Input")

# Instructions for Copy-Pasting
st.sidebar.markdown("""
**Instructions:**  
- Copy exactly **12 rows** of data from your spreadsheet.  
- Format can be **comma-separated** (e.g., `100,200`) or **tab-separated** (e.g., `100\t200`).  
- Paste the data below.
""")

# Text Area for Pasting Data
data_input = st.sidebar.text_area(
    "Paste your dataset here:",
    "100,200\n120,220\n130,250\n140,270\n150,290\n160,310\n170,330\n180,350\n190,370\n200,390\n210,410\n220,430",
    height=200
)

# === Parse Dataset ===
if data_input:
    try:
        from io import StringIO
        
        # Replace tabs with commas (if pasted from Excel)
        data_input = data_input.replace("\t", ",")
        
        # Read the pasted data into a DataFrame
        data = pd.read_csv(StringIO(data_input), names=["Variable", "Gross Profit"])
        
        # Validate row count
        if len(data) != 12:
            st.sidebar.error("⚠️ Please paste exactly **12 rows** of data.")
            st.stop()
        
        # Display dataset preview
        st.write("### ✅ Dataset Preview:")
        st.dataframe(data)
    
    except Exception as e:
        st.sidebar.error("❌ Invalid data format. Ensure it's two columns and properly separated.")
        st.stop()
else:
    st.warning("⏳ Please paste your dataset to proceed.")
    st.stop()

# === Regression Analysis ===
# -----------------------------
# 📊 REGRESSION ANALYSIS
# -----------------------------
st.write("---")
st.write("### 📊 Regression Analysis")

# 📌 Prepare Regression Model
X = data['Variable']
y = data['Gross Profit']
X = sm.add_constant(X)

# 🔄 Build and Fit the Model
model = sm.OLS(y, X).fit()

# Extract Key Metrics
summary = model.summary()
r_squared = model.rsquared
adj_r_squared = model.rsquared_adj
f_statistic = model.fvalue
p_value = model.f_pvalue
intercept = model.params['const']
slope = model.params['Variable']

# 📝 Display Regression Metrics in Cards
st.write("#### 📑 Key Regression Metrics:")

# 🛈 Add a Pop-Up (Expander) for Ideal Targets
with st.expander("❓ **What do these metrics mean?** Click to learn more"):
    st.markdown("""
    **ℹ️ Ideal Targets:**  
    - **R-Squared:** Closer to **1.0** indicates a better fit.  
    - **Adjusted R-Squared:** Adjusts for predictor count; closer to **1.0** is better.  
    - **F-Statistic:** Higher value indicates a better overall model fit.  
    - **P-Value (F-Stat):** Should be **< 0.05** for statistical significance.  
    - **Intercept:** Represents the baseline value when predictors are zero.  
    - **Slope:** Indicates the rate of change in the dependent variable per unit increase in the independent variable.
    """)

# Display Metrics in Three Columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="📈 **R-Squared**", value=f"{r_squared:.3f}")
    st.caption("Ideal: Closer to 1.0")

    st.metric(label="📊 **Adjusted R-Squared**", value=f"{adj_r_squared:.3f}")
    st.caption("Ideal: Closer to 1.0")

with col2:
    st.metric(label="📊 **F-Statistic**", value=f"{f_statistic:.3f}")
    st.caption("Higher is better")

    st.metric(label="📉 **P-Value (F-Stat)**", value=f"{p_value:.3e}")
    st.caption("Ideal: < 0.05")

with col3:
    st.metric(label="⚡ **Intercept (const)**", value=f"{intercept:.3f}")
    st.caption("Baseline value")

    st.metric(label="📐 **Slope (Variable)**", value=f"{slope:.3f}")
    st.caption("Change per unit of Variable")

# 📝 Display Detailed Summary Table
st.write("#### 📊 Detailed Regression Summary:")
import statsmodels.iolib.summary2 as sm2
summary_df = sm2.summary_col([model], stars=True, float_format="%.3f").tables[0]
st.write(summary_df)


# Generate Regression Summary Table
summary_df = sm2.summary_col([model], stars=True, float_format="%.3f").tables[0]

# Display Summary as a Static Table

st.write(summary_df)

# === Visualization ===
st.write("### 📈 Regression Plot:")
fig, ax = plt.subplots()
ax.scatter(data['Variable'], data['Gross Profit'], label='Data Points')
ax.plot(data['Variable'], model.predict(X), color='red', label='Regression Line')
ax.set_title('Variable vs Gross Profit')
ax.set_xlabel('Variable')
ax.set_ylabel('Gross Profit')
ax.legend()
st.pyplot(fig)

import streamlit as st
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

# === Initialize Default Variables ===
data = None  # Placeholder for dataset

# === Sidebar Data Input ===
st.sidebar.header("📋 Data Input")
st.sidebar.markdown("""
**Instructions:**  
- Copy exactly **12 rows** of data from your spreadsheet. GP on the RH column.  
- Format can be **comma-separated** (e.g., `100,200`) or **tab-separated** (e.g., `100\t200`).  
- Paste the data below.
""")

# Text Area for Data Input
data_input = st.sidebar.text_area(
    "Paste your dataset here:",
    "100,200\n120,220\n130,250\n140,270\n150,290\n160,310\n170,330\n180,350\n190,370\n200,390\n210,410\n220,430",
    height=200
)

# Add a "Run Analysis" Button
run_button = st.button("🚀 Run Analysis")

# === Placeholder Message Before Run Analysis ===
if not run_button:
    st.info("📝 **Press 'Run Analysis' to begin data analysis.**")
    st.stop()

# === Run Analysis Only If Button is Clicked ===
if run_button:
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
            
            # Ensure data types are numeric
            data["Variable"] = pd.to_numeric(data["Variable"], errors='coerce')
            data["Gross Profit"] = pd.to_numeric(data["Gross Profit"], errors='coerce')
            
            if data.isnull().any().any():
                st.sidebar.error("❌ Non-numeric values detected. Please ensure all data is numeric.")
                st.stop()
            
            # Display dataset preview
            st.write("### ✅ Dataset Preview:")
            st.dataframe(data)
            st.success("✅ Dataset successfully validated! Proceeding with analysis...")

            # === Regression Analysis ===
            st.write("---")
            st.write("### 📊 Regression Analysis")

            # Prepare Regression Model
            X = data['Variable']
            y = data['Gross Profit']
            X = sm.add_constant(X)

            # Build and Fit the Model
            model = sm.OLS(y, X).fit()

            # Extract Key Metrics
            r_squared = model.rsquared
            adj_r_squared = model.rsquared_adj
            f_statistic = model.fvalue
            p_value = model.f_pvalue
            intercept = model.params['const']
            slope = model.params['Variable']

            # Display Key Regression Metrics
            st.write("#### 📑 Key Regression Metrics:")
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

            # Display Regression Plot
            st.write("### 📈 Regression Plot:")
            fig, ax = plt.subplots()
            ax.scatter(data['Variable'], data['Gross Profit'], label='Data Points')
            ax.plot(data['Variable'], model.predict(X), color='red', label='Regression Line')
            ax.set_title('Variable vs Gross Profit')
            ax.set_xlabel('Variable')
            ax.set_ylabel('Gross Profit')
            ax.legend()
            st.pyplot(fig)

            # Display Correlation Heatmap
            st.write("### 🔗 Correlation Heatmap")
            correlation_matrix = data.corr()
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(
                correlation_matrix,
                annot=True,
                cmap="coolwarm",
                fmt=".2f",
                vmin=-1,
                vmax=1,
                center=0,
                linewidths=1,
                square=True,
                cbar_kws={"shrink": 0.75}
            )
            ax.set_title('Correlation Heatmap Between Variables')
            st.pyplot(fig)

        except Exception as e:
            st.sidebar.error(f"❌ An error occurred: {e}")
            st.stop()
    else:
        st.warning("⏳ Please paste your dataset to proceed.")
        st.stop()

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

# -----------------------------
# 📊 CORRELATION HEATMAP
# -----------------------------
st.write("---")
st.write("### 🔗 Correlation Heatmap")

import seaborn as sns

# Calculate Correlation Matrix
correlation_matrix = data.corr()

# Plot Heatmap with Adjusted Colour Scale
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    vmin=-1,  # Set minimum value for the colour scale
    vmax=1,   # Set maximum value for the colour scale
    center=0, # Ensure 0 correlation is neutral (white/grey)
    linewidths=1,
    square=True,
    cbar_kws={"shrink": 0.75}  # Adjust colour bar size
)
ax.set_title('Correlation Heatmap Between Variables')
st.pyplot(fig)
# 📑 Add Explanation
with st.expander("❓ **What does this mean?** Click to learn more"):
    st.markdown("""
    - A **correlation coefficient (r)** measures the strength and direction of the relationship between two variables.  
    - **Range:** `-1` (strong negative correlation) to `+1` (strong positive correlation).  
    - **Close to 1:** Strong positive correlation (e.g., both increase together).  
    - **Close to -1:** Strong negative correlation (e.g., one decreases as the other increases).  
    - **Close to 0:** Weak or no correlation.  
    """)

# Provide Quick Insights
if correlation_matrix.loc['Variable', 'Gross Profit'] > 0.7:
    st.success("✅ **Strong Positive Correlation Detected!**")
elif correlation_matrix.loc['Variable', 'Gross Profit'] < -0.7:
    st.warning("⚠️ **Strong Negative Correlation Detected!**")
else:
    st.info("ℹ️ **Weak or Moderate Correlation Observed.**")



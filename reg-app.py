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
X = data['Variable']
y = data['Gross Profit']
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()

st.write("### 📊 Regression Summary:")
st.text(model.summary())

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

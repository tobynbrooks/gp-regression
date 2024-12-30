import streamlit as st
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# === Streamlit App Title ===
st.title("📊 Regression Analysis Dashboard")

# === Sidebar Data Input ===
st.sidebar.header("Data Input")
data_input = st.sidebar.text_area(
    "Paste your dataset here (Variable, Gross Profit format):",
    "10,100\n20,200\n30,150\n40,300\n50,250"
)

# === Parse Dataset ===
from io import StringIO
try:
    data = pd.read_csv(StringIO(data_input), names=["Variable", "Gross Profit"])
    st.write("### Dataset Preview:")
    st.write(data)
except Exception as e:
    st.error("Invalid dataset format. Ensure it's comma-separated with two columns.")
    st.stop()

# === Regression Analysis ===
X = data['Variable']
y = data['Gross Profit']
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()

st.write("### Regression Summary:")
st.text(model.summary())

# === Visualization ===
st.write("### Regression Plot:")
fig, ax = plt.subplots()
ax.scatter(data['Variable'], data['Gross Profit'], label='Data Points')
ax.plot(data['Variable'], model.predict(X), color='red', label='Regression Line')
ax.set_title('Variable vs Gross Profit')
ax.set_xlabel('Variable')
ax.set_ylabel('Gross Profit')
ax.legend()
st.pyplot(fig)

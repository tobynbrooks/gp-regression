import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# === STEP 1: Input Your Data ===
data = {
    'Variable': [10, 20, 30, 40, 50],
    'Gross Profit': [100, 200, 150, 300, 250]
}

# Create a DataFrame
df = pd.DataFrame(data)

# === STEP 2: Quick Summary Statistics ===
print("\n📊 SUMMARY STATISTICS:")
print(df.describe())

# === STEP 3: Regression Analysis ===
X = df['Variable']
y = df['Gross Profit']
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()

print("\n📉 REGRESSION SUMMARY:")
print(model.summary())

# === STEP 4: Save Plot as an Image ===
plt.figure(figsize=(10, 6))
plt.scatter(df['Variable'], df['Gross Profit'], label='Data Points')
plt.plot(df['Variable'], model.predict(X), color='red', label='Regression Line')
plt.title('Variable vs Gross Profit')
plt.xlabel('Variable')
plt.ylabel('Gross Profit')
plt.legend()
plt.savefig('regression_plot.png')
print("\n✅ Plot saved as 'regression_plot.png'")

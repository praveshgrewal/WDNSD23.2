# 1. Import all required libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score, mean_squared_error
# 2. Load the dataset
df = sns.load_dataset('tips')
# 3. Separate features (X) and target (y)
X = df[['total_bill', 'size']]
y = df['tip']
# 4. Split data to avoid data leakage (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# 5. Scale features so network treats both columns equally
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test) # Transform only!
# --- APPROACH 1: MACHINE LEARNING (LINEAR REGRESSION) ---
ml_model = LinearRegression()
ml_model.fit(X_train_scaled, y_train)
ml_preds = ml_model.predict(X_test_scaled)
print("ML R2 Score:", r2_score(y_test, ml_preds))
# --- APPROACH 2: DEEP LEARNING (MULTI-LAYER ANN) ---
# Build and train Neural Network using scikit-learn MLPRegressor
dl_model = MLPRegressor(
    hidden_layer_sizes=(8, 4),  # 2 hidden layers with 8 and 4 neurons
    activation='relu',
    solver='adam',  # Uses adam optimizer
    learning_rate_init=0.001,
    max_iter=1000,
    random_state=42,
    verbose=0
)

# Train the model
dl_model.fit(X_train_scaled, y_train)

# Predict using the Deep Learning model
dl_preds = dl_model.predict(X_test_scaled)
print("DL Multi-Layer R2 Score:", r2_score(y_test, dl_preds))
print("DL Multi-Layer MSE:", mean_squared_error(y_test, dl_preds))

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Plot 1: Actual vs Predicted (ML Model)
axes[0].scatter(y_test, ml_preds, alpha=0.6)
axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
axes[0].set_xlabel('Actual Tip ($)')
axes[0].set_ylabel('Predicted Tip ($)')
axes[0].set_title(f'ML: Linear Regression\nR² = {r2_score(y_test, ml_preds):.3f}')

# Plot 2: Actual vs Predicted (DL Model)
axes[1].scatter(y_test, dl_preds, alpha=0.6, color='green')
axes[1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
axes[1].set_xlabel('Actual Tip ($)')
axes[1].set_ylabel('Predicted Tip ($)')
axes[1].set_title(f'DL: Neural Network\nR² = {r2_score(y_test, dl_preds):.3f}')

plt.tight_layout()
plt.savefig('regression_comparison.png', dpi=100, bbox_inches='tight')
print("\n✓ Plot saved as 'regression_comparison.png'")
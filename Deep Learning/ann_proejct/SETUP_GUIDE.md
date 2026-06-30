# Setup Guide - Fraud Detection Django Application

## Quick Start (5 minutes)

### Step 1: Activate Environment
```bash
conda activate tf_env
```

### Step 2: Navigate to Project
```bash
cd /Volumes/E/skill\ circle/WDNSD23.2/Deep\ Learning/ann_proejct
```

### Step 3: Run the Application
```bash
python manage.py runserver
```

### Step 4: Open Browser
Visit: **http://127.0.0.1:8000/**

---

## Detailed Setup Instructions

### Prerequisites Check

Before starting, ensure you have:

1. **Python Environment**
   ```bash
   conda list | grep tf_env
   ```
   Should show: `tf_env   /opt/anaconda3/envs/tf_env`

2. **Required Packages**
   ```bash
   conda run -n tf_env pip list | grep django
   ```
   Should show: `Django 5.2.15`

### Installation Steps

#### Step 1: Activate the Environment
```bash
# Activate the tf_env conda environment
conda activate tf_env

# Verify activation (prompt should show (tf_env) at the start)
which python
```

#### Step 2: Verify Django Installation
```bash
# Check if Django is installed
python -c "import django; print(django.VERSION)"

# If not installed, run:
pip install django
```

#### Step 3: Apply Database Migrations
```bash
cd /Volumes/E/skill\ circle/WDNSD23.2/Deep\ Learning/ann_proejct
python manage.py migrate
```

Expected output:
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

#### Step 4: Start Development Server
```bash
python manage.py runserver
```

Expected output:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

#### Step 5: Access the Application
Open your browser and navigate to:
- **Main App**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## Using the Application

### Web Interface

1. **Enter Transaction Details**
   - Personal info (Age, Gender)
   - Account info (Type, Income, Credit Score, etc.)
   - Transaction info (Type, Category, Amount, etc.)
   - Timing & Device info

2. **Submit Form**
   - Click "Analyze Transaction" button

3. **View Results**
   - See fraud probability score
   - Get recommended actions
   - Option to analyze another transaction

### Example Transaction Data

**Safe Transaction Example:**
- Age: 45
- Gender: Male
- Account Type: Savings
- Annual Income: $75,000
- Credit Score: 750
- Account Tenure: 24 months
- Transaction Hour: 14
- Day of Week: Monday
- Transaction Type: Debit
- Category: Shopping
- Payment Method: Card
- Device Type: Mobile
- Amount: $150.50
- International: No
- Account Balance After: $5,000

**Suspicious Transaction Example:**
- Age: 28
- Gender: Female
- Account Type: Credit
- Annual Income: $35,000
- Credit Score: 580
- Account Tenure: 3 months
- Transaction Hour: 3 (midnight)
- Day of Week: Sunday
- Transaction Type: Transfer
- Category: Travel
- Payment Method: Mobile Wallet
- Device Type: Desktop
- Amount: $5,000 (unusually high)
- International: Yes
- Account Balance After: $500

---

## API Usage

### Making API Requests

#### Using curl:
```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_age": 45,
    "customer_gender": "M",
    "account_type": "Savings",
    "annual_income": 75000,
    "credit_score": 750,
    "account_tenure_months": 24,
    "transaction_hour": 14,
    "day_of_week": "Monday",
    "transaction_type": "Debit",
    "transaction_category": "Shopping",
    "payment_method": "Card",
    "device_type": "Mobile",
    "amount": 150.50,
    "is_international": false,
    "account_balance_after": 5000
  }'
```

#### Using Python:
```python
import requests
import json

url = "http://127.0.0.1:8000/api/predict/"
data = {
    "customer_age": 45,
    "customer_gender": "M",
    "account_type": "Savings",
    "annual_income": 75000,
    "credit_score": 750,
    "account_tenure_months": 24,
    "transaction_hour": 14,
    "day_of_week": "Monday",
    "transaction_type": "Debit",
    "transaction_category": "Shopping",
    "payment_method": "Card",
    "device_type": "Mobile",
    "amount": 150.50,
    "is_international": False,
    "account_balance_after": 5000
}

response = requests.post(url, json=data)
result = response.json()
print(json.dumps(result, indent=2))
```

#### Response Example:
```json
{
  "success": true,
  "is_fraud": false,
  "fraud_probability": 15.34,
  "safe_probability": 84.66
}
```

---

## Troubleshooting

### Problem 1: "ModuleNotFoundError: No module named 'django'"

**Solution:**
```bash
conda activate tf_env
pip install django
```

### Problem 2: "ModuleNotFoundError: No module named 'tensorflow'"

**Solution:**
```bash
conda activate tf_env
pip install tensorflow-macos tensorflow-metal
```

### Problem 3: Port 8000 is already in use

**Solution 1** - Use a different port:
```bash
python manage.py runserver 8001
```

**Solution 2** - Kill the process using port 8000:
```bash
lsof -ti:8000 | xargs kill -9
```

### Problem 4: "FileNotFoundError: ann_model.pkl"

**Solution:**
Ensure `ann_model.pkl` exists in the project root:
```bash
ls -la ann_model.pkl
```

If missing, run the Jupyter notebook to regenerate the model.

### Problem 5: Database errors (sqlite3)

**Solution:**
```bash
# Delete the old database and regenerate
rm db.sqlite3

# Apply migrations
python manage.py migrate
```

### Problem 6: Form validation errors

**Solution:**
- Ensure all numeric fields have valid numbers
- Categorical fields must use predefined choices
- Amount must be positive
- Age must be between 18-120

---

## Advanced Configuration

### Change Server Port
```bash
python manage.py runserver 0.0.0.0:8080
```

### Create Superuser for Admin
```bash
python manage.py createsuperuser
```

### Collect Static Files (for production)
```bash
python manage.py collectstatic
```

### Make Database Backups
```bash
# Dump data
python manage.py dumpdata > backup.json

# Load data
python manage.py loaddata backup.json
```

---

## File Locations

| Item | Location |
|------|----------|
| Project Root | `/Volumes/E/skill circle/WDNSD23.2/Deep Learning/ann_proejct/` |
| Django Settings | `fraud_detection/settings.py` |
| URL Configuration | `fraud_detection/urls.py` |
| App Views | `predictor/views.py` |
| App Forms | `predictor/forms.py` |
| Templates | `predictor/templates/predictor/` |
| Database | `db.sqlite3` |
| Model File | `ann_model.pkl` |
| Dataset | `indian_financial_transactions (2).csv` |

---

## Model Information

- **Input Features**: 110+ (after one-hot encoding)
- **Architecture**: 64 → 32 → 1 neurons
- **Training Accuracy**: See logs/fit/ directory
- **Output**: Fraud probability (0-1)
- **Threshold**: 0.5 (≥ 0.5 = Fraud, < 0.5 = Safe)

---

## Next Steps

1. ✅ Setup complete
2. 🌐 Start the development server
3. 📝 Test with sample transactions
4. 📊 Review prediction accuracy
5. 🚀 Deploy to production (optional)

---

## Support & Documentation

- **Django Docs**: https://docs.djangoproject.com/
- **TensorFlow Docs**: https://www.tensorflow.org/
- **Project README**: `README.md` in project root
- **Original Notebook**: `ann_fraud_detection.ipynb`

---

## Security Reminders

⚠️ **For Development Only:**
- `DEBUG = True` (change to `False` for production)
- `SECRET_KEY` is exposed (use environment variables)
- `ALLOWED_HOSTS = []` (add your domain for production)

✅ **Before Production:**
1. Change `SECRET_KEY` in settings.py
2. Set `DEBUG = False`
3. Set `ALLOWED_HOSTS = ['yourdomain.com']`
4. Use PostgreSQL instead of SQLite
5. Enable HTTPS
6. Set up proper authentication
7. Configure CORS if needed

---

**Last Updated**: June 30, 2026

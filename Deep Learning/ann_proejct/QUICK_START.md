# 🚨 Fraud Detection Django App - Quick Reference

## 🚀 START THE APP (30 seconds)

```bash
# Step 1: Activate environment
conda activate tf_env

# Step 2: Navigate to project
cd /Volumes/E/skill\ circle/WDNSD23.2/Deep\ Learning/ann_proejct

# Step 3: Start server
python manage.py runserver

# Step 4: Open browser
# http://127.0.0.1:8000/
```

---

## 📋 Form Fields Reference

Copy-paste ready example values:

```
Age: 45
Gender: M
Account Type: Savings
Annual Income: 75000
Credit Score: 750
Account Tenure: 24
Transaction Hour: 14
Day of Week: Monday
Transaction Type: Debit
Category: Shopping
Payment Method: Card
Device Type: Mobile
Amount: 150.50
International: ☐ (unchecked)
Balance After: 5000
```

---

## 🔌 API Quick Test

### Using curl:
```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"customer_age": 45, "customer_gender": "M", "account_type": "Savings", "annual_income": 75000, "credit_score": 750, "account_tenure_months": 24, "transaction_hour": 14, "day_of_week": "Monday", "transaction_type": "Debit", "transaction_category": "Shopping", "payment_method": "Card", "device_type": "Mobile", "amount": 150.50, "is_international": false, "account_balance_after": 5000}'
```

### Using Python:
```python
import requests

resp = requests.post('http://127.0.0.1:8000/api/predict/', json={
    "customer_age": 45, "customer_gender": "M", "account_type": "Savings",
    "annual_income": 75000, "credit_score": 750, "account_tenure_months": 24,
    "transaction_hour": 14, "day_of_week": "Monday", "transaction_type": "Debit",
    "transaction_category": "Shopping", "payment_method": "Card", "device_type": "Mobile",
    "amount": 150.50, "is_international": False, "account_balance_after": 5000
})
print(resp.json())
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `predictor/views.py` | Model loading & predictions |
| `predictor/forms.py` | Form validation |
| `predictor/templates/index.html` | Prediction form |
| `predictor/templates/result.html` | Results page |
| `ann_model.pkl` | **Trained model (DO NOT DELETE)** |
| `db.sqlite3` | Database |
| `manage.py` | Django management |

---

## 🔧 Useful Commands

```bash
# Activate environment
conda activate tf_env

# Check if Django installed
python -c "import django; print(django.VERSION)"

# Run migrations
python manage.py migrate

# Start dev server
python manage.py runserver

# Use different port
python manage.py runserver 8001

# Create admin user
python manage.py createsuperuser

# Access admin
# http://127.0.0.1:8000/admin/

# Check for errors
python manage.py check

# Reset database
rm db.sqlite3 && python manage.py migrate

# Install packages
pip install -r requirements.txt
```

---

## 🎨 UI Design

- **Colors**: Purple gradient (#667eea → #764ba2)
- **Framework**: Bootstrap 5.3.0
- **Forms**: Clean, modern inputs
- **Results**: Color-coded (Red = Fraud, Green = Safe)
- **Responsive**: Works on mobile, tablet, desktop

---

## 🧪 Test Cases

### Test 1: Normal Transaction
- Young, good credit, reasonable amount
- Expected: Safe ✅

### Test 2: Suspicious Transaction  
- Late night, high amount, international
- Expected: Fraud ⚠️

### Test 3: Extreme Values
- Max values on all fields
- Expected: Model-dependent

---

## ⚡ Performance

- **Model Load Time**: ~2 seconds (first request)
- **Prediction Time**: ~50-100ms
- **Database**: SQLite (fast for dev)
- **Caching**: Model cached globally for speed

---

## 🐛 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Port 8000 in use | `python manage.py runserver 8001` |
| Module not found | `conda activate tf_env && pip install -r requirements.txt` |
| Template not found | Check `predictor/templates/predictor/` exists |
| Model not found | Ensure `ann_model.pkl` in project root |
| Database error | `rm db.sqlite3 && python manage.py migrate` |

---

## 📚 Documentation

- **Full Guide**: `SETUP_GUIDE.md`
- **Project Info**: `README.md`
- **Summary**: `PROJECT_SUMMARY.md`
- **Quick Ref**: This file

---

## 🌐 URLs

| Path | Function |
|------|----------|
| `/` | Main form |
| `/predict/` | Form processing |
| `/api/predict/` | JSON API |
| `/admin/` | Admin panel |

---

## ✅ Verification Checklist

- [x] Django installed in tf_env
- [x] Project structure created
- [x] Predictor app integrated
- [x] Forms created with validation
- [x] Views with model loading
- [x] Templates with Bootstrap styling
- [x] API endpoint ready
- [x] Migrations applied
- [x] Documentation complete

---

## 🎯 Next Actions

1. **Run**: `python manage.py runserver`
2. **Test**: Visit http://127.0.0.1:8000/
3. **Try**: Fill form and submit
4. **Review**: Check results
5. **Customize**: Modify as needed

---

## 📞 Help

- Django Docs: https://docs.djangoproject.com/
- TensorFlow: https://tensorflow.org/
- Python: https://python.org/

---

**Status**: ✅ READY TO USE  
**Framework**: Django 5.2.15  
**Environment**: tf_env  
**Updated**: 2026-06-30

Enjoy your fraud detection app! 🚀

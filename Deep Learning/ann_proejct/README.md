# Fraud Detection Django Application

A web-based application for detecting fraudulent transactions using an Artificial Neural Network (ANN) trained on Indian financial transactions data.

## Project Structure

```
ann_proejct/
├── ann_fraud_detection.ipynb          # Original Jupyter notebook
├── ann_model.pkl                      # Trained model (pickle file)
├── indian_financial_transactions.csv  # Training dataset
├── manage.py                          # Django management script
├── requirements.txt                   # Project dependencies
├── fraud_detection/                   # Main Django project
│   ├── __init__.py
│   ├── settings.py                    # Django settings
│   ├── urls.py                        # URL routing
│   ├── asgi.py
│   └── wsgi.py
├── predictor/                         # Main Django app
│   ├── migrations/
│   ├── templates/predictor/
│   │   ├── base.html                  # Base template
│   │   ├── index.html                 # Prediction form
│   │   └── result.html                # Prediction results
│   ├── forms.py                       # Django forms
│   ├── views.py                       # View logic
│   ├── urls.py                        # App URLs
│   ├── models.py
│   ├── admin.py
│   ├── apps.py
│   └── tests.py
└── logs/                              # TensorBoard logs from training
```

## Prerequisites

- Python 3.8+
- tf_env conda environment (already configured)
- Django 5.2.15
- TensorFlow 2.16.2
- scikit-learn 1.5.0
- pandas 2.2.2

## Installation

### 1. Activate the tf_env Environment

```bash
conda activate tf_env
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

Or if Django isn't already installed:

```bash
pip install django
```

## Running the Application

### 1. Apply Database Migrations (if not already done)

```bash
python manage.py migrate
```

### 2. Start the Development Server

```bash
python manage.py runserver
```

The application will start at: **http://127.0.0.1:8000/**

### 3. Access the Application

- **Home Page**: http://127.0.0.1:8000/
- **Prediction Form**: http://127.0.0.1:8000/
- **API Endpoint**: http://127.0.0.1:8000/api/predict/

## Usage

### Web Interface

1. Open the home page at http://127.0.0.1:8000/
2. Fill in the transaction details:
   - **Personal Information**: Age, Gender
   - **Account Information**: Account Type, Annual Income, Credit Score, Account Tenure, Account Balance
   - **Transaction Details**: Type, Category, Amount, Payment Method
   - **Timing & Device**: Transaction Hour, Day of Week, Device Type
   - **Additional Info**: International Transaction Flag
3. Click "Analyze Transaction" button
4. View the prediction results with fraud probability scores

### API Endpoint

Send a POST request with JSON data:

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

**Response:**

```json
{
  "success": true,
  "is_fraud": false,
  "fraud_probability": 15.34,
  "safe_probability": 84.66
}
```

## Model Information

### Training Details

- **Model Type**: Artificial Neural Network (ANN)
- **Architecture**:
  - Input Layer: 110+ features (after one-hot encoding)
  - Hidden Layer 1: 64 neurons with ReLU activation
  - Dropout: 0.2
  - Hidden Layer 2: 32 neurons with ReLU activation
  - Output Layer: 1 neuron with Sigmoid activation (binary classification)

- **Training Configuration**:
  - Optimizer: Adam
  - Loss Function: Binary Crossentropy
  - Metrics: Accuracy
  - Batch Size: 256
  - Epochs: 10
  - Validation Split: 0.2

### Feature Engineering

The model uses the following features:

**Numeric Features:**
- Customer Age
- Annual Income
- Credit Score
- Account Tenure (months)
- Transaction Hour
- Transaction Amount
- Account Balance After

**Categorical Features (One-Hot Encoded):**
- Customer Gender (M/F)
- Account Type (Savings/Checking/Credit)
- Day of Week
- Transaction Type (Debit/Credit/Transfer)
- Transaction Category (Shopping/Bills/Food/Entertainment/Travel/Other)
- Payment Method (Card/Bank Transfer/Mobile Wallet/Check/Cash)
- Device Type (Mobile/Desktop/Tablet)

**Binary Features:**
- Is International (Yes/No)

## Model Persistence

The trained model is saved in `ann_model.pkl` containing:
- Model architecture (JSON format)
- Model weights
- Scaler parameters (mean and scale)
- Feature column names

## Performance

- **Test Accuracy**: Varies based on the test set
- **Test Loss**: Depends on model training

View TensorBoard logs:

```bash
tensorboard --logdir=logs/fit
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'tensorflow'"

**Solution:**
```bash
pip install tensorflow-macos tensorflow-metal
```

### Issue: "FileNotFoundError: ann_model.pkl"

**Solution:**
Ensure the `ann_model.pkl` file is in the project root directory.

### Issue: Port 8000 already in use

**Solution:**
```bash
python manage.py runserver 8001
```

## Files Description

| File | Purpose |
|------|---------|
| `forms.py` | Django form for transaction input with validation |
| `views.py` | Core logic for loading model, preprocessing data, and making predictions |
| `urls.py` | URL routing for the predictor app |
| `base.html` | Base template with Bootstrap styling |
| `index.html` | Main form page for user input |
| `result.html` | Results page showing prediction and confidence scores |

## Features

✅ Real-time fraud detection using deep learning  
✅ User-friendly web interface  
✅ JSON API for programmatic access  
✅ Mobile-responsive design  
✅ Detailed prediction results with confidence scores  
✅ Transaction summary with recommended actions  
✅ Beautiful Bootstrap 5 UI with gradient styling  

## Security Notes

- Change `SECRET_KEY` in `fraud_detection/settings.py` before production deployment
- Set `DEBUG = False` for production
- Use environment variables for sensitive configuration
- Implement proper authentication for API endpoints

## Future Enhancements

- Add user authentication and transaction history
- Implement batch prediction for multiple transactions
- Add more sophisticated feature engineering
- Create admin dashboard for model monitoring
- Add email notifications for suspicious transactions
- Implement model retraining pipeline

## Support

For issues or questions, refer to:
- Django Documentation: https://docs.djangoproject.com/
- TensorFlow Documentation: https://www.tensorflow.org/docs
- The original Jupyter notebook: `ann_fraud_detection.ipynb`

## License

This project is for educational purposes.

from django.shortcuts import render
from django.http import JsonResponse
from .forms import TransactionForm
import pickle
import json
import numpy as np
import pandas as pd
from pathlib import Path
from tensorflow.keras.models import model_from_json
from sklearn.preprocessing import StandardScaler
import os

# Load the model globally
MODEL_DATA = None
SCALER = None
FEATURE_COLUMNS = None

def load_model():
    global MODEL_DATA, SCALER, FEATURE_COLUMNS
    
    if MODEL_DATA is None:
        model_path = os.path.join(os.path.dirname(__file__), '..', 'ann_model.pkl')
        
        with open(model_path, 'rb') as f:
            MODEL_DATA = pickle.load(f)
        
        # Reconstruct the model
        from tensorflow.keras.models import model_from_json
        model = model_from_json(MODEL_DATA['model_config'])
        model.set_weights(MODEL_DATA['model_weights'])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        MODEL_DATA['model'] = model
        
        # Reconstruct the scaler
        SCALER = StandardScaler()
        SCALER.mean_ = np.array(MODEL_DATA['scaler_mean'])
        SCALER.scale_ = np.array(MODEL_DATA['scaler_scale'])
        
        FEATURE_COLUMNS = MODEL_DATA['feature_columns']

def prepare_features(form_data):
    """Convert form data to feature vector matching the trained model"""
    # Define the columns in the same order as training
    selected_columns = [
        'customer_age', 'customer_gender', 'account_type', 'annual_income',
        'credit_score', 'account_tenure_months', 'transaction_hour', 'day_of_week',
        'transaction_type', 'transaction_category', 'payment_method', 'device_type',
        'amount', 'is_international', 'account_balance_after'
    ]
    
    # Create a DataFrame with the form data
    df = pd.DataFrame([form_data], columns=selected_columns + ['is_fraud'])
    
    # Handle numeric conversions
    numeric_cols = ['customer_age', 'annual_income', 'credit_score', 
                   'account_tenure_months', 'transaction_hour', 'amount', 'account_balance_after']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Apply one-hot encoding for categorical columns
    categorical_cols = ['customer_gender', 'account_type', 'day_of_week', 
                       'transaction_type', 'transaction_category', 'payment_method', 'device_type']
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    
    # Remove the is_fraud column if it exists
    if 'is_fraud' in df_encoded.columns:
        df_encoded = df_encoded.drop('is_fraud', axis=1)
    
    # Reindex to match training features
    df_encoded = df_encoded.reindex(columns=FEATURE_COLUMNS, fill_value=0)
    
    # Scale the features
    df_encoded[df_encoded.columns] = SCALER.transform(df_encoded[df_encoded.columns])
    
    return df_encoded.values

def index(request):
    """Render the prediction form"""
    form = TransactionForm()
    return render(request, 'predictor/index.html', {'form': form})

def predict(request):
    """Handle form submission and return prediction"""
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        
        if form.is_valid():
            try:
                # Load model if not already loaded
                load_model()
                
                # Prepare data
                form_data = {
                    'customer_age': form.cleaned_data['customer_age'],
                    'customer_gender': form.cleaned_data['customer_gender'],
                    'account_type': form.cleaned_data['account_type'],
                    'annual_income': form.cleaned_data['annual_income'],
                    'credit_score': form.cleaned_data['credit_score'],
                    'account_tenure_months': form.cleaned_data['account_tenure_months'],
                    'transaction_hour': form.cleaned_data['transaction_hour'],
                    'day_of_week': form.cleaned_data['day_of_week'],
                    'transaction_type': form.cleaned_data['transaction_type'],
                    'transaction_category': form.cleaned_data['transaction_category'],
                    'payment_method': form.cleaned_data['payment_method'],
                    'device_type': form.cleaned_data['device_type'],
                    'amount': form.cleaned_data['amount'],
                    'is_international': 1 if form.cleaned_data['is_international'] else 0,
                    'account_balance_after': form.cleaned_data['account_balance_after'],
                    'is_fraud': 0  # Placeholder
                }
                
                # Prepare features
                features = prepare_features(form_data)
                
                # Make prediction
                prediction = MODEL_DATA['model'].predict(features, verbose=0)[0][0]
                
                # Determine if fraud
                is_fraud = prediction > 0.5
                fraud_probability = float(prediction) * 100
                
                result = {
                    'success': True,
                    'is_fraud': is_fraud,
                    'fraud_probability': round(fraud_probability, 2),
                    'safe_probability': round(100 - fraud_probability, 2),
                    'amount': form.cleaned_data['amount'],
                }
                
                return render(request, 'predictor/result.html', result)
                
            except Exception as e:
                return render(request, 'predictor/index.html', {
                    'form': form,
                    'error': f'Prediction error: {str(e)}'
                })
        else:
            return render(request, 'predictor/index.html', {
                'form': form,
                'error': 'Please fill all fields correctly.'
            })
    
    return render(request, 'predictor/index.html', {'form': TransactionForm()})

def api_predict(request):
    """API endpoint for predictions (JSON)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Load model
            load_model()
            
            # Prepare data
            form_data = {
                'customer_age': data.get('customer_age'),
                'customer_gender': data.get('customer_gender'),
                'account_type': data.get('account_type'),
                'annual_income': data.get('annual_income'),
                'credit_score': data.get('credit_score'),
                'account_tenure_months': data.get('account_tenure_months'),
                'transaction_hour': data.get('transaction_hour'),
                'day_of_week': data.get('day_of_week'),
                'transaction_type': data.get('transaction_type'),
                'transaction_category': data.get('transaction_category'),
                'payment_method': data.get('payment_method'),
                'device_type': data.get('device_type'),
                'amount': data.get('amount'),
                'is_international': 1 if data.get('is_international') else 0,
                'account_balance_after': data.get('account_balance_after'),
                'is_fraud': 0
            }
            
            # Prepare features
            features = prepare_features(form_data)
            
            # Make prediction
            prediction = MODEL_DATA['model'].predict(features, verbose=0)[0][0]
            
            return JsonResponse({
                'success': True,
                'is_fraud': bool(prediction > 0.5),
                'fraud_probability': round(float(prediction) * 100, 2),
                'safe_probability': round(100 - float(prediction) * 100, 2),
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'POST request required'}, status=405)

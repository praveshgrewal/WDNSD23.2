import pickle
import os
import numpy as np
from django.shortcuts import render
from .forms import EmailForm

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'spam_model.pkl')

with open(MODEL_PATH, 'rb') as f:
    payload = pickle.load(f)
    model = payload['model']
    features = payload['features']


def predict(request):
    result = None
    confidence = None
    form = EmailForm()

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            input_data = np.array([[
                data['word_count'],
                data['num_links'],
                data['num_exclamations'],
                data['capital_ratio'],
                data['special_char_ratio'],
                int(data['has_html']),
                data['email_length'],
                data['sender_score'],
            ]])

            prediction = model.predict(input_data)[0]
            proba = model.predict_proba(input_data)[0]
            confidence = round(max(proba) * 100, 2)
            result = 'SPAM' if prediction == 1 else 'HAM'

    return render(request, 'classifier/index.html', {
        'form': form,
        'result': result,
        'confidence': confidence,
    })

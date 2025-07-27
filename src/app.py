import joblib
from urllib.parse import urlparse, parse_qs
import re
import urllib
import numpy as np
from scipy.sparse import hstack
import streamlit as st

# 모델 및 벡터라이저 로드
rf_model = joblib.load('rf_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

ip_pattern = r"(?:\d{1,3}\.){3}\d{1,3}"
shorteningServices = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net|buff\.ly|rb\.gy|rebrand\.ly|short\.cm|clk\.im|cutt\.ly|t2m\.io|bl\.ink|tiny\.cc"

def parse_query_string(url):
    if '?' not in url:
        return {}
    query_string = url.split('?')[-1]
    query_pairs = query_string.split('&')
    params = {}
    for pair in query_pairs:
        split_pair = pair.split('=', 1)
        key = split_pair[0]
        value = split_pair[1] if len(split_pair) > 1 else None
        params[key] = value
    return params

def extract_features(url):
    features = {}
    features['IP_LIKE'] = 1 if re.search(ip_pattern, url) else 0
    features['AT'] = 1 if "@" in url else 0
    features['URL_Depth'] = len([segment for segment in urlparse(url).path.split('/') if segment])
    features['Redirection'] = 1 if url.rfind('//') > 6 else 0
    features['Is_Https'] = 1 if urllib.parse.urlsplit(url).scheme == 'https' else 0
    features['TINY_URL'] = 1 if re.search(shorteningServices, url) else 0
    features['Query'] = len(parse_query_string(url))
    features['(-)_InDomain'] = 1 if '-' in urlparse(url).netloc else 0
    return features

def tokenize_url(url: str):
    tokens = []
    parsed_url = urlparse(url)
    domain_tokens = parsed_url.netloc.split('.')
    tokens.extend(domain_tokens)
    path_tokens = parsed_url.path.split('/')
    tokens.extend([token for token in path_tokens if token])
    query_tokens = parse_qs(parsed_url.query)
    for key, values in query_tokens.items():
        tokens.append(key)
        tokens.extend(values)
    return tokens

def predict_phishing(url: str):
    tokenized_url = ' '.join(tokenize_url(url))
    url_vector = vectorizer.transform([tokenized_url])

    features = extract_features(url)
    other_features = np.array([[features['IP_LIKE'], features['AT'], features['URL_Depth'], features['Redirection'],
                                features['Is_Https'], features['TINY_URL'], features['Query'], features['(-)_InDomain']]])

    final_vector = hstack([url_vector, other_features])

    prediction = rf_model.predict(final_vector)
    return prediction[0]

# Streamlit 애플리케이션
def main():
    st.title('Phishing URL Detector')

    url = st.text_input('Enter URL', '')

    if st.button('Predict'):
        if not url:
            st.error('Please enter a URL.')
        else:
            prediction = predict_phishing(url)
            result = 'Phishing' if prediction == 1 else 'Not Phishing'
            st.success(f'The URL is predicted as: {result}')

if __name__ == '__main__':
    main()

### ai_logic.py

PRODUCTS = [
    {
        "name": "BGF World Gold A2 USD BWGU",
        "risk": "High",
        "amount_range": "SGD 1,000 – 10,000",
        "objective": "High capital appreciation",
        "summary": "A unit trust focused on gold-related companies with strong growth potential.",
        "link": "https://www.hsbc.com.sg/investments/products/unit-trusts/fund-details/"
    },
    # Add more products here
]

def match_products(profile):
    matched = []
    for product in PRODUCTS:
        if (product["risk"].lower() == profile["risk"].lower() and
            product["objective"].lower() in profile["objective"].lower() and
            product["amount_range"] == profile["amount"]):
            matched.append(product)
    return matched


def predict_prices_for(product_name):
    import numpy as np
    import pandas as pd
    from sklearn.linear_model import LinearRegression

    history = {
        "BGF World Gold A2 USD BWGU": [5.1, 5.3, 5.5, 5.6, 5.8, 6.0]
    }

    prices = history.get(product_name)
    if not prices:
        return None

    X = np.array(range(1, len(prices)+1)).reshape(-1, 1)
    y = np.array(prices)

    model = LinearRegression()
    model.fit(X, y)

    future_months = np.array([[7], [8], [9]])
    forecast = model.predict(future_months)

    df = pd.DataFrame({
        "Month": ["Month 7", "Month 8", "Month 9"],
        "Predicted Price": forecast
    })
    return df


# Helper functions for sentiment analysis

def collect_social_data(tokens):
    """Dummy implementation"""
    return {token: {'twitter': 0.0, 'telegram': 0.0, 'reddit': 0.0} for token in tokens}

def compute_velocity(data):
    """Dummy implementation"""
    # Simple average of social scores
    velocities = {}
    for token, values in data.items():
        velocities[token] = sum(values.values()) / 3
    return velocities

def generate_alerts(velocity):
    """Dummy implementation - returns empty list"""
    alerts = []
    for token, vel in velocity.items():
        if vel > 0.5:  # dummy threshold
            alerts.append(f"High velocity detected for {token}: {vel}")
    return alerts
import requests

# Define the URL of your Flask app
url = 'http://localhost:5000/check_metrics.html'

# Send a POST request
response = requests.post(url)

# Print the response
print(response.text)

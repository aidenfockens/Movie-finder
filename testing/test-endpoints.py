import requests
api_key = "630b4e7c293ad229ae05e63103af19fe"
api_url = "http://localhost:5001/recommendations"
params = {
    "title": "Coraline",
    "media_type": "movie",
    "min_rating": 7.0  
}


response = requests.get(api_url, params=params)

# Check if the response is successful
if response.status_code == 200:
    try:
        recommendations = response.json()
        for movie in recommendations:
            print(f"Title: {movie['title']}, Rating: {movie['rating']}, Description: {movie['description']}")
    except ValueError:
        print("Error: Received a non-JSON response")
        print(response.text)  # Print the response text for debugging
else:
    print("Error: Received status code", response.status_code)
    print("Response content:", response.text)  # Print the full response for debugging

"# URL Shortener" 
To test in codespace terminal:
curl -X 'POST' \
  'http://localhost:8000/shorten' \
  -H 'Content-Type: application/json' \
  -d '{ "long_url": "https://github.com" }'
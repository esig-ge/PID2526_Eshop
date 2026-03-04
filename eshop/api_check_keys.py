
## Run this file to check if the environment variables are set correctly. You should see the values of the environment variables printed out.
## If some keys are missing, ask osman or abel to provide you with the correct keys
import os
print(os.getenv("API_KEY_OLLAMA"))
print(os.getenv("STRIPE_SECRET_KEY"))
print(os.getenv("STRIPE_PUBLISHABLE_KEY"))
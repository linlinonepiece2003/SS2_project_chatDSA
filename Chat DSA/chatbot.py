import openai

# Replace 'your-api-key' with your actual OpenAI API key
openai.api_key = 'sk-proj-2l3NpAj4bc7QU2Eryai7T3BlbkFJraamyZC6xfhMEAflSK8q'

def get_bot_response(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ]
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return "Oops, something went wrong."

# To test the function directly, you can uncomment the following lines:
# if __name__ == "__main__":
#     print(get_bot_response("Hello, how are you?"))
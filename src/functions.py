import sys
import google.generativeai as palm
import configparser

def get_api():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config.get('API', 'gemini_api_key', fallback=None)

def hs_neuraliser(input_text):
    api = get_api()
    palm.configure(api_key=api)
    model = palm.GenerativeModel('gemini-1.5-flash')
    prompt = ("Convert this speech to more humble and shouldn't offend anyone: ") + input_text
    response = model.generate_content(prompt)

    return response.text

def hs_detector(input_text):
    api = get_api()
    palm.configure(api_key=api)
    model = palm.GenerativeModel('gemini-1.5-flash')
    prompt = ("Can the following sentence hurt anyone and if about any political prompt reply as Yes, answer in "
              "Yes Or No only") + input_text

    try:
        # Generate the content using the model
        analysis_response = model.generate_content(prompt)

        # Convert response to lowercase and trim any excess whitespace
        response_text = analysis_response.text.strip().lower()

        # Determine the decision based on the response
        if response_text == "yes":
            return True
        elif response_text == "no":
            return False
        else:
            # Handle unexpected responses
            print("Unexpected response:", response_text)
            return None

    except ValueError as error:
        print("Error:", error)

        # Specific check for the known error message
        if str(error) == ("Invalid operation: The `response.text` quick accessor requires the response to contain "
                          "a valid `Part`, but none were returned. Please check the `candidate.safety_ratings` to "
                          "determine if the response was blocked."):
            return True  # Assume potentially harmful content

        # Default return value in case of unexpected failures
    return None
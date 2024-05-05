from flask import Flask, jsonify
from flask import request as req
from flask_cors import CORS
from llama_cpp import Llama
import sys
import pandas as pd
from llama_cpp import Llama
import os
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Llama
# LLM = Llama(
#     model_path="C:\Isfand\eestech\hackathon\examples\llama-2-7b-chat.Q5_K_M.gguf",
#     n_ctx=2048,
# )


@app.route("/analyze_issue_hardcoded", methods=["POST"])
def analyze_issue_hardcoded():
    user_message = req.json.get("user_message")
    response = (
        "Hi, I'm Llama. Nice to meet me. \n Your message was this: " + user_message
    )
    return jsonify({"response": response})


def process_for_issue_id(user_message):
    try:
        issue_id = int(user_message)
    except ValueError:
        issue_id = -1
    return issue_id


# Define endpoint
@app.route("/analyze_issue", methods=["POST"])
def analyze_issue():
    # Get issue ID from the request
    user_message = req.json.get("user_message")

    issue_id = process_for_issue_id(user_message)

    if issue_id == -1:
        return jsonify({"errorFound": "true", "message": "The issue ID is not a number"})
    
    

    LLM = Llama(model_path="llama-2-7b-chat.Q8_0.gguf", n_ctx=4096, seed=42, n_batch=1024, verbose=False)
    # LLM = Llama(model_path="llama-2-7b-chat.Q5_K_M.gguf", n_ctx=4096, seed=42, n_batch=1024, verbose=False)

    # Read issue Dataframe from Pickle file
    #df = pd.read_pickle('github_issues.pkl')
    df = pd.read_pickle('github_issues_team10.pkl')

    # Only take issues, no pull requests
    df = df.loc[df['pr'] == 'issue']

    def get_sample_by_index(index):
        if index < 0 or index >= len(df):
            raise ValueError("Index out of range")
        return df.iloc[index]

    # if len(sys.argv) != 2:
    #     print("Usage: python script.py <index>")
    #     sys.exit(1)
    try:
        index = df.index.get_loc(str(issue_id))
    except KeyError:
        return jsonify({"errorFound": "true", "message": "There is no issue with this issue ID"})

    try:
        # index = int(sys.argv[1])
        sample = get_sample_by_index(index)
    except ValueError:
        print("Index must be an integer")
        sys.exit(1)
    except IndexError:
        print("Index out of range")
        sys.exit(1)

    subject = sample['title']
    request = sample['body']
    comment = sample['comment']
    repo_name = sample['repo_name']
    pr=sample['pr']
    state=sample['state']
    created=sample['created']
    closed=sample['closed']
    url=sample['url']
    url = sample['url'].replace('https://api.github.com/repos', 'https://github.com')
    id = sample.name

    # Define the Characters dataframe
    Characters = pd.DataFrame(columns=['Character', 'Description'])

    # Assign character descriptions
    Herald=Characters.loc['Herald'] = ['Herald', 'Herald is the customer support manager. He analyzes the response times of the support team and ensures that they meet the desired standards. He focuses on improving the efficiency of issue resolution processes provided to the customers and tracks overall satisfaction. His goal is to reduce response time and improve customer satisfaction.']
    Daniel=Characters.loc['Daniel'] = ['Daniel', 'Daniel is the customer experience designer. He analyzes the accuracy and relevance of the support team responses and ensures that support team communications are clear, concise, and easily understandable for customers. He works on improving the quality and accessibility of documentation and resources provided to customers. His goal is to enhance the overall customer experience']
    Sarah=Characters.loc['Sarah'] = ['Sarah', 'Sarah is the marketing manager. She analyzes the support team responses and ensure that support team interactions are empathetic and friendly towards the customers, aligning with the company brand values.'] 
    #    She analyzes customer support requests and responses to identifies trends. Her goal is to help to attract and retain customers']

    print(30*'-')
    print('Selected issue:')
    print(f"Subject: {subject}")
    print(f"Request: {request}")
    print(30*'-')





    def find_first_date(text):
        # Define the regular expression pattern for YYYY-MM-DD format
        date_pattern = r'\b\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}\b'
        
        # Search for the first occurrence of the pattern in the text
        match = re.search(date_pattern, text)
        
        # If a match is found, return the matched date
        if match:
            return match.group(0)
        else:
            return None

    # Example usage:
    # for item in new_df['comment']:
    # item = new_df.loc[21,'comment']
    item = str({comment})
    issue= f"{created}"
    closed = f"{closed}"
    print(item)
    print(issue)

    issue_date = find_first_date(issue)
    first_date = find_first_date(item)
    closed_date = find_first_date(closed)
        # break



    # create a text prompt
    prompt = f'The following is a customer request. Based on the duration between the Issue date and the First Response date: (Date Format is : YYYY-MM-DD HH:MM:SS±HH:MM), estimate the response time and translate it in a number between 1 (bad) and 5 (excellent):\n \
    "Issue date: {issue_date} \
    First Response date: {first_date}"'

    # Generate a response (takes several seconds to minutes)
    response_time = LLM(prompt, max_tokens=0)

    # Display the response
    print('Response Time:')
    print(response_time["choices"][0]["text"])


    # create a text prompt
    prompt = f'The following is a customer request. Estimate the quality of response based on the accuracy and relevance of the support team responses from the Comments section to this request and translate it in a number between 1 (not good) and 5 (excellent):\n \
    "Subject: {subject} \
    Request: {request} \
    Comments: {comment} \
    Issue Created: {created} \
    Issue Closed: {closed}"'

    # Generate a response (takes several seconds to minutes)
    quality_of_response = LLM(prompt, max_tokens=0)

    # Display the response
    print('Quality of Response:')
    print(quality_of_response["choices"][0]["text"])


    # create a text prompt
    prompt = f'The following is a customer request. Estimate the customer satisfaction based on the gathered feedback from customers about their overall satisfaction with the support they received team responses from the Comments section, date/time of the response and translate it in a number between 1 (not good) and 5 (excellent):\n \
    "Subject: {subject} \
    Request: {request} \
    Comments: {comment} \
    Issue Created: {created} \
    Issue Closed: {closed}"'

    # Generate a response (takes several seconds to minutes)
    customer_satisfaction = LLM(prompt, max_tokens=0)

    # Display the response
    print('Customer Satisfaction:')
    print(customer_satisfaction["choices"][0]["text"])



    # create a text prompt
    prompt = f'The following is a customer request. Estimate the friendliness of the customer support based on the Comments and translate it in a number between 1 (not good) and 5 (excellent):\n \
    "Subject: {subject} \
    Request: {request} \
    Comments: {comment} \
    Issue Created: {created} \
    Issue Closed: {closed}"'

    # Generate a response (takes several seconds to minutes)
    friendliness = LLM(prompt, max_tokens=0)

    # Display the response
    print('Friendliness:')
    print(friendliness["choices"][0]["text"])


    # prompt = f'Summarize the below texts:\n \
    # "Response Time: {response_time["choices"][0]["text"]} \
    # Resolution Time: {resolution_time["choices"][0]["text"]} \
    # Quality of Response: {quality_of_response["choices"][0]["text"]} \
    # Customer Satisfaction: {customer_satisfaction["choices"][0]["text"]} \
    # Friendliness: {friendliness["choices"][0]["text"]}"'

    # output_general = LLM(prompt, max_tokens=0)

    # # Display the response
    # print('General Summary:')
    # print(output_general["choices"][0]["text"])




    # create a text prompt for Harald, the customer support manager
    prompt = f'Below is a customer request along with the supplimentary information\n \
    "Subject: {subject} \
    Request: {request} \
    Comment: {comment} \
    Repo Name: {repo_name} \
    Type: {pr} \
    State: {state} \
    Issue Created: {created} \
    Issue Closed: {closed} \
    Response Time: {response_time["choices"][0]["text"]} \
    Quality of Response: {quality_of_response["choices"][0]["text"]} \
    Customer Satisfaction: {customer_satisfaction["choices"][0]["text"]} \
    Friendliness: {friendliness["choices"][0]["text"]}" \
    Now, read through the character {Herald} and give an opinion on the customer support as per his role. mention the reasoning behind his opinion and suggest where it can improve: '

    # Generate a response (takes several seconds to minutes)
    output_herald = LLM(prompt, max_tokens=0)

    # Display the response
    print("Herald's Feedback:")
    print(output_herald["choices"][0]["text"])



    # create a text prompt for Daniel, customer experience designer
    prompt = f'Below is a customer request along with the supplimentary information\n \
    "Subject: {subject} \
    Request: {request} \
    Comment: {comment} \
    Repo Name: {repo_name} \
    Type: {pr} \
    State: {state} \
    Issue Created: {created} \
    Issue Closed: {closed} \
    Response Time: {response_time["choices"][0]["text"]} \
    Quality of Response: {quality_of_response["choices"][0]["text"]} \
    Customer Satisfaction: {customer_satisfaction["choices"][0]["text"]} \
    Friendliness: {friendliness["choices"][0]["text"]}" \
    Now, read through the character {Daniel} and give an opinion on the customer support as per his role. mention the reasoning behind his opinion and suggest where it can improve: '

    # Generate a response (takes several seconds to minutes)
    output_daniel = LLM(prompt, max_tokens=0)

    # Display the response
    print("Daniel's Feedback:")
    print(output_daniel["choices"][0]["text"])


    # create a text prompt for Sarah, customer experience designer
    prompt = f'Below is a customer request along with the supplimentary information\n \
    "Subject: {subject} \
    Request: {request} \
    Comment: {comment} \
    Repo Name: {repo_name} \
    Type: {pr} \
    State: {state} \
    Issue Created: {created} \
    Issue Closed: {closed} \
    Response Time: {response_time["choices"][0]["text"]} \
    Quality of Response: {quality_of_response["choices"][0]["text"]} \
    Customer Satisfaction: {customer_satisfaction["choices"][0]["text"]} \
    Friendliness: {friendliness["choices"][0]["text"]}" \
    Now, read through the character {Sarah} and give an opinion on the customer support as per his role. mention the reasoning behind his opinion and suggest where it can improve: '

    # Generate a response (takes several seconds to minutes)
    output_sarah = LLM(prompt, max_tokens=0)

    # Display the response
    print("Sarah's Feedback:")
    print(output_sarah["choices"][0]["text"])



    # Create a DataFrame with the outputs
    df_output = pd.DataFrame({
        'Title': [subject],
        'URL': [url],
    #   'General Feedback': [output_general["choices"][0]["text"]],
        'Herald Feedback': [output_herald["choices"][0]["text"]],
        'Daniel Feedback': [output_daniel["choices"][0]["text"]],
        'Sarah Feedback': [output_sarah["choices"][0]["text"]]
    })
    
    herald_output = output_herald["choices"][0]["text"]
    daniel_output = output_daniel["choices"][0]["text"]
    sarah_output = output_sarah["choices"][0]["text"]
    
    chatbox_message = "Thank you for your patience. Our team has processed the information and here are the insights: \n\n **Harald's Insights:** \n" + herald_output + "\n\n" + "**Daniel's Insights:** \n\n" + daniel_output + "\n\n" + "**Sarah's Insights:** \n" + sarah_output + "\n\nHope these insights will help you improve customer experience. \n"


    return jsonify(
        {
            "chatbot_message": chatbox_message
        }
    )
    
    return jsonify(
        {
            "chatbot_message": "blah"
        }
    )



    # # Generate responses
    # output_herald = LLM(prompt_herald, max_tokens=0)
    # output_daniel = LLM(prompt_daniel, max_tokens=0)
    # output_sarah = LLM(prompt_sarah, max_tokens=0)
    # output_julian = LLM(prompt_julian, max_tokens=0)

    # return jsonify(
    #     {
    #         "herald_output": output_herald["choices"][0]["text"],
    #         "daniel_output": output_daniel["choices"][0]["text"],
    #         "sarah_output": output_sarah["choices"][0]["text"],
    #         "julian_output": output_julian["choices"][0]["text"],
    #     }
    # )


if __name__ == "__main__":
    app.run(debug=True)

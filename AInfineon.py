# load the large language model file
import sys
import pandas as pd
from llama_cpp import Llama
import os
import re

LLM = Llama(model_path="llama-2-7b-chat.Q8_0.gguf", n_ctx=4096, seed=42, n_batch=1024, verbose=False)

# Read issue Dataframe from Pickle file
#df = pd.read_pickle('github_issues.pkl')
df = pd.read_pickle('github_issues_team10.pkl')

# Only take issues, no pull requests
df = df.loc[df['pr'] == 'issue']

def get_sample_by_index(index):
    if index < 0 or index >= len(df):
        raise ValueError("Index out of range")
    return df.iloc[index]

if len(sys.argv) != 2:
    print("Usage: python script.py <index>")
    sys.exit(1)

try:
    index = int(sys.argv[1])
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

issue_date = find_first_date(issue)
first_date = find_first_date(item)
closed_date = find_first_date(closed)



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
    'Herald Feedback': [output_herald["choices"][0]["text"]],
    'Daniel Feedback': [output_daniel["choices"][0]["text"]],
    'Sarah Feedback': [output_sarah["choices"][0]["text"]]
})

# Append the DataFrame to the CSV file
#df_output.to_csv('outputs.csv', mode='a', header=False, index=False)

# Check if the file exists
if not os.path.isfile('outputs.csv'):
    # If the file does not exist, write the DataFrame with the header
    df_output.to_csv('outputs.csv', mode='w', header=True, index=False)
else:
    # If the file does exist, append to it without writing the header
    df_output.to_csv('outputs.csv', mode='a', header=False, index=False)
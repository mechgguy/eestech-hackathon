# eestech-hackathon
# Hackathon Submission: Customer Experience Enhancement with Public Data and Generative AI

## Introduction
This repository contains the submission of Team 10 for the Hackathon organized by EESTEC LC Aachen in partnership with Infineon. Our project aims to enhance customer experience using public data and generative AI.

## Problem Statement
The topic of the hackathon is "How can we improve customer experience with public data and generative AI?". Our team proposes a solution UI, which is a CLI and a web UI chatbot type built on top of the CLI, utilising a Large Language Model (LLM)-based model. The model provides feedback to different personas, acting as customers, by analyzing their comments and suggesting improvements. More details on problem statement can be found at [github](https://github.com/Infineon/hackathon).

## Solution Overview
Our solution is a UI which is based on a Large Language Model (LLM) that analyzes customer comments and provides tailored feedback to improve their experience. We have identified and defined customer experience metrics, both abstract and non-abstract, by considering various customer personas and viewpoints. By leveraging public data and generative AI, our model offers effective and consistent predictions on how issues and comments can be handled better to enhance customer satisfaction. The UI is a CLI `AInfineon.py` and a web UI `flask-api.py`, the UI takes in the issue as input and gives output the generalised feedback for the issue resolution and personalised feedback to different personas so as to improve end-user customer experience. The [solution video]() can be found. 

## Key Features
- Large Language Model (LLM)-based solution.
- Feedback generation for different customer personas and the end-user customer.
- Definition and analysis of abstract and non-abstract customer experience metrics.
- Prompt Engineering so as to generate robust and homogenous responses for many different types of issues. 
- Leveraging public data and generative AI for enhanced predictions.
- We propose a web UI and a CLI for demonstration for our work.

## How It Works
1. **Data Collection**: We gather customer comments and related data from public sources. For our current dummy implementation we used the pickle data of github issues `github_issues.pkl` (and further with user comments). 
2. **Preprocessing**: The data is preprocessed to remove noise and irrelevant information. We identified that some of the entries in the master pickle file comprised of Bot or automated github pull-requests and pull-requests in general which we processed as not relevant to the task at hand and so were discarded due to the fact that any inference derieved from such issues would not contribute to improving customer experience. The details on precprocessing including discussions can be found in the following python notebook `data-preprocessing.ipynb`. Some information was observed during preprocessing, mainly the fact that we needed more information about user comments to get more context for us and as an input to the LLM for better understanding of the history of an issue, to this purpose edits were made in `fetch_github_issues.py` to gather information about comments, comment history and more information over issues.
3. **Model Selection**: We selected the Language Model (LLM) with respect to the computational and compatibility requirements of the task at hand. It was noted that although real time behaviour is not required, the model should process eaxh isuue within 10 minutes of standard time in a normal PC equipped with 16GB CPU RAM and no GPU. We used a naÏve chat-based state-of-the-art LLM since it can be remarked that the train data was not enough to notice any change in the model's output or performance.
4. **Processing an Issue**: Go through an issue with its comment history and process it through the LLM to get potential failpoints where users could have handled the situation better. This is made possble by running through the web UI or the CLI. More details on implementation can be found in section **Getting Started**.
5. **Feedback Generation**: The model analyzes customer comments and generates feedback tailored to different personas. Another key feature of the model is to provide different feedback to different personas using them, after consideration of their responsibilities, goals etc.
6. **Evaluation Metric Definition**: Another key endevour in the project is to define customer experience. We considered customer experience with respect to different personas within the organisation and the customer (end-user) as well, outside the organisation. Thus many numerable and abstract metrics.
7. **Evaluation**: We evaluate the effectiveness of the feedback generated by the model using various custom-defined metrics.

## Customer Experience Definition
The tool was to be used by 4 users of different personas, Harald, Julian, Daniel and Sarah, as an example. These users and many other part of the company used the tool in order to get feedback to ultimately better the customer experience. So, we put us into their roles and also to the shoes of the customer and identified the following parameters to be used as performance metrics by our LLM.
- **Response Time**: calculate the time between creation of the issue and the first comment to the issue and evaluate if that is reasonable with respect to the issue.
- **Resolution Time**: calculate the time between creation of the issue and the resolution to the issue and evaluate if that is reasonable with respect to the issue.
- **Response Effectiveness**: read the comments and the sequence of comments to the issue and evaluate if that helps the customer or in resolution of the issue.
- **Empathy and Friendliness**: read the tone of users' comments to the issue and evaluate if the comments are valid, helpful and unbaised especially with respect to knowledge level and experience of the user.
- **Customer Satisfaction**: read customer comments (if any) and evaluate if the activity in the issue was helpful to the customer. 

"Please note that while the data processed by the LLM model is not restricted to predefined performance parameters, the model will analyze both the provided data and prompts semantically. Consequently, it will generate responses based on these parameters outlined in the prompts, while also considering the semantic context of the inputs."

The parameters were identified as being the most important to the end-user, the customer and are listed in no particular order. These metrics were used in the prompt engineering and the LLM should consider them while making comments on the user comments to better customer experience.

## Prompt Engineering
Prompt engineering involves crafting specific prompts or instructions given to a language model to produce desired outputs. The goal of this exercise is to guide the model towards generating outputs that align with the intended objective. The focus on Prompt Engineering is to ask the correct questions and getting the precise and homogenous answers and parsing them in an effectively readable and understandble format. Following are some examples data where we brainstormed for the correct prompt while prompt training.

For eg. we remarked that using english in 1st person in prompt was making the model ambiguous to different persons or stakeholders involved. Thus we encouraged the repeated use of proper nouns (person names rather than he,she,it) for our prompt to make relationships and information flow clear, even if the prompt reads strange in colloquial English speech.  

## Getting Started
To get started with our project, follow these steps:
1. Clone this repository to your local machine.
2. Install the required dependencies <as mentioned in the `requirements.txt` file.>
* Note: We have used the following LLM model for our implementation [llama-2-7b-chat.Q4_K_M.gguf](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/blob/main/llama-2-7b-chat.Q4_K_M.gguf), if you wish to use other models do not forget to change your references in the individual scripts.
4. Collect and prepare the required data to send to the preprocessing step. Here we can correspond it to `github_issues.pkl`.
5. Preprocess the data by identifying its patterns and its redundancies and remove the extra information. Here we can correspond to `fetch_github_issues.py`.
6. Work on your prompt, engineer it, perform trial-and-error iterations with `AInfineon.py` till you get satisfactory results.
7. Your model and prompt is ready to be deployed in the UI.
8. We have developed a Command Line UI and a Web UI on top of it.
9. To launch the Command Line UI launch the `AInfineon.py` script with the appropriate issue number.
10. To launch the web UI, you need npm, so install it
11. Go to ~/Chatbot and further run `npm install`, it will install all libraries required for the front-end and then run `npm start` and it will start the front-end.
13. You would see terminal with server starting detail on some port.
14. Run the `flask-api.py` script.
15. Give the issue number as input to the chatbot.
16. We envisage to build a fully capable chatbot as an application had we had more time on the project. 

## Project Outcome Overview
- We have some inroads in preprocessing of data and have a semantic understanding of the pickle data provided. We have recognised some defunct columns which do not add to the variety or the utility of the LLM model.
- We have dereived a correct prompt with formatting of the result such as to obtain a robust result output from the LLM which can be used by internal users so as to improve the customer experience.
- We also have UIs in Command Line and Web based supoorting our work, both use the same scripts and model for implementation and are rudimentary in nature.

## Future Improvement Outlook
As stated with more time duration, the team could have worked more on getting the data from the Infineon User Community using a web scrapper. A dummy version was tried and the title of the issues was obtained but it was observed that to gather all the information was too complex and time consuming so the endeavour was abandoned.

Another area where focus was left out was the comparision and implementation of different LLMs and their finetuning over the input data. We remarked that such a small amount of data would not create an appreciable change in the internet scaled trained state of the art LLMs used. Also, we did glance over the hyperparameters of the model selected but that was too forgone over other priority issues like prompt engineering.

We started working on the UI on the final day, and would like to improve much on this rudimentary UI. The current UI comprise of a command line UI and a web UI. We envisage better post processing and better visualisation had more time been available.

## Special Section (Feedback to Organisers)
- We would have liked if the competition was bigger and better advertised.
- We would have liked if technical support be provided in person for all days.
- We would have liked if we would have been provided with a common cloud cluster to compensate for different infrastructures and computational capabilities of personal laptops for a competition involving generative AI.
- We would have liked it better if the final presentation was in person.

## Contributors
Team 10 EESTEC LC Aachen AI Hackathon 2024
- [Manas Mehrotra](https://github.com/mechgguy)
- [Kh Safkat Amin](https://github.com/khsafkatamin)
- [Isfandyar Siddiqui](https://github.com/isfand-yar)

Endeavour overtaken between the 03.05.2024-05.05.2024

## Acknowledgements
We would like to thank EESTEC LC Aachen and Infineon for organizing this hackathon and providing us with the opportunity to work on such an exciting project.

## License
This project is licensed under the [MIT License](https://www.mit.edu/~amini/LICENSE.md).

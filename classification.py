from langchain_ollama import OllamaLLM

# prompt template
def build_prompt(comment):
    prompt =  f"""
    Review the following comment and classify it as technical feedback or use case scenario. 
    ''' 
    {comment}
    '''
    """
    return prompt

#sample comment
comment = "I think the API should use a POST request instead of a GET request."



# specifiy the model to use 
model = OllamaLLM(model="llama3.2:1b")

# invoke the model 
prompt = build_prompt(comment)
result = model.invoke(input=prompt)
print(result)

# categories to classify the comment 
CLASSIFICATIONS = {
    "Technical Feedback": "technical_feedback",
    "Use Case": "use_case",
    "Feature Request": "feature_request",
    "Administrative": "administrative",
    "Conclusion / Resolution": "conclusion_resolution",
    "Philosophical": "philosophical",
    "Unknown": "unknown"
}

import json
from const.llm import MAX_GPT_MODEL_TOKENS

def process_text(text: str) -> str:
    """
    This function processes the input text and ensures that it is within the maximum token limit
    of the GPT model.
    """
    # Check if the text length is within the maximum token limit
    if len(text) > MAX_GPT_MODEL_TOKENS:
        # If the text is too long, truncate it and add an ellipsis
        text = text[:MAX_GPT_MODEL_TOKENS - 3] + "..."
    return text

if __name__ == "__main__":
    # Get some text from user input or a file
    text = "This is a long piece of text that needs to be processed by the GPT model."
    
    # Process the text
    processed_text = process_text(text)
    
    # Print the processed text
    print(processed_text)

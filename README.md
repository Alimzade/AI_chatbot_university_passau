# University of Passau AI Assistant Chatbot

This AI assistant helps students of the University of Passau by answering questions about teaching modules from the M.Sc. AI Engineering and M.Sc. Computer Science module catalogs. It also has the potential to be expanded with more use cases and content from the University's homepage.

## Features

* Answers questions about teaching modules
* Vectorized using Sentence Transformer model
* LLM of your choice: OpenAI, Mistral AI etc.
* Conversational capabilities (not just querying)
* Potential for expansion with more content and use cases

## Running the Project

To run the UniPassau Assistant UI, execute the following command in your terminal:

```bash
pip install requirements.txt
python -m uvicorn app.app:app --reload 

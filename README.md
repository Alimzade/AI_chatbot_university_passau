# AI Assistant Chatbot - University of Passau

This AI assistant helps students of the University of Passau by answering questions about teaching modules from the M.Sc. AI Engineering and M.Sc. Computer Science module catalogs. It also has the potential to be expanded with more use cases and content.

<img width="1570" height="1276" alt="unichat" src="https://github.com/user-attachments/assets/1c934dc8-1c42-49bb-b9aa-97a733c42a55" />


## Features

* Answers questions about teaching modules
* Vectorized using Sentence Transformer model
* LLM of your choice: OpenAI, Mistral AI etc.
* Conversational capabilities (not just querying)
* Potential for expansion with more content and use cases

## Libraries

* pandas, scikit-learn
* pdfplumber
* transformers, sentence-transformers
* uvicorn, fastapi

## Running the Project

To run the University Chat UI, execute the following commands in your terminal:

```bash
pip install requirements.txt
python -m uvicorn app.app:app --reload 

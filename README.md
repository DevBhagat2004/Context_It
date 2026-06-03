# Context_It

Most LLMs running on a laptop have a limited context window — they can only process a certain amount of text at once. Feeding an entire long document directly into a local model is often impossible, and even when it works, it is slow, uses a lot of memory, and forces the model to wade through large amounts of irrelevant information just to answer a simple question.

This project solves that problem by building a RAG pipeline entirely from scratch, with no paid APIs and no cloud dependencies. Instead of feeding the whole document to the LLM, the pipeline retrieves only the most relevant chunks of a document based on the user's query, and passes just those to the model. The LLM only ever sees a small, focused slice of information that is directly relevant to the question being asked.

The result is a system that can handle large documents on a regular laptop, uses far less resources than whole-document approaches, and produces faster response times — because the model is doing less work on more targeted input.

Everything runs locally. The embedding model, the vector database, and the LLM itself all run on your machine with no internet connection required after the initial setup.
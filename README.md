# Context_It

Most AI models running on a laptop can only read a certain amount of text at once. Feeding an entire long document directly into a local model is often impossible, and even when it works, it is slow, uses a lot of memory, and forces the model to go through large amounts of irrelevant information just to answer a simple question.

This project solves that problem by building a pipeline that works like a smart filter. Instead of handing the whole document to the AI, the system first finds only the parts of the document that are actually relevant to the question being asked, and passes just those parts to the model. The model then only has to read a small, focused chunk of information to give an answer.

The result is a system that can handle large documents on a regular laptop, uses far less memory and processing power than feeding the whole document at once, and responds faster because the model is doing less work on more targeted input.

Everything runs on your own machine. Nothing is sent to the internet or any paid service after the first time the models are downloaded.
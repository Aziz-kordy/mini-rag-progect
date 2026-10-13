from string import Template 

system_prompt=Template("\n".join(["you read the text and answer from the text"]))

document_prompt=Template("\n".join(["##Document NO:$doc_num","### Content:$chunk_text"]))


footer_prompt=Template("\n".join(["Answer only using the provided context. If the answer isn't in the context, say you don't know.","## answer:"]))
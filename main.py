import utils

# Example question
question = "Could you please provide the list of Products that are available in stock ?"
print("Input Question is: ", question)
answer = utils.query_llm(question)
print(answer)


question = "Could you please provide the Order status for order number 89086"
print("Input Question is: ", question)
answer = utils.query_llm(question)
print(answer)

question = "Could you please provide the Product Price for Wireless Headphones ?"
print("Input Question is: ", question)
answer = utils.query_llm(question)
print(answer)
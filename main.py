from chatbot import chatBot

# chatBot_ = chatBot()
# print(chatBot_.check_status())
# chatBot_.get_channel_id("chatbot-test")
# chatBot_.post_msg()

print('start init chatbot structure')
chatBot_ = chatBot()
print('finish chatbot structure')
# print(chatBot_.check_status())
chatBot_.get_channel_id("chatbot-test")
print('finish get channle id process in chatbot structure')
chatBot_.post_msg()
print('finish post msg using chatbot method')

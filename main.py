from chatbot import chatBot

chatBot_ = chatBot()
print(chatBot_.check_status())
chatBot_.get_channel_id("chatbot-test")
chatBot_.post_msg()
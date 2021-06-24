from chatbot import chatBot

chatBot_ = chatBot()
print(chatBot_.check_status())
chatBot_.get_channel_id("always-ready")
chatBot_.post_msg()
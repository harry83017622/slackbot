# from chatbot import chatBot


# print('start init chatbot structure')
# chatBot_ = chatBot()
# print('finish chatbot structure')
# # print(chatBot_.check_status())
# chatBot_.get_channel_id("chatbot-test")
# print('finish get channle id process in chatbot structure')
# chatBot_.post_msg()
# print('finish post msg using chatbot method')


import control.control as ctllr

# daily update
# remove this function and just call ctllr.daily_update() when test
def entry_point(request):
    ctllr.daily_update()
    print("finish daily update")
    return "task done"
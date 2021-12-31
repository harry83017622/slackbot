import control.control as ctllr

# daily update
# remove this function and just call ctllr.daily_update() when test
def entry_point(request):
    ctllr.daily_update()
    print("finish daily update")
    return "task done"
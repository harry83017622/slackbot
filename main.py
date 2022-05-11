import control.control as ctllr

# daily update
# just call ctllr.daily_update(use_local_src=True) when test
# ctllr.daily_update(use_local_src=True, upload=False)


def entry_point(request):
    ctllr.daily_update(use_local_src=False)
    print("finish daily update")
    return "task done"

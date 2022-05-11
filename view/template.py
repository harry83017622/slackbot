def create_template(user_points: list):
    blocks_head = [
        {"type": "divider"},
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "Daily Ranking", "emoji": True},
        },
    ]
    blocks_body = []

    for writer, nums in user_points:
        print(writer, nums)

        stars = ":star:" * nums
        blocks_body.append(
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*{writer}*\n{stars}\n"},
            }
        )

    blocks_end = [
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": """
                    *~Now move your ass and start coding~*
                     :cat: <https://leetcode.com/|Leetcode>
                    """,
            },
        },
    ]
    blocks = blocks_head + blocks_body + blocks_end
    return blocks

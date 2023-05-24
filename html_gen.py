def posts_html(posts, channel):
    html = ""
    phtml = """<a href="/stream/{channel}/{id}"><div class="col">
                    <div class="card shadow-sm">
                        <img class="lzy_img" src="https://cdn.jsdelivr.net/gh/TechShreyash/AnimeDex@main/static/img/loading.gif" data-src="{img}" alt="{title}">
                        </img>
                        <div class="card-body">
                            <h6 class="card-subtitle">{title}</h5>
                        </div>
                    </div>
                </div></a>"""
    for post in posts:
        html += phtml.format(
            id=post["msg-id"],
            img=f"/api/thumb/{channel}/{post['msg-id']}",
            title=post["title"],
            channel=channel,
        )
    return html

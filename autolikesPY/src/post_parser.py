class Post:
    def __init__(self, id, author, liked, author_group):
        self.id = id
        self.author = author
        self.liked = liked
        self.author_group = author_group

def parse_post(post):
    post_id = int(post.attrs['id'].split('-').pop())
    author = post.select_one('.messageInfo .username')
    liked = post.select_one('.LikeLink') and 'unlike' in post.select_one('.LikeLink').attrs.get('class', [])

    author_span = author.select_one('span') if author else None
    is_uniq = 'style' in author_span.attrs if author_span and 'attrs' in author_span else False
    author_class = author_span.attrs['class'] if author_span and 'class' in author_span.attrs else []

    return Post(
        id=post_id,
        liked=liked or False,
        author=author.get_text() if author else '',
        author_group=999 if is_uniq else int(author_class[0][5:]) if author_class else 0
    )

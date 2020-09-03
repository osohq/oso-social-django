# Allow anyone to view any public posts.
allow(_actor, "view", post: Post) if
    post.access_level = Post.ACCESS_PUBLIC;

# Allow a user to view their private posts.
allow(actor: User, "view", post: Post) if
    post.access_level = Post.ACCESS_PRIVATE and
    post.created_by = actor;

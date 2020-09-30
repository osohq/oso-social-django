# Allow anyone to view any public posts.
allow(_actor, "view", post: social::Post) if
    is_public(post);

# Allow a user to view their private posts.
allow(actor: social::User, "view", post: social::Post) if
    is_private(post) and
    post.created_by = actor;

allow(actor: social::User, "view", _: social::Post) if
    actor.is_moderator();

is_public(post: social::Post) if post.access_level = social::Post.ACCESS_PUBLIC;
is_private(post: social::Post) if post.access_level = social::Post.ACCESS_PRIVATE;

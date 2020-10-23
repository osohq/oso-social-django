# Allow anyone to view any public posts.
allow(_actor, "read", post: social::Post) if
    post.access_level = social::Post.ACCESS_PUBLIC;

# Allow a user to view their private posts.
allow(actor: social::User, _action, post: social::Post) if
    post.created_by = actor;

# Allow by role
allow(user: social::User, action: String, post: social::Post) if
    action in ["read", "create", "update", "delete"] and
    role = user.role_set.all() and
    role.created_by.id = post.created_by.id and
    permission = role.permissions.all() and
    permission.get_resource() = "post" and
    permission.get_action() = action;
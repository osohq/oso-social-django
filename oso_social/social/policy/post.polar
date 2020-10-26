
## POST RESOURCES

# Allow anyone to view any public posts.
allow(_actor, "read", post: social::Post) if
    post.access_level = social::Post.ACCESS_PUBLIC;

# Allow a user to manage their posts.
allow(actor: social::User, _action, post: social::Post) if
    post.created_by = actor;

# Dynamic roles
# TODO: make this rule generic by adding a base model that has a name and created_by field
allow(user: social::User, action: String, post: social::Post) if
    allow_by_custom_role(user, action, "post", post);

# allow based on custom roles
allow_by_custom_role(user: social::User, action: String, resource_name: String, resource) if
    role = user.role_set.all() and
    role.created_by =  resource.created_by and
    permission = role.permissions.all() and
    permission.get_resource() = resource_name and
    permission.get_action() = action;

## ROLE RESOURCES

# Allow a user to manage their roles.
allow(actor: social::User, _action, role: social::Role) if
    role.created_by = actor;

# A user is allowed to delete a permission if they are allowed to update a role
allow(actor: social::User, action, permission: social::Permission) if
    action in ["create", "delete"] and
    allow(actor, "update", permission.role);


# Built-in roles
allow(user: social::User, action: String, resource) if
    role = user.role_set.all() and
    allow_role(role, action, resource);

allow_role(role: social::Role{name: "Moderator"}, "delete", _resource: social::Post) if
    role.created_by = None;

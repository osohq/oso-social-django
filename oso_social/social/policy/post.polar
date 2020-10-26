
## POST RESOURCES

# Allow anyone to view any public posts.
allow(_actor, "read", post: social::Post) if
    post.access_level = social::Post.ACCESS_PUBLIC;

# Allow a user to manage their posts.
allow(actor: social::User, _action, post: social::Post) if
    post.created_by = actor;

## ROLE RESOURCES

# Allow a user to manage their roles.
allow(actor: social::User, _action, role: social::Role) if
    role.created_by = actor;

# A user is allowed to delete a permission if they are allowed to update a role
allow(actor: social::User, action, permission: social::Permission) if
    action in ["create", "delete"] and
    allow(actor, "update", permission.role);

# hack around partial eval, specific to "create" when you don't have an actual instance, the Dictionary resource
# is a poor man's Partial object
allow_by_model(user: social::User, action: String, resource: {type: resource_type, owner: resource_owner}) if
    # type checking
    resource_type matches String and
    resource_owner matches social::User and
    action in ["read", "create", "update", "delete"] and

    # logic
    role = user.role_set.all() and
    role.created_by =  resource_owner and
    permission = role.permissions.all() and
    permission.get_resource() = resource_type and
    permission.get_action() = action;

allow(user: social::User, action: String, post: social::Post) if
    allow_by_model(user, action, {type: "post", owner: post.created_by});


# Built-in roles
allow(user: social::User, action: String, resource) if
    role = user.role_set.all() and
    allow_role(role, action, resource);

allow_role(role: social::Role{name: "Moderator"}, "delete", _resource: social::Post) if
    not role.created_by matches social::User;

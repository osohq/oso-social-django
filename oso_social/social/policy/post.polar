## BUILT-IN RULES
allow(user, action, resource) if
    user_in_role(user, role) and
    role_applies_to_resource(role, resource) and
    role_allow(user, role, action, resource);

## Role-based rules

# Get a user's roles
user_in_role(user: social::User, role) if
    role = user.role_set.all();

# Specify that a role applies to a resource
# In this case, a role applies to a Post or Role resource if it is in the same organization as the resource;
# Any role may apply to an HttpRequest resource.
role_applies_to_resource(_role: social::Role{organization: org}, _resource: social::Post{organization: org});
role_applies_to_resource(_role: social::Role{organization: org}, _resource: social::Role{organization: org, custom: true});
role_applies_to_resource(_role, _resource: HttpRequest);

# built-in roles
role_allow(_user: social::User, _role: social::Role{name: "Admin", custom: false}, _action, _resource: social::Post);
role_allow(_user: social::User, _role: social::Role{name: "Admin", custom: false}, _action, _resource: social::Role);
role_allow(_user: social::User, _role: social::Role{name: "Admin", custom: false}, "GET", _resource: HttpRequest{path: "/roles/"});

# custom roles
resource_kind(_resource: social::Role, "role");
resource_kind(_resource: social::Post, "post");
role_allow(_user: social::User, role: social::Role, action: String, resource) if
    role.custom and
    # Get the role's permissions (social::Permission in models.py)
    permission = role.permissions.all() and
    kind = permission.get_resource_kind() and
    resource_kind(resource, kind) and
    permission.get_action() = action;

## ALLOW RULES (attribute-based)

# Allow anyone to view any public posts within their organization.
allow(actor: social::User, "read", post: social::Post) if
    post.access_level = social::Post.ACCESS_PUBLIC and
    actor.organization = post.organization;

# Allow a user to manage their own posts.
allow(actor: social::User, _action, post: social::Post) if
    post.created_by = actor;

# A user is allowed to create/delete a permission if they are allowed to update the role.
allow(actor: social::User, action, permission: social::Permission) if
    action in ["create", "delete"] and
    allow(actor, "update", permission.role);
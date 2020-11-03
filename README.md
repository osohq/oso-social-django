# oso-social-django

This example repo contains a Twitter clone written using [Django](https://docs.djangoproject.com/en/3.1/) and [oso](https://www.osohq.com/).

This example is explained [on the oso blog](https://www.osohq.com/post/django-access-control).

# Running the example

- Clone the repo
- Install dependencies `pip install -r requirements.txt`
- Run `./oso_social/manage.py migrate`
- Run `./oso_social/manage.py runserver`

# Application Overview

- Multi-tenant twitter-like app
  - Tenants are Organizations
  - Resources are Posts
    - Posts can be public or private, and are scoped to organizations
    - Available actions on `Post` are "create", "read", "delete"
  - Built-in `Admin` role
  - The `Admin` can create custom roles to give users within the organization permissions on Posts, and assign them to other users within the organization
  - The `Admin` can take any action on a Post

## Policy

- Role-based rules
  - The policy uses a pattern we've designed for role-based attribute control that consists of 3 types of rules:
    - `user_in_role(user, role)` is used to get all the roles on a user, and can be defined based on the role model you use in your application. In this app, we get the roles off the user model using Django methods.
    - `role_applies_to_resource(role, resource)` is used to specify that a role applies to a resource. In the general case (all roles apply to all resources), use `role_applies_to_resource(_role, _resource);` In this app, we scoped roles to only apply to `Post` and `Role` resources that have the same organization as the role, but let any role apply to `HttpRequest` resources
    - `role_allow(user, role, action, resource)` specifies the actual permissions that a particular role has (e.g. an action-resource pair)
      - We used this to specify he permissions of the built-in `Admin` role, as well as the permissions granted by custom roles.
  - The three rules types above are enforced by the `allow()` rule at the top of the file
- Attribute-based rules
  - There are also some `allow` rules that give access based on the attributes of the Actor or Resource, e.g.
    - Users can take any action on their own posts
    - Anyone can view public posts within their organization
    - Access to `Permission` resources is inherited from access to `Role` resources.

## Enforcement

- All policy checking happens in `views.py`. The sample app exhibits a few different levels of authZ enforcement:
  - Route-level authZ
    - We authorize the `/roles/` route with the `@authorize_request` decorator. This is the only route-level check we care about in the app
    - Note: the `RouteAuthorization` Django middleware can be used to add request authorization to all routes. See more in our docs [here](https://docs.osohq.com/using/frameworks/django.html#requiring-authorization-on-every-request).
  - Record-level authZ is done using two methods:
    - `Oso.is_allowed(actor, action, resource)`: checks the policy for `allow(actor, action, resource)` and returns `True/False`
      - We use this to check access for controlling UI elements, the "delete" buttons and the "Roles" link.
    - `Oso.authorize()`: calls `is_allowed()` with Django defaults, where `actor` defaults to the current user and `action` defaults to the request method
      - Raises a `Forbidden` exception if the authorize check fails
      - We use this to authorize the records being accessed in each route handler, by passing in the record and the action being requested (e.g. "read", "create", "delete")
      - Note: the `RequireAuthorization` middleware can be used to enforce that `authorize()` is being called in each route handler. See more in our docs [here](https://docs.osohq.com/using/frameworks/django.html#requiring-authorization-on-every-request).
  - Frontend authZ checks
    - We provide authZ context to the UI templates by defining `oso_context_processor()` in `views.py` and registering it as a template context processor in `settings.py`.
      - The authZ context provided is whether the user has access to the `/roles/` endpoint, so that we can control whether the link to that page is shown.

## Tracing

- To run the app with tracing, use `export POLAR_LOG=1`

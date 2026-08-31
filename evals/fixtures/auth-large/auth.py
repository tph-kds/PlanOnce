def authorized(user, required_role):
    return required_role in user.roles

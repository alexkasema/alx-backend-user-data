#!/usr/bin/env python3

from api.v1.auth.auth import Auth

a = Auth()

excluded_paths = ["/api/v1/stat*"]
paths = ["/api/v1/users","/api/v1/status","/api/v1/stats"]

for path in paths:
    print(a.require_auth(path, excluded_paths))

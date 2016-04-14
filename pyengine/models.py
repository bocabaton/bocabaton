import uuid
from django.db import models

class user(models.Model):
    user_id = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=255, default='')
    state = models.CharField(max_length=20, default='enable')
    email = models.CharField(max_length=255, default='')
    language = models.CharField(max_length=30)
    timezone = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True, editable=False)

class token(models.Model):
    user = models.ForeignKey('user', to_field='user_id')
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

# Resource > Infrastructure

class region(models.Model):
    name        = models.CharField(max_length=32)
    uuid        = models.UUIDField(default=uuid.uuid4, unique=True)
    created     = models.DateTimeField(auto_now_add=True, editable=False)
    status      = models.CharField(max_length=20, default="enabled")

class zone(models.Model):
    name        = models.CharField(max_length=32)
    uuid        = models.UUIDField(default=uuid.uuid4, unique=True)
    created     = models.DateTimeField(auto_now_add=True, editable=False)
    status      = models.CharField(max_length=20, default="enabled")
    region_uuid = models.UUIDField()

class cluster(models.Model):
    name        = models.CharField(max_length=32)
    uuid        = models.UUIDField(default=uuid.uuid4, unique=True)
    created     = models.DateTimeField(auto_now_add=True, editable=False)
    status      = models.CharField(max_length=20, default="enabled")
    zone_uuid   = models.UUIDField()

class host(models.Model):
    name        = models.CharField(max_length=32)
    uuid        = models.UUIDField(default=uuid.uuid4, unique=True)
    domain      = models.CharField(max_length=64, default='')
    ipv4        = models.GenericIPAddressField(protocol='IPv4')
    user_id     = models.CharField(max_length=20, default='root')
    password    = models.CharField(max_length=128, default='')
    id_rsa      = models.CharField(max_length=2048, default='')
    id_dsa      = models.CharField(max_length=2048, default='')
    created     = models.DateTimeField(auto_now_add=True, editable=False)
    status      = models.CharField(max_length=20, default="unknown")
    cluster_uuid= models.UUIDField()

# Workspace

class workspace(models.Model):
    user_id     = models.CharField(max_length=32)
    name        = models.CharField(max_length=32)
    uuid        = models.UUIDField(default=uuid.uuid4, unique=True)
    created     = models.DateTimeField(auto_now_add=True, editable=False)
    status      = models.CharField(max_length=20, default="enabled")

class ws2user(models.Model):
    workspace_uuid  = models.CharField(max_length=36)
    email           = models.CharField(max_length=255)
    role            = models.CharField(max_length=32, default='owner')

class workflow(models.Model):
    name        = models.CharField(max_length=32)
    uuid        = models.UUIDField(default=uuid.uuid4, unique=True)
    workspace_uuid  = models.CharField(max_length=36)
    created     = models.DateTimeField(auto_now_add=True, editable=False)
    status      = models.CharField(max_length=20, default="enabled")


class bpmn(models.Model):
    uuid        = models.UUIDField(default=uuid.uuid4, unique=True)
    workflow_uuid  = models.CharField(max_length=36)
    created     = models.DateTimeField(auto_now_add=True, editable=False)
    status      = models.CharField(max_length=20, default="enabled")
    config     = models.TextField()
  
class workflow_template(models.Model):
    name        = models.CharField(max_length=32)
    uuid        = models.UUIDField(default=uuid.uuid4, unique=True)
    category    = models.CharField(max_length=32)
    config      = models.TextField()
    created     = models.DateTimeField(auto_now_add=True, editable=False)
    status      = models.CharField(max_length=20, default="enabled")

class task_template(models.Model):
    name        = models.CharField(max_length=32)
    fw_type     = models.CharField(max_length=32)
    uuid        = models.UUIDField(default=uuid.uuid4, unique=True)
    category    = models.CharField(max_length=32)
    config      = models.TextField()
    created     = models.DateTimeField(auto_now_add=True, editable=False)
    status      = models.CharField(max_length=20, default="enabled")


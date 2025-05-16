from django.db import models
import uuid

class EActionType(models.TextChoices):
    ENABLE = 'ENABLE', 'Enable'
    DISABLE = 'DISABLE', 'Disable'
    TOGGLE = 'TOGGLE', 'Toggle'

    def __str__(self):
        return self.name


class EStatus(models.TextChoices):
    ENABLED = 'ENABLED', 'Enabled'
    DISABLED = 'DISABLED', 'Disabled'
    TOGGLED = 'TOGGLED', 'Toggled'

    def __str__(self):
        return self.name


class Project(models.Model):
    """
    Model representing a project.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Environment(models.Model):
    """
    Model representing an environment.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='environments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class FeatureFlag(models.Model):
    """
    Model representing a feature flag.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    key = models.CharField(max_length=255)
    state = models.CharField(max_length=10, choices=EStatus.choices)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='feature_flags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key


class RolloutRule(models.Model):
    """
    Model representing a rollout rule.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    percentage = models.PositiveSmallIntegerField()
    group_name = models.CharField(max_length=255)
    active_from = models.DateTimeField()
    active_until = models.DateTimeField()
    feature_flag = models.ForeignKey(FeatureFlag, on_delete=models.CASCADE, related_name='rollout_rules')

    def __str__(self):
        return f"RolloutRule {self.id} for FeatureFlag {self.feature_flag_id}"


class ToggleLog(models.Model):
    """
    Model representing a toggle log.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    feature_flag = models.ForeignKey(FeatureFlag, on_delete=models.CASCADE, related_name='toggle_logs')
    user_id = models.UUIDField()
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE, related_name='toggle_logs')
    previous_state = models.CharField(max_length=10, choices=EStatus.choices)
    new_state = models.CharField(max_length=10, choices=EStatus.choices)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ToggleLog {self.id} for FeatureFlag {self.feature_flag.key}"


class FlagScheduler(models.Model):
    """
    Model representing a flag scheduler.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    feature_flag = models.ForeignKey(FeatureFlag, on_delete=models.CASCADE, related_name='flag_schedulers')
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE, related_name='flag_schedulers')
    scheduled_time = models.DateTimeField()
    action = models.CharField(max_length=10, choices=EActionType.choices)

    def __str__(self):
        return f"FlagScheduler {self.id} for FeatureFlag {self.feature_flag.key} in Environment {self.environment.name}"
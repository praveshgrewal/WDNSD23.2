from django.db import models
from django.utils import timezone
import os


def profile_image_path(instance, filename):
    """Generate upload path for profile images."""
    ext = filename.split('.')[-1]
    return f'profiles/{instance.employee_id}_{instance.name}.{ext}'


class Employee(models.Model):
    """Model representing a registered employee for face attendance."""
    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100, blank=True, default='')
    profile_image = models.ImageField(
        upload_to=profile_image_path, blank=True, null=True
    )
    is_trained = models.BooleanField(default=False)
    images_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} (ID: {self.employee_id})"

    def get_faces_dir(self):
        """Return the directory path where this employee's face images are stored."""
        from django.conf import settings
        path = os.path.join(settings.MEDIA_ROOT, 'faces', str(self.employee_id))
        os.makedirs(path, exist_ok=True)
        return path


class Attendance(models.Model):
    """Model to record employee check-in and check-out times."""
    STATUS_CHOICES = [
        ('IN', 'Checked In'),
        ('OUT', 'Checked Out'),
    ]

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='attendance_records'
    )
    date = models.DateField(default=timezone.now)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='IN')
    confidence = models.FloatField(default=0.0, help_text='Face match confidence percentage')

    class Meta:
        ordering = ['-date', '-check_in']
        unique_together = ['employee', 'date']

    def __str__(self):
        return f"{self.employee.name} — {self.date} ({self.status})"

    @property
    def duration(self):
        """Calculate working duration if both check-in and check-out exist."""
        if self.check_in and self.check_out:
            delta = self.check_out - self.check_in
            hours, remainder = divmod(delta.seconds, 3600)
            minutes = remainder // 60
            return f"{hours}h {minutes}m"
        return "—"

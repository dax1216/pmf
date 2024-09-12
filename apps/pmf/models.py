import json
from django.db import models

class ProcessStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"

class CriterionWeight:
    def weights(self):
        # criteria weight value over 10
        return {
            "business_fit": 9,
            "customization": 8,
            "ease_of_adoption": 6,
            "cost": 7,
            "integration": 8,
        }

    def max_score(self):
        # max total score for all criteria
        return sum([w * 10 for w in self.weights().values()])


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255)
    pmf_score_details = models.JSONField(null=True, blank=True)
    status = models.CharField(
        max_length=32, choices=ProcessStatus.choices, default=ProcessStatus.PENDING
    )

    def __str__(self):
        return self.name

    @property
    def pmf_score(self):
        if self.pmf_score_details:
            scores = self.pmf_score_details
            total = 0
            for s in scores:
                total += scores[s] * CriterionWeight().weights()[s]

            return round((total / CriterionWeight().max_score()) * 100, 2)

        return 0
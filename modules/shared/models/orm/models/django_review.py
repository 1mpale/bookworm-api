# Copyright 2024 BookWorm Inc. All rights reserved.

"""Django ORM model for reviews."""

from django.db import models

from modules.shared.models.orm.models.django_base_model import DjangoBaseModel


class DjangoReview(DjangoBaseModel):
    """Review database model.

    Stores user reviews for books including rating, content,
    and computed sentiment score.
    """

    book = models.ForeignKey(
        "shared_models.DjangoBook",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    user = models.ForeignKey(
        "shared_models.DjangoUser",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.IntegerField()
    title = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField()
    sentiment_score = models.FloatField(null=True, blank=True)
    sentiment_processed = models.BooleanField(default=False)

    class Meta:
        db_table = "reviews"
        ordering = ["-created_at"]
        unique_together = [("book", "user")]

    def __str__(self) -> str:
        return f"Review by {self.user_id} for {self.book_id}: {self.rating}/5"

    __all__ = ["DjangoReview"]

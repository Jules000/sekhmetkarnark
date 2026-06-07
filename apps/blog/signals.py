from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Article


@receiver(post_save, sender=Article)
@receiver(post_delete, sender=Article)
def invalidate_article_cache(sender, instance, **kwargs):
    cache.delete_pattern("sk:*article*")
    cache.delete_pattern("sk:*article_list*")
    cache.delete_pattern("sk:*homepage*")

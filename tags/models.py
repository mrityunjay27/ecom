from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.


class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        return TaggedItem.objects \
            .select_related('tag') \
            .filter(
                content_type=content_type,
                object_id=obj_id
        )


class Tag(models.Model):
    label = models.CharField(max_length=255)


class TaggedItem(models.Model):
    objects = TaggedItemManager()
    # What tag applied to what object
    # 3 things has to be defined for Generic Relationships
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # TYPE (product, video, article)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # id
    object_id = models.PositiveIntegerField()
    # object
    content_object = GenericForeignKey()  # this will fetch the actual content

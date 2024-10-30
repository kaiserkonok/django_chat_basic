from django.db import models
from django.contrib.auth.models import User

class PrivateChat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1_room')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2_room')

    @classmethod
    def get_or_create_private_chat(cls, user1, user2):
        if cls.objects.filter(user1=user1, user2=user2).exists():
            return cls.objects.get(user1=user1, user2=user2)
        elif cls.objects.filter(user1=user2, user2=user1).exists():
            return cls.objects.get(user1=user2, user2=user1)
        
        return cls.objects.create(user1=user1, user2=user2)

    def __str__(self):
        return f"{self.user1.username} and {self.user2.username}"


class Message(models.Model):
    room = models.ForeignKey(PrivateChat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp', )

    def __str__(self):
        return f"{self.sender.username}: {self.message}"

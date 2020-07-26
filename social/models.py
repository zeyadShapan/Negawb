from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class ChatRequest(models.Model):
    request_sender = models.ForeignKey(
        User, related_name='request_sender', on_delete=models.CASCADE)
    request_receiver = models.ForeignKey(
        User, related_name='request_receiver', on_delete=models.CASCADE)
    sent_date = models.DateTimeField(auto_now_add=True)


class ChatBox(models.Model):
    user_1 = models.ForeignKey(
        User, related_name='user_1', on_delete=models.CASCADE)
    user_2 = models.ForeignKey(
        User, related_name='user_2', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_1} | {self.user_2}'


class Message(models.Model):
    chat_box = models.ForeignKey(
        ChatBox, related_name='chat_box', null=True, on_delete=models.CASCADE)
    message_sender = models.ForeignKey(
        User, related_name='message_sender', null=True, on_delete=models.CASCADE)
    sent_date = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        return f'message_sender: {self.message_sender}, chat_box: {self.chat_box}'


class ChatGroup(models.Model):
    image = models.ImageField(upload_to='group_images',
                            default='static/categories/logo.png')
    members = models.ManyToManyField(User, related_name='group_memebers')
    title = models.CharField(max_length=75)
    is_public = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    group_admins = models.ManyToManyField(User, related_name='gropu_admins')
    created_date = models.DateTimeField(auto_now_add=True)

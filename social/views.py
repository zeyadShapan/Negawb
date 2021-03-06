from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import now
import datetime
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import ChatGroupForm
from .models import ChatBox, Message, ChatGroup, GroupRequest, GroupMessage, Notification, Area
from people.models import FriendRequest
from webpush import send_user_notification
User = get_user_model()


def chat(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            chat_boxes = ChatBox.objects.filter(
                Q(user_1=request.user) | Q(user_2=request.user))
            groups = ChatGroup.objects.filter(members=request.user)
        else:
            chat_boxes = []
            groups = []
        return render(request, 'social/chathome.html', {'chat_boxes': chat_boxes, 'groups': groups})
    else:
        form = ChatGroupForm(data=request.POST, files=request.FILES)
        group = form.save(commit=False)
        group.author = request.user
        group.save()
        group.members.add(request.user)
        group.group_admins.add(request.user)
        return redirect('social:chat_group', pk=group.id)

# Friend


@login_required
def chat_friend(request, pk):
    # Chat info
    friend = get_object_or_404(User, pk=pk)
    chat_box = ChatBox.objects.filter(
        user_1=request.user, user_2=friend).first()
    if not chat_box:
        chat_box = ChatBox.objects.filter(
            user_1=friend, user_2=request.user).first()

    # Read all messages
    for message in Message.objects.filter(Q(is_read=False), ~Q(message_sender=request.user)):
        message.is_read = True
        message.save()
    for notification in Notification.objects.filter(sender=friend, url=f"/social/chat_friend/{friend.id}"):
        notification.delete()

    chat_messages_list = Message.objects.filter(
        chat_box=chat_box).order_by('date')
    # chat messages Paginator
    paginator = Paginator(chat_messages_list, 7)
    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    else:
        page = 0
    page = paginator.num_pages - page

    try:
        chat_messages = paginator.page(page)
    except EmptyPage:
        chat_messages = []
    except PageNotAnInteger:
        chat_messages = paginator.page(paginator.num_pages)

    if request.method == 'GET' and not request.GET.get('action') and not request.GET.get('page'):
        return render(request, 'social/chat_friend.html', {'friend': friend, 'chat_messages': chat_messages, })
    # Paginate messages
    elif request.GET.get('page'):
        return JsonResponse({'chat_messages': serialize('json', chat_messages)})
    # Load new messages
    elif request.GET.get('action') == 'load_new_messages':
        last_message_id = int(request.GET.get('last_message_id'))
        chat_messages = Message.objects.filter(
            chat_box=chat_box, id__gt=last_message_id).order_by('date')
        return JsonResponse({'chat_messages': serialize('json', chat_messages)})


def send_friend_message(request, pk):
    friend = get_object_or_404(User, pk=pk)
    chat_box = ChatBox.objects.filter(
        user_1=request.user, user_2=friend).first()
    if not chat_box:
        chat_box = ChatBox.objects.filter(
            user_1=friend, user_2=request.user).first()
    message = Message(chat_box=chat_box, message_sender=request.user,
                      message=request.GET.get('message'))
    # friend notification
    if friend.allow_friends_notifications:
        # !ABSOLUTE PATH
        notification = Notification.objects.create(
            type='friend_message', sender=request.user, url=f'/social/chat_friend/{request.user.id}', content=f'a message from {request.user.username}: {message.message[:100]}')
        notification.save()
        notification.receiver.add(friend)
        for receiver in notification.receiver.all():
            if notification.sender.who_see_avatar == 'everyone':
                sender_avatar = notification.sender.avatar.url
            elif notification.sender.who_see_avatar == 'friends' and receiver in receiver.friends.all():
                sender_avatar = notification.sender.avatar.url
            else:
                sender_avatar = '/media/profile_images/DefaultUserImage.jpg'
            payload = {"head": f"Message from {notification.sender}",
                        "body": notification.content,
                        "url": notification.url,
                        "icon": sender_avatar,
                        }
            send_user_notification(
                user=receiver, payload=payload, ttl=1000)
    # End normal friend notification
    message.save()
    return JsonResponse({})


def send_friend_file_message(request, pk):
    friend = get_object_or_404(User, pk=pk)
    chat_box = ChatBox.objects.filter(
        user_1=request.user, user_2=friend).first()
    if not chat_box:
        chat_box = ChatBox.objects.filter(
            user_1=friend, user_2=request.user).first()

    message = Message(chat_box=chat_box, message_sender=request.user,
                      file=request.FILES.get('file'), image=request.FILES.get('image'), video=request.FILES.get('video'), audio=request.FILES.get('audio'))
    message.save()
    return redirect('social:chat_friend', pk=pk)


def send_friend_voice_message(request, pk):
    friend = get_object_or_404(User, pk=pk)
    chat_box = ChatBox.objects.filter(
        user_1=request.user, user_2=friend).first()
    if not chat_box:
        chat_box = ChatBox.objects.filter(
            user_1=friend, user_2=request.user).first()
    message = Message(
        chat_box=chat_box, message_sender=request.user, audio=request.FILES.get('audio'))
    message.save()
    return JsonResponse({})


# End friend

# Groups


def chat_group(request, pk):
    group = get_object_or_404(ChatGroup, pk=pk)

    if not request.user in group.members.all():
        messages.error(request, 'You are not in this group')
        return redirect('chat')

    chat_messages_list = GroupMessage.objects.filter(group=group)
    areas = Area.objects.filter(group=group)
    # chat messages Paginator
    paginator = Paginator(chat_messages_list, 7)
    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    else:
        page = 0
    page = paginator.num_pages - page

    try:
        chat_messages = paginator.page(page)
    except EmptyPage:
        chat_messages = []
    except PageNotAnInteger:
        chat_messages = paginator.page(paginator.num_pages)

    # form
    form = ChatGroupForm(instance=group)
    if request.method == 'GET' and not request.GET.get('action') and not request.GET.get('page'):
        return render(request, 'social/chat_group.html', {'group': group, 'chat_messages': chat_messages, 'form': form, 'areas': areas})

    # Paginate messages
    elif request.GET.get('page'):
        return JsonResponse({'chat_messages': serialize('json', chat_messages)})

    # Load new messaages
    elif request.GET.get('action') == 'load_new_messages':
        last_message_id = int(request.GET.get('last_message_id'))
        chat_messages = GroupMessage.objects.filter(
            group=group, id__gt=last_message_id).order_by('date')
        return JsonResponse({'chat_messages': serialize('json', chat_messages)})


def edit_group(request, pk):
    group = get_object_or_404(ChatGroup, pk=pk)
    form = ChatGroupForm(
        instance=group, data=request.POST, files=request.FILES)
    if request.user == group.author or request.user in group.group_admins.all():
        form.save()
    else:
        messages.error(request, 'Only group admins can edit')
    return redirect('social:chat_group', pk=pk)


def send_group_message(request, pk):
    group = get_object_or_404(ChatGroup, pk=pk)
    try:
        area = get_object_or_404(Area, pk=request.GET.get('area'))
    except:
        area = None
    message = GroupMessage(
        group=group, message_sender=request.user, message=request.GET.get('message'), area=area)
    # group notification
    receivers = [member for member in group.members.filter(
        Q(allow_groups_notifications=True), ~Q(id=request.user.id))]
    notification = Notification(type='group_message', sender=request.user, url=f'/social/chat_group/{group.id}/', content=message.message[:100])
    if receivers:
        notification.save()
        for receiver in receivers:
            if not area or not receiver in area.muted_users.all():
                notification.receiver.add(receiver)
        for receiver in notification.receiver.all():
            payload = {"head": f"A message from {group.title} Group, {notification.sender}",
                        "body": notification.content,
                        "url": notification.url,
                        "icon": group.image.url,
                        }
            send_user_notification(
                user=receiver, payload=payload, ttl=1000)

    message.save()
    return JsonResponse({})


def send_group_file_message(request, pk):
    group = get_object_or_404(ChatGroup, pk=pk)
    try:
        area = get_object_or_404(Area, pk=request.GET.get('area'))
    except:
        area = None
    message = GroupMessage(
        group=group, message_sender=request.user, file=request.FILES.get('file'), image=request.FILES.get('image'), video=request.FILES.get('video'), audio=request.FILES.get('audio'), area=area)
    message.save()
    return redirect('social:chat_group', pk=pk)


def send_group_voice_message(request, pk):
    group = get_object_or_404(ChatGroup, pk=pk)
    print(request.POST.get('area'))
    try:
        area = get_object_or_404(Area, pk=int(request.POST.get('area')))
    except:
        area = None
    message = GroupMessage(
        group=group, message_sender=request.user, audio=request.FILES.get('audio'), area=area)
    message.save()
    return JsonResponse({})


def send_group_invite(request, user_pk, group_pk):
    request_sender = request.user
    reciever = get_object_or_404(User, pk=user_pk)
    group = get_object_or_404(ChatGroup, pk=group_pk)
    if request_sender == reciever:
        message = {
            'text': f'You can\'t invite yourself',
            'tags': 'error',
        }
        return JsonResponse({'message': message})

    group_request = GroupRequest(
        request_sender=request_sender, reciever=reciever, group=group)
    group_request_check = GroupRequest.objects.filter(
        request_sender=request_sender, reciever=reciever)
    if group_request_check:
        message = {
            'text': f'You already send a group request to {reciever}',
            'tags': 'warning',
        }
        return JsonResponse({'message': message})
    elif reciever.who_add_group == 'none' or (reciever.who_add_group == 'friends' and not request_sender in reciever.friends.all()):
        message = {
            'text': f'You can\'t add {reciever.username} because he/she disables that feature',
            'tags': 'warning',
        }
        return JsonResponse({'message': message})
    else:
        group_request.save()
        # !ABSOLUTE PATH
        if reciever.allow_invites:
            notification = Notification(type='invites', sender=request.user,
                                        url='/user/requests/', content=f'{request.user.username} invited you to join {group.title}')
            notification.save()
            notification.receiver.add(reciever)
            for receiver in notification.receiver.all():
                if notification.sender.who_see_avatar == 'everyone':
                    sender_avatar = notification.sender.avatar.url
                elif notification.sender.who_see_avatar == 'friends' and receiver in receiver.friends.all():
                    sender_avatar = notification.sender.avatar.url
                else:
                    sender_avatar = '/media/profile_images/DefaultUserImage.jpg'
                payload = {"head": f"{notification.sender.username} invited you to join {group.title}",
                           "body": notification.content,
                           "url": notification.url,
                           "icon": sender_avatar,
                           }
                send_user_notification(
                    user=receiver, payload=payload, ttl=1000)
        message = {
            'text': f'Successfully invited {reciever}',
            'tags': 'success',
        }
        return JsonResponse({'message': message})


def join_group(request):
    pk = request.GET.get('pk')
    group_request = get_object_or_404(GroupRequest, pk=pk)
    group = group_request.group
    group.members.add(request.user)
    group_request.delete()
    if group_request.request_sender.your_invites:
        notification = Notification(type='your_invites', sender=request.user,
                                    url=f'/social/chat_group/{group.id}/', content=f'{request.user} joined {group.title}')
        notification.save()
        notification.receiver.add(group_request.request_sender)
    message = {
        'text': f'Welome to {group.title}',
        'tags': 'success',
    }
    return JsonResponse({'message': message})


def deny_group(request):
    pk = request.GET.get('pk')
    group_request = get_object_or_404(GroupRequest, pk=pk)
    group_request.delete()
    if group_request.request_sender.your_invites:
        notification = Notification(type='your_invites', sender=request.user,
                                    url=f'/people/{request.user.id}/', content=f'{request.user} Denied your invite to join {group_request.group.title}')
        notification.save()
        notification.receiver.add(group_request.request_sender)
    message = {
        'text': f'You didn\'t join {group_request.group.title}',
        'tags': 'success'
    }
    return JsonResponse({'message': message, })


def kick_member(request, group_pk, member_pk):
    member = get_object_or_404(User, pk=member_pk)
    group = get_object_or_404(ChatGroup, pk=group_pk)
    if request.user == group.author or (request.user in group.group_admins.all() and not member == group.author):
        group.members.remove(member)
    return JsonResponse({})


def hire_member(request, group_pk, member_pk):
    member = get_object_or_404(User, pk=member_pk)
    group = get_object_or_404(ChatGroup, pk=group_pk)
    if (request.user == group.author or request.user in group.group_admins.all()) and (member not in group.group_admins.all()):
        group.group_admins.add(member)
        return JsonResponse({})


def lower_member(request, group_pk, member_pk):
    member = get_object_or_404(User, pk=member_pk)
    group = get_object_or_404(ChatGroup, pk=group_pk)
    if request.user == group.author and not member == request.user:
        group.group_admins.remove(member)
        return JsonResponse({})


@login_required
def delete_group(request, pk):
    group = get_object_or_404(ChatGroup, pk=pk)
    if request.user == group.author:
        group.delete()
        return redirect('chat')
    else:
        messages.error(request, 'Only the group owner can delete the group')
        return redirect('social:chat_group', pk=pk)


def leave_group(request, pk):
    group = get_object_or_404(ChatGroup, pk=pk)
    group.members.remove(request.user)
    message = GroupMessage(
        group=group, message_sender=request.user, message=f'{request.user} left the group')
    message.save()
    if group.members.all().count() <= 0:
        group.delete()
    else:
        if request.user == group.author:
            try:
                group.author = group.group_admins.all()[1]
                group.save()
            except:
                group.author = group.members.all().first()
                group.save()
        if request.user in group.group_admins.all():
            group.group_admins.remove(request.user)
    return redirect('chat')

# End groups

# Notifications


def click_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    notification.is_read = True
    notification.save()
    return redirect(notification.url)


def read_all_notifications(request):
    notifications = Notification.objects.filter(
        receiver=request.user, is_read=False)
    for notification in notifications:
        notification.is_read = True
        notification.save()
    messages.success(request, 'Read all ✅')
    return redirect('home')


def delete_all_notifications(request):
    notifications = Notification.objects.filter(receiver=request.user)
    for notification in notifications:
        notification.delete()
    messages.success(request, 'Deleted all ✅')
    return redirect('home')

# End notifications


def take_down_friend_request(request, pk):
    friend_request = get_object_or_404(FriendRequest, pk=pk)
    friend_request.delete()
    return JsonResponse({})

# Area


def create_area(request, pk):
    group = get_object_or_404(ChatGroup, pk=pk)
    if request.user == group.author or request.user in group.group_admins.all():
        area = Area(name=request.GET.get('name'), group=group, )
        area.save()
        return JsonResponse({})


def delete_area(request, pk):
    area = get_object_or_404(Area, pk=pk)
    group = area.group
    if request.user == group.author or request.user in group.group_admins.all():
        area.delete()
    return JsonResponse({})


def load_area(request, group_pk, area_pk):
    group = get_object_or_404(ChatGroup, pk=group_pk)
    area = get_object_or_404(Area, pk=area_pk)
    if not request.user in group.members.all():
        messages.error(request, 'You are not in this group')
        return redirect('chat')

    chat_messages_list = GroupMessage.objects.filter(group=group, area=area)
    areas = Area.objects.filter(group=group)
    # chat messages Paginator
    paginator = Paginator(chat_messages_list, 7)
    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    else:
        page = 0
    page = paginator.num_pages - page

    try:
        chat_messages = paginator.page(page)
    except EmptyPage:
        chat_messages = []
    except PageNotAnInteger:
        chat_messages = paginator.page(paginator.num_pages)

    # form
    form = ChatGroupForm(instance=group)
    if request.method == 'GET' and not request.GET.get('action') and not request.GET.get('page'):
        return render(request, 'social/load_area.html', {'group': group, 'chat_messages': chat_messages, 'form': form, 'areas': areas, 'curr_area': area, })

    elif request.GET.get('action') == 'load_new_messages':
        last_message_id = int(request.GET.get('last_message_id'))
        chat_messages = GroupMessage.objects.filter(
            group=group, id__gt=last_message_id, area=area).order_by('date')
        return JsonResponse({'chat_messages': serialize('json', chat_messages)})

    # Paginate messages
    elif request.GET.get('page'):
        return JsonResponse({'chat_messages': serialize('json', chat_messages)})


def mute_area(request, pk):
    area = get_object_or_404(Area, pk=pk)
    if request.user in area.muted_users.all():
        area.muted_users.remove(request.user)
    else:
        area.muted_users.add(request.user)
    return redirect('social:chat_group', pk=area.group.id)
# End area

# Otehr users


def search_users(request):
    q = request.GET.get('q')
    # Todo add phone
    results = User.objects.filter(
        (Q(username__icontains=q) | Q(email__icontains=q)), ~Q(id=request.user.id))
    serialized_results = []
    for result in results:
        if result.who_see_avatar == 'everyone' or result == request.user:
            result_avatar = result.avatar.url
        elif result.who_see_avatar == 'friends' and request.user in result.friends.all():
            result_avatar = result.avatar.url
        else:
            result_avatar = '/media/profile_images/DefaultUserImage.jpg'
        invite = True
        if result.who_add_group == 'none' or (result.who_add_group == 'friends' and not request.user in result.friends.all()):
            invite = False
        serialized_results.append({
            'id': result.id,
            'username': result.username,
            'bio': result.bio,
            'avatar': result_avatar,
            'email': result.email,
            # 'phone': result.phone,
            'is_allowed_group_invite': invite,
        })

    return JsonResponse({'results': serialized_results})

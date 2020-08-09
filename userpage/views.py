from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from comments.models import Post, Comment
from people.models import FriendRequest
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model as user_model
from .forms import UserForm, UserPrivacyForm, UserPasswordForm, DistractionFreeForm
from social.models import GroupRequest
User = user_model()


@login_required
def home(request):
    user = request.user
    form = UserForm(instance=request.user)
    privacy_form = UserPrivacyForm(instance=request.user)
    distraction_free_form = DistractionFreeForm(instance = request.user)
    if request.method == 'GET':
        return render(request, 'userpage/index.html', {'user': user, 'form': form, 'privacy_form': privacy_form, 'distraction_free_form':distraction_free_form})
    elif request.POST['submit'] == 'Update':
        try:
            if request.POST['email']:
                validate_email(request.POST['email'])
            form = UserForm(data=request.POST,
                            files=request.FILES, instance=request.user)
            form.save()
            messages.success(request, 'Updated successfully')
            return redirect('userpage:home')
        except ValidationError:
            messages.error(request, 'Invalid email address')
            return redirect('userpage:home')
        except:
            messages.error(
                request, 'unknown error occured, please try again and report a feedback so we can fix this error')
            return redirect('userpage:home')
    elif request.POST['submit'] == 'Update Privacy':
        form = UserPrivacyForm(
            data=request.POST, files=request.FILES, instance=request.user)
        form.save()
        messages.success(request, 'Successfully updated privacy settings')
        return redirect('userpage:home')
    elif request.POST['submit'] == 'Update Password':
        user = authenticate(
            request, username=request.user.username, password=request.POST['password'])
        if user:
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = UserPasswordForm(
                        request.POST, instance=request.user)
                    user.save()
                    user.set_password(request.POST['password1'])
                    messages.success(request, 'Successfully changed password')
                except:
                    messages.error(
                        request, 'Unknown error occured, please try again and report a feedback so we can fix this error')
            else:
                messages.error(request, 'Passwords didn\'t match')
        else:
            messages.error(request, 'Username and Old password didn\'t match')

        return redirect('userpage:home')
    elif request.POST['submit'] == 'DFree':
        form = DistractionFreeForm(request.POST, instance = request.user)
        form.save()
        messages.success(request, 'DistractionFreeMedia 💪🏻')
        return redirect('userpage:home')


@login_required
def posts(request):
    posts = Post.objects.filter(user=request.user).order_by('-post_date')
    return render(request, 'userpage/posts.html', {'posts': posts})


@login_required
def friends(request):
    if request.method == 'GET':
        friends = User.objects.filter(friends=request.user)
        return render(request, 'userpage/friends.html', {'friends': friends})


@login_required
def friendrequests(request):
    requests = FriendRequest.objects.filter(to_user=request.user)
    group_requests = GroupRequest.objects.filter(reciever=request.user)
    user_friends = User.objects.filter(friends = request.user)
    if request.method == 'GET':
        return render(request, 'userpage/friendrequest.html', {'requests': requests, 'group_requests': group_requests, 'user_friends': user_friends})


@login_required
def denyrequest(request, request_id):
    denied_request = get_object_or_404(FriendRequest, pk=request_id)
    denied_request.delete()
    message = {
        'text': f'Friend Request denied',
        'tags': 'success'
    }
    return JsonResponse({'message': message})


@login_required
def requestssent(request):
    requests = FriendRequest.objects.filter(from_user=request.user)
    return render(request, 'userpage/requestssent.html', {'requests': requests})


@login_required
def acceptrequest(request, request_id):
    friend_request = get_object_or_404(FriendRequest, pk=request_id)
    from_user = request.user
    to_user = friend_request.from_user

    from_user.friends.add(to_user)
    to_user.friends.add(from_user)
    friend_request.delete()
    messages.success(request, f'{to_user} is now a friend')
    message = {
        'text': f'{to_user} is now a friend 😄',
        'tags': 'success'
    }
    return JsonResponse({'message': message})


@login_required
def friendsresult(request):
    query = request.GET.get('q')
    results = User.objects.filter(
        Q(username__icontains=query), friends=request.user)
    return render(request, 'userpage/friendsresult.html', {'results': results})


@login_required
def unfriend(request, pk):
    friend = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user = request.user
        user.friends.remove(friend)
        friend.friends.remove(user)
        messages.success(request, f'{friend.username} is no longer a friend')
        return redirect('userpage:friends')

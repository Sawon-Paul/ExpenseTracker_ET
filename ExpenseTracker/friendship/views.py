from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FriendRequest, Friendship
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def friends_page(request):
    user = request.user

    # Get all friendships involving the user
    my_friends_qs = Friendship.objects.filter(user1=user) | Friendship.objects.filter(user2=user)
    my_friends = [f.user2 if f.user1 == user else f.user1 for f in my_friends_qs]

    friend_requests = FriendRequest.objects.filter(to_user=user, is_active=True, is_rejected=False)

    friend_ids = [f.id for f in my_friends]
    sent_request_ids = FriendRequest.objects.filter(from_user=user, is_active=True).values_list('to_user_id', flat=True)
    received_request_ids = FriendRequest.objects.filter(to_user=user, is_active=True).values_list('from_user_id', flat=True)

    exclude_ids = set(friend_ids) | set(sent_request_ids) | set(received_request_ids) | {user.id}
    suggestions = User.objects.exclude(id__in=exclude_ids)

    return render(request, 'friends/friends.html', {
        'my_friends': my_friends,
        'friend_requests': friend_requests,
        'suggestions': suggestions,
    })

@login_required
def send_friend_request(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    existing_request = FriendRequest.objects.filter(from_user=request.user, to_user=receiver, is_active=True, is_rejected=False).first()

    if not existing_request:
        FriendRequest.objects.create(from_user=request.user, to_user=receiver)
        messages.success(request, 'Friend request sent!')
    else:
        messages.warning(request, 'Friend request already sent.')

    return redirect('friends_page')

@login_required
def confirm_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    friend_request.is_active = False
    friend_request.save()

    user1, user2 = sorted([friend_request.from_user, friend_request.to_user], key=lambda u: u.id)
    if not Friendship.objects.filter(user1=user1, user2=user2).exists():
        Friendship.objects.create(user1=user1, user2=user2)

    messages.success(request, 'Friend request accepted!')
    return redirect('friends_page')

@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    friend_request.is_active = False
    friend_request.is_rejected = True
    friend_request.delete()

    messages.info(request, 'Friend request rejected and removed.')
    return redirect('friends_page')

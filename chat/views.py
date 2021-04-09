from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from .models import User, Message
from django.db.models import Q

import json


@ login_required
def chatroom(request, pk):
    other_user = get_object_or_404(User, pk=pk)
    messages = Message.objects.filter(
        Q(reciver=other_user, sender=request.user) | Q(reciver=request.user, sender=request.user)
    )
    messages.update(seen=True)
    return render(request, 'chatroom.html', {'other_user':other_user, 'messages':messages})


@ login_required
def ajax_load_messages(request, pk):
    other_user = get_object_or_404(User, pk=pk)
    messages = Message.objects.filter(seen=False)
    messages.update(seen=True)
    message_list = [{
        'sender': message.sender.username,
        'message': message.message,
        'sent': message.sender == request.user
        } for message in messages]
    if request.method == 'POST':
        message = json.loads(request.body)
        m = Message.objects.create(reciver=other_user, sender=request.user, message=message)
        message_list.append({
            'sender': request.user.username,
            'message': m.message,
            'sent':True,
        })
    return JsonResponse(message_list, safe=False)
from ..models import Message,User_Room,Room
def message_filter(request,username,room,messages_list):
  room
  if Room.objects.filter(name__icontains=username):
        for rooms in Room.objects.filter(name__icontains=username):
            if rooms.name==username+"-"+request.user.username or rooms.name==request.user.username+"-"+username:
                if User_Room.objects.get(user=request.user,room=rooms):      
                    room=User_Room.objects.filter(user=request.user,room=rooms)
    

  print('room',room)

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import TaskSerializer,UserSerializer
from api.models import Tasks
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions

class TasksView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Tasks.objects.all()
        serializer=TaskSerializer(qs,many=True)            
        return Response(data=serializer.data)

    def post(self,request,*args,**kwargs):
        serializer=TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class TaskDetailView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Tasks.objects.get(id=id)
        serializer=TaskSerializer(qs,many=False)
        return Response(data=serializer.data)

    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Tasks.objects.get(id=id)
        serializer=TaskSerializer(data=request.data,instance=qs)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Tasks.objects.get(id=id).delete()
        return Response(data="deleted")

class ViewsetView(ViewSet):
    def list(self,request,*args,**kwargs):
        qs=Tasks.objects.all()
        serializer=TaskSerializer(qs,many=True)            
        return Response(data=serializer.data)
        
    def create(self,request,*args,**kwargs): 
        serializer=TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Tasks.objects.get(id=id)
        serializer=TaskSerializer(qs,many=False)
        return Response(data=serializer.data)

    def update(self,request,*args,**kwargs): 
        id=kwargs.get("id")
        qs=Tasks.objects.get(id=id)
        serializer=TaskSerializer(data=request.data,instance=qs)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Tasks.objects.get(id=id).delete()
        return Response(data="deleted")



class TaskModelViewsetView(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    # def create(self, request, *args, **kwargs):
    #     serializer=TaskSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(user=request.user)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)

    serializer_class=TaskSerializer
    queryset=Tasks.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def list(self,request,*args,**kwargs):
        qs=Tasks.objects.filter(User=request.user)
        serializer=TaskSerializer(qs,many=True)
        return Response(data=serializer.data)

    @action(methods=["GET"],detail=False)
    def finished_tasks(self,request,*args,**kwargs):
        qs=Tasks.objects.filter(status=True)
        serializer=TaskSerializer(qs,many=True)
        return Response(data=serializer.data)
    @action(methods=["GET"],detail=False)
    def pending_tasks(self,request,*args,**kwargs):
        qs=Tasks.objects.filter(status=False)
        serializer=TaskSerializer(qs,many=True)
        return Response(data=serializer.data)


    # native to queryset serialization
    
    @action(methods=["POST"],detail=True)
    def markas_done(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Tasks.objects.filter(id=id).update(status=True)
        
        return Response(data="status updated")


class UsersView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()

        
    def create(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid(): 
            usr=User.objects.create_user(**serializer.validated_data)
            serializer=UserSerializer(usr,many=False)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors) 







   
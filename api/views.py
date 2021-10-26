from django.db.models.fields import BooleanField
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import models
from . import serializers

# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/notes/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of notes'
        },
        {
            'Endpoint': '/notes/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single note object'
        },
        {
            'Endpoint': '/notes/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes and exiting note'
        },
    ]
    return Response(routes)

@api_view(['GET', "POST"])
def getNotes(request):
    
    if request.method == "GET":        
        notes = models.Note.objects.all().order_by('-updated')
        serializer = serializers.NoteSerializer(notes, many=True)
        
        return Response(serializer.data)

    if request.method == "POST":
        return createNote(request)

@api_view(['GET', 'DELETE', 'PUT'])
def getNote(request, pk):

    if request.method == "GET":
        note = models.Note.objects.get(id=pk)
        serializer = serializers.NoteSerializer(note, many=False)
        
        return Response(serializer.data)

    if request.method == "DELETE":
        return deleteNote(request, pk)

    if request.method == "PUT":
        return updateNote(request, pk)

def createNote(request):
    data = request.data
    note = models.Note.objects.create(
        body=data['body'] 
    )
    serializer = serializers.NoteSerializer(note, many=False)
    return Response(serializer.data)

def updateNote(request, pk):
    data = request.data
    note = models.Note.objects.get(id=pk)
    serializer = serializers.NoteSerializer(instance = note, data = data)

    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)

def deleteNote(request, pk):
    note = models.Note.objects.get(id=pk)
    note.delete()
    return Response('Note Deleted')
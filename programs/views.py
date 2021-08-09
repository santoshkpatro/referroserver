import uuid
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from .models import Program
from .serializers import ProgramSerializer


class ProgramList(generics.ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        programs = self.queryset.filter(owner=self.request.user)
        return programs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProgramSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return super().perform_create(serializer)


class ProgramDetail(APIView):
    permission_classes = (IsAuthenticated, IsOwner)

    def get_object(self, program_id):
        try:
            program = Program.objects.get(id=program_id)
            self.check_object_permissions(self.request, program)
            return program
        except Program.DoesNotExist:
            return Response({'detail': 'Program not found!'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, program_id, format=None):
        program = self.get_object(program_id)
        serializer = ProgramSerializer(program)
        return Response(serializer.data)

    def put(self, request, program_id, format=None):
        program = self.get_object(program_id)
        serializer = ProgramSerializer(program, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(('GET',))
def access_token(request, program_id):
    try:
        program = Program.objects.get(id=program_id)
        if request.user != program.owner:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'detail': 'You are not authorized'})
        program.access_token = uuid.uuid4()
        program.save()
        return Response(status=status.HTTP_201_CREATED, data={'access_token': str(program.access_token)})
    except Program.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'Program not found'})

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics

from django.contrib.auth.models import User
from snippets.serializers import UserSerializer
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework import permissions

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework import renderers
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import detail_route
import django_filters.rest_framework
from rest_framework.filters import OrderingFilter

@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		'snippets': reverse('snippet-list', request=request, format=format)
	})

class UserViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	This viewset automatically provides `list` and `detail` actions.
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer
	filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, OrderingFilter,)
    #filter_fields = ('title', 'code')
    #ordering_fields = ('id', 'title', 'code')
    filter_fields = '__all__'
    ordering_fields = '__all__'
    ordering = ('-code',)

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


#class SnippetHighlight(generics.GenericAPIView):
#    queryset = Snippet.objects.all()
#    renderer_classes = (renderers.StaticHTMLRenderer,)
#
#    def get(self, request, *args, **kwargs):
#        snippet = self.get_object()
#        return Response(snippet.highlighted)
#
#
#class SnippetList(generics.ListCreateAPIView):
#    queryset = Snippet.objects.all()
#    serializer_class = SnippetSerializer
#    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
#
#    def perform_create(self, serializer):
#        serializer.save(owner=self.request.user)
#
#
#class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#    queryset = Snippet.objects.all()
#    serializer_class = SnippetSerializer
#    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)




#class UserList(generics.ListAPIView):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer


#class UserDetail(generics.RetrieveAPIView):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer




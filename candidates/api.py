from django.db.models import Q, IntegerField, When, Count, Case, Sum, Value
from rest_framework import viewsets, status
from rest_framework.response import Response
from candidates.models import Candidate
from candidates.serializers import CandidateSerializer

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Candidate deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    from django.db.models import Q, IntegerField, When, Case, Sum, Value

    def get_queryset(self):
        queryset = Candidate.objects.all()
        search_query = self.request.query_params.get('search', None)

        if search_query:
            search_words = search_query.split()

            query = Q()
            for word in search_words:
                query |= Q(name__icontains=word)

            queryset = queryset.filter(query).distinct()

            queryset = queryset.annotate(
                match_count=Sum(
                    Case(
                        *[When(name__icontains=word, then=1) for word in search_words],
                        default=Value(0),
                        output_field=IntegerField()
                    )
                )
            )
            queryset = queryset.order_by('-match_count')

        return queryset

from django.contrib.gis.geos import Polygon

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from .models import Peak
from .serializers import PeakSerializer
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas



@api_view(['GET', 'POST', 'DELETE'])
def peak_list(request):
# GET list of peaks, POST a new peak, DELETE all peaks
    if request.method == 'GET':
        peaks = Peak.objects.all()
        # get data from request
        name = request.GET.get('name', None)
        # find by name
        if name is not None:
            peaks = peaks.filter(name__icontains=name)
        peak_serializer = PeakSerializer(peaks, many=True)
        return Response(peak_serializer.data)
    elif request.method == 'POST':
        peak_data = JSONParser().parse(request)
        peak_serializer = PeakSerializer(data=peak_data)
        if peak_serializer.is_valid():
            peak_serializer.save()
            return Response(peak_serializer.data, status=status.HTTP_201_CREATED)
        return Response(peak_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = Peak.objects.all().delete()
        return Response({'message': '{} Peaks were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def peak_detail(request, pk):
    # find peak by pk (id)
    try:
        peak = Peak.objects.get(pk=pk)
    except Peak.DoesNotExist:
        return Response({'message': 'The peak does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        peak_serializer = PeakSerializer(peak)
        return Response(peak_serializer.data)
    elif request.method == 'PUT':
        peak_data = JSONParser().parse(request)
        peak_serializer = PeakSerializer(Peak, data=peak_data)
        if peak_serializer.is_valid():
            peak_serializer.save()
            return Response(peak_serializer.data)
        return Response(peak_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        peak.delete()
        return Response({'message': 'Peak was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def peaks_by_bbox(request, xmin, ymin, xmax, ymax):
    bbox = (float(xmin), float(ymin), float(xmax), float(ymax))
    geom = Polygon.from_bbox(bbox)
    try:
        peaks = Peak.objects.filter(location__contained=geom)
    except Peak.DoesNotExist:
        return Response({'message': f'No peak in this bbox {geom} '}, status=status.HTTP_404_NOT_FOUND)
    peaks_serializer = PeakSerializer(peaks, many=True)
    return Response(peaks_serializer.data)

@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Mountain peaks')
    return response.Response(generator.get_schema(request=request))



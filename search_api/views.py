import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult

from .task import perform_search_task

class SearchAPIView(APIView):
    def post(self, request):
        try:

            keywords_list = request.data.get('keywords', [])
            url = request.data.get('url', '')
            
            if not keywords_list or not url:
                return Response({'error': 'Both keywords and URL are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
            task_result = perform_search_task.delay(url, keywords_list)
            return Response({'task_id': task_result.id, 'status': 'Task initiated.'})
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class TaskStatusAPIView(APIView):
    def get(self, request, task_id):
        try:

            result = AsyncResult(task_id)

            if result.successful():
                response_data = {'status': 'Task completed'}
               
                if result.result is not None:
                   response_data['result'] = json.loads(json.dumps(result.result))
                else:
                    response_data['result'] = 'No result produced by the task'

                return Response(response_data)
            
            elif result.failed():

                return Response({'status': 'Task failed', 'error': str(result.result)})
            else:
                return Response({'status': 'Working on it'})

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
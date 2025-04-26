from django.shortcuts import render, redirect
from django.views import View
from .forms import TextDocumentForm
from .utils import calculate_tf_idf

class UploadView(View):
    def get(self, request):
        form = TextDocumentForm()
        return render(request, 'text_analyzer/upload.html', {'form': form})
    
    def post(self, request):
        form = TextDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            
            file_content = document.file.read().decode('utf-8', errors='ignore')
            tf_idf_data = calculate_tf_idf(file_content)
            request.session['tf_idf_data'] = tf_idf_data
            
            return redirect('results')
        
        return render(request, 'text_analyzer/upload.html', {'form': form})

class ResultsView(View):
    def get(self, request):
        tf_idf_data = request.session.get('tf_idf_data', [])
        
        sort_by = request.GET.get('sort_by', request.session.get('sort_by', 'idf'))
        sort_order = request.GET.get('sort_order', request.session.get('sort_order', 'desc'))
        
        request.session['sort_by'] = sort_by
        request.session['sort_order'] = sort_order
        
        reverse_sort = sort_order == 'desc'
        sorted_data = sorted(tf_idf_data, key=lambda x: x[sort_by], reverse=reverse_sort)
        
        top_50 = sorted_data[:50]
        bottom_50 = sorted_data[-50:] if len(sorted_data) > 50 else []
        
        display_data = top_50 if sort_order == 'desc' else bottom_50
        
        return render(request, 'text_analyzer/results.html', {
            'tf_idf_data': display_data,
            'sort_by': sort_by,
            'sort_order': sort_order
        })
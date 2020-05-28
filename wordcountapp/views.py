from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from .forms import FileUploadForm
from .models import FileUpload

from .mrwordcount import MRWordCount

# Create your views here.

def home_view(request, *args, **kwargs):
	app_context = {
		"app_name": "Django Word Count on AWS",
		"app_created_by": "Mustafa Görkem Uysal",
		"app_number": 151805026
	}
	return render(request, "home.html", app_context)

def upload_view(request):
	if request.method == 'POST':
		form = FileUploadForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			request.session['redirected'] = True
			return redirect('wordcount')
	else:
		form = FileUploadForm()
	return render(request, 'upload.html', {
		'form': form
	})

def wordcount_view(request):
	word_count = {}
	if request.session['redirected']:
		request.session['redirected'] = False
		last_file = FileUpload.objects.last()
		mrjob = MRWordCount(args=[last_file.upload_file.path])
		with mrjob.make_runner() as runner:
			runner.run()
			for key, value in mrjob.parse_output(runner.cat_output()):
				word_count[key] = value
		word_count = sorted(word_count.items(), key = lambda x: x[1], reverse = True)
		return render(request, 'wordcount.html', {
			'word_count': word_count
		})
	else:
		return redirect('upload')
		


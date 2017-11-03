from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from urllib.parse import urlencode, quote_plus, unquote
from .forms import LoginForm
from .models import Question, QuestionResult, Choice

# Create your views here.

def leaderboard(request):
	if request.user.is_superuser:
		res = QuestionResult.objects.all()
		res_dict = {}
		for x in res:
			try:
				res_dict[str(x.user)] += 1 if x.selected_choice.is_correct else 0
			except:
				res_dict[str(x.user)] = 1 if x.selected_choice.is_correct else 0
		print(res_dict)
		params = {}
		return render(request, "leaderboard.html", params)
	else:
		raise Http404()

@login_required
def index(request):

	if 'question' not in request.GET:
		get = {}
		get['question'] = 1
		return HttpResponseRedirect("/?" + urlencode(get, quote_via = quote_plus))

	question_id = int(request.GET['question'])
	question = get_object_or_404(Question, id = question_id)
	choices = question.choice_set.all()
	all_questions = Question.objects.all()

	invalid = False
	if request.method == "POST":
		choice_id = int(request.POST['choice'])
		if Choice.objects.get(id = choice_id) in choices:
			try:
				prev_result = QuestionResult.objects.get(Q(user = request.user) & Q(question = question))
				prev_result.delete()
			except:
				pass
			for choice in choices:
				if choice.id == choice_id:
					selected = choice
			result = QuestionResult.objects.create(user = request.user, question = question, selected_choice = selected)
			result.save()

		else:
			invalid = True

	try:
		user_selected = QuestionResult.objects.get(Q(user = request.user) & Q(question = question))
		curr_selected_choice = user_selected.selected_choice.id
	except:
		curr_selected_choice = -1

	print(curr_selected_choice)

	params = {
		'curr_selected_choice' : curr_selected_choice,
		'choices' : choices,
		'all_questions' : all_questions,
		'question' : question,
		'invalid' : invalid,
	}
	return render(request, "index.html", params)

def logout_view(request):
	if request.user.is_authenticated():
		logout(request)
		return HttpResponseRedirect('/login')
	else:
		raise Http404()

def login_view(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')

	invalid = False
	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			username = form.cleaned_data['user']
			password = form.cleaned_data['password']

			user = authenticate(username = username, password = password)

			if user is not None:
				login(request, user)

				try:
					return HttpResponseRedirect(request.GET['next'])
				except:
					return HttpResponseRedirect('/')

			else:
				invalid = True

	else:
		
		form = LoginForm()

	return render(request, 'login.html', {'form' : form, 'invalid': invalid})
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views import View
from apps.course.models import Course
from apps.forum.forms import CreateQuestionForm, CreateAnswerForm
from apps.forum.models import Question, Answer


class CreateQuestion(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        init = {'course_id': kwargs['course_id']}
        question_form = CreateQuestionForm(initial=init)
        return render(request, 'Forum_app/CreateQuestion.html', {'form': question_form})
    def post(self, request, *args, **kwargs):
        question_form = CreateQuestionForm(request.POST)
        if not question_form.is_valid():
            return render(request, 'Forum_app/CreateQuestion.html', {'form': question_form})
        data = question_form.cleaned_data
        if request.user.is_user_in_course(data['course_id']):
            Question.objects.create(course_id=data['course_id'],
                                    user=request.user,
                                    title=data['title'],
                                    body=data['body'])
            return redirect(f"/forum?course_id={data['course_id']}")
        else:
            return HttpResponseBadRequest()


class ListQuestion(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        is_user_in_course = False
        course = None
        filter = request.GET.get('filter', '')
        course_id = request.GET.get('course_id', '')
        questions = Question.objects.filter(title__icontains=filter)
        if course_id != '':
            try:
                course = Course.objects.get(id=course_id)
                questions = questions.filter(course_id=course_id)
                if user.is_authenticated:
                    is_user_in_course = user.is_user_in_course(course.id)
            except Course.DoesNotExist:
                return HttpResponseNotFound()
        context = {
            'questions': questions,
            'course': course,
            'is_user_in_course': is_user_in_course
        }
        return render(request, 'Forum_app/ListQuestions.html', context)


class ShowQuestion(View):
    def get(self, request, *args, **kwargs):
        question_id = kwargs.get('question_id')
        try:
            question = Question.objects.get(id=question_id)
            form = CreateAnswerForm(initial={'question_id': question.id})
            context = {
                'form': form,
                'question': question
            }
            return render(request, 'Forum_app/ShowQuestion.html', context)
        except Question.DoesNotExist:
            return HttpResponseNotFound()


class AddAnswer(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = CreateAnswerForm(request.POST)
        if not form.is_valid():
            question_id = form.cleaned_question_id()
            if Question.objects.filter(id=question_id).exists():
                return redirect(f'/forum/show_question/{question_id}')
            return HttpResponseBadRequest()
        data = form.cleaned_data
        Answer.objects.create(
            question_id=data['question_id'],
            user=request.user,
            answer_body=data['answer_body']
        )
        return redirect(f"/forum/show_question/{data['question_id']}")


class SelectIsTrueAnswer(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        question_id = request.GET.get('question_id')
        answer_id = request.GET.get('answer_id')
        try:
            question = Question.objects.get(id=question_id)
            if question.user.id == user.id:
                if Answer.objects.filter(id=answer_id).exists():
                    Answer.objects.filter(question_id=question_id).update(is_true=False)
                    Answer.objects.filter(id=answer_id).update(is_true=True)
                    return redirect(f"/forum/show_question/{question_id}")
                else:
                    return HttpResponseBadRequest()
        except Question.DoesNotExist:
            return HttpResponseBadRequest()

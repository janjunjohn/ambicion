from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, View
from client.models import Gallery, Sample, Family
from .forms import GalleryForm, SampleForm, LoginForm
from django.contrib import messages
from .gd_client import GoogleDriveClient, DeleteFailedError


class Login(LoginView):
    template_name = 'manager/login.html'
    from_class = LoginForm


class Logout(LogoutView):
    template_name = 'manager/login.html'


class TopView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/top.html'


class MainSlideView(LoginRequiredMixin, CreateView):
    template_name = 'manager/main_slide.html'
    form_class = GalleryForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery_list'] = Gallery.objects.all()
        context['gallery_count'] = Gallery.objects.count()
        return context

    def post(self, request, *args, **kwargs):
        target_pk = request.POST.get('pk')
        target_img = request.FILES.get('img')
        target_title = request.POST.get('title')
        before_img_name = Gallery.objects.get(pk=target_pk).img.name
        is_update_img = False
        if target_img is None:
            target_img = Gallery.objects.get(pk=target_pk).img
        else:
            is_update_img = True
        if target_title == '':
            target_title = Gallery.objects.get(pk=target_pk).title
        try:
            Gallery.objects.update_or_create(
                pk=target_pk,
                defaults={
                    'img': target_img,
                    'title': target_title,
                    'is_standby': False,
                },
            )
            if is_update_img:
                gdc = GoogleDriveClient()
                gdc.upload_file(Gallery.objects.get(pk=target_pk).img.url, 'gallery')
                if len(before_img_name) > 2:
                    print(before_img_name)
                    gdc.delete_file(before_img_name, 'gallery')
            messages.success(request, '更新完了！')
        except DeleteFailedError:
            messages.error(request, 'googleドライブのファイル削除に失敗！不要なファイルを削除してください。')
        except Exception:
            import traceback

            traceback.print_exc()
            messages.error(request, '同じタイトルは使えない！')
        return redirect('manager:main_slide')


class SampleView(CreateView, LoginRequiredMixin):
    template_name = 'manager/sample.html'
    form_class = SampleForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sample_list'] = Sample.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        target_pk = request.POST.get('pk')
        target_img = request.FILES.get('img')
        target_name = request.POST.get('name')
        before_img_name = Sample.objects.get(pk=target_pk).img.name
        is_update_img = False
        if target_img is None:
            target_img = Sample.objects.get(pk=target_pk).img
        else:
            is_update_img = True
        if target_name == '':
            target_name = Sample.objects.get(pk=target_pk).name
        try:
            Sample.objects.update_or_create(
                id=target_pk,
                defaults={'img': target_img, 'name': target_name, 'is_standby': False},
            )
            if is_update_img:
                gdc = GoogleDriveClient()
                num_check_is_exist_file_name = 2
                gdc.upload_file(Sample.objects.get(pk=target_pk).img.url, 'sample')
                if len(before_img_name) > num_check_is_exist_file_name:
                    gdc.delete_file(before_img_name, 'sample')
            messages.success(request, '更新完了！')
        except DeleteFailedError:
            messages.error(request, 'googleドライブのファイル削除に失敗！不要なファイルを削除してください。')
        except Exception:
            import traceback

            traceback.print_exc()
            messages.error(request, '同じ名前は使えない！')
        return redirect('manager:sample')


class FamilyView(CreateView, LoginRequiredMixin):
    template_name = 'manager/family.html'
    model = Family


class DeleteView(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        page_name = self.kwargs['page_name']
        target_pk = self.kwargs['pk']
        if page_name == 'main_slide':
            Gallery.objects.update_or_create(
                pk=target_pk, defaults={'is_standby': True}
            )
        elif page_name == 'sample':
            Sample.objects.update_or_create(pk=target_pk, defaults={'is_standby': True})
        elif page_name == 'family':
            Family.objects.update_or_create(pk=target_pk, defaults={'is_standby': True})
        return redirect(f'manager:{page_name}')

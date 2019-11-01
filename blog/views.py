from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from .models import Post
from .forms import CreateForm
from .cifar import pred_photo


cifar_dict = {
    "airplane": '飛行機', "automobile": '自動車', "bird": '鳥',
    "cat": '猫', "deer": '鹿', "dog": '犬', "frog": 'カエル',
    "horse": '馬', "ship": '舟', "truck": 'トラック'
    }

class PostListView(ListView):
    model = Post
    # template_name = 'blog/home.html' デフォルトは<= <app>/<model>_<viewtype>.htmlなので「blog/post_list.html」
    context_object_name = 'posts'
    ordering = ['-date_posted']

class LabelListView(ListView):
    model = Post
    template_name = 'blog/label_list.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    
    def get_queryset(self):
        label = self.kwargs.get('label')
        return Post.objects.filter(label=label).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs['pk'])
        if post.label:
            label_jp = cifar_dict.get(post.label)
        else:
            label_jp = '判別不可'
        context['label_jp'] = label_jp
        return context

class PostCreateView(TemplateView):
    def __init__(self):
        self.params={
            'form': CreateForm(),
            }
    # GETリクエスト
    def get(self, request, *args, **kwargs):
        return render(request, 'blog/post_form.html', self.params)
    
    # POSTリクエスト
    def post(self, request, *args, **kwargs):
        # POSTされたフォームデータを取得
        form = CreateForm(request.POST, request.FILES)
        # フォームデータのエラーチェック
        if not form.is_valid():
            raise ValueError('invalid form')
        image = form.cleaned_data['image']

        result_label, result_per = pred_photo.check_photo_str(image)

        post = Post()
        post.title = form.cleaned_data['title']
        post.content = form.cleaned_data['content']
        post.author = form.cleaned_data['author']
        post.image = image
        post.label = result_label

        Post.objects.create(
            title=post.title,
            content=post.content,
            author=post.author,
            image=post.image,
            label=post.label,
        )
        messages.success(
            request,
            f'{cifar_dict.get(result_label)}の写真が投稿されました! 可能性は{result_per}%です。修正は更新ページから可能です')
        return redirect('blog-home')

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    fields = ['title', 'image', 'label', 'content', 'author']

class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'


def about(request):
    return render(request, 'blog/about.html', {'context': '当ブログでは画像を自動判別します!'})

def cnn(request):
    text = '「画像の深層学習」と言えばCNNというくらいメジャーな手法である。CNNはConvolutional Neural Networkの頭文字を取ったもので、ニューラルネットワークに「畳み込み」という操作を導入したものである。'
    context = { 'text': text}
    return render(request, 'blog/about_cnn.html', context)

def cifar(request):
    text = 'Kerasを用いてCNNを使用して画像認識を行ってみます。使用するデータはCIFAR-10と呼ばれるもので、飛行機、鳥、犬などの10種類の分類を行うことができます。全体画像数は60000件となり、そのうち50000件が訓練用データ、残り10000件がテスト用データに分けられます。CIFAR-10はKerasのデータセットに用意されているので、簡単にインポートして実行することが出来ます。'
    context = { 'text': text}
    return render(request, 'blog/about_cifar.html', context)
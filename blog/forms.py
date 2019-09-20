from django import forms
from .models import Post

class CreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'content', 'author']
    
    """
    image = forms.ImageField(label="判定する画像を選択してください",
                             error_messages={'missing' : '画像ファイルが選択されていません。',
                                             'invalid' : '分類する画像ファイルを選択してください。',
                                             'invalid_image' : '画像ファイルではないようです。'})
    """
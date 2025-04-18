from django import forms
from .models import Room,Message
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from .models import Room, Topic, Profile

class RoomForm(forms.ModelForm):
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "custom-multi-select"}),
        required=True  
    )

    class Meta:
        model = Room
        fields = ['topics', 'name', 'description']
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter room name", "class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Enter description", "class": "form-control"}),
        }
        
    def clean_topics(self):
        topics = self.cleaned_data.get('topics')
        if not topics:
            raise forms.ValidationError("Please select at least one topic.")
        return topics


        
class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['profile_picture','username','email','password1',"password2"]
        
    def clean_email(self):
            email = self.cleaned_data.get("email")
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('Email already exists')
            
            return email
        
    def save(self, commit=True):
        user = super().save(commit=False) 
        print("commit = " ,commit) 
        if commit:
            user.save()
            print("user created = ",user)  
            if 'profile_picture' in self.cleaned_data:
                profile = Profile.objects.get(user=user)
                profile.profile_picture = self.cleaned_data['profile_picture']
                profile.save()  
        return user
        
class UpdateMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        
        widgets = {
            'text' : forms.Textarea(attrs={'placeholder':'Update message','rows':4, "class":"form-control"})
        }